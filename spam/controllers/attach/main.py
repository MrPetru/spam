# -*- coding: utf-8 -*-
#
# This file is part of SPAM (Spark Project & Asset Manager).
#
# SPAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPAM.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""Task controller"""

import os, shutil, mimetypes
from tg import expose, url, tmpl_context, validate, require, response
from tg.controllers import RestController
from tg.decorators import with_trailing_slash
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from spam.model import session_get, Asset, AssetVersion, Category, Note
from spam.model import project_get, container_get, asset_get, category_get
from spam.model import assetversion_get
from spam.lib.widgets import FormAssetNew, FormAssetEdit, FormAssetConfirm
from spam.lib.widgets import FormAttachUpload
#from spam.lib.widgets import BoxStatus
from spam.lib import repo, preview
from spam.lib.notifications import notify, TOPIC_ASSETS
from spam.lib.journaling import journal
from spam.lib.decorators import project_set_active, asset_set_active
from repoze.what.predicates import Any
from spam.lib.predicates import is_project_user, is_project_admin
from spam.lib.predicates import is_asset_supervisor, is_asset_artist
from spam.lib.predicates import is_asset_owner

from spam.lib.helpers import widget_actions
from tg import app_globals as G

# for tasks
from spam.model import Task, Note, Attach
from spam.model import task_get_all, task_get

import logging
log = logging.getLogger(__name__)

f_attach = FormAttachUpload(action=url('/attach'))

from spam.lib import attachments

class Controller(RestController):
    """
        manipulate with attachemts
    """
    
    _custom_actions = ['attach']
    
    @project_set_active
    @asset_set_active
    @require(is_asset_owner())
    @expose('spam.templates.forms.form')
    def get_attach(self, proj, asset_id, **kwargs):
        """Display a attach form."""
        asset = asset_get(proj, asset_id)
        f_attach.custom_method = 'ATTACH'
        f_attach.value = dict(proj=asset.project.id,
                               asset_id=asset.id,
                               project_name_=asset.project.name,
                               container_=asset.parent.owner.path,
                               category_id_=asset.category.id,
                               asset_name_=asset.name,
                              )
        
        name, ext = os.path.splitext(asset.name)
        #f_attach.child.children.uploader.ext = ext
        tmpl_context.form = f_attach
        return dict(title='%s %s' % (_('Upload an attach for Asset:'),
                                                                    asset.path))
    
        
    @project_set_active
    @asset_set_active
    @require(is_asset_owner())
    @expose('json')
    @validate(f_attach, error_handler=get_attach)
    def post_attach(self, proj, asset_id, name, uploaded, comment=None,
                                                                uploader=None):
        """Put a new attachment"""
        
        session = session_get()
        asset = asset_get(proj, asset_id)
        user = tmpl_context.user

        if not asset.checkedout or user != asset.owner:
            msg = '%s %s' % (_('Cannot publish Asset:'), asset.path)
            return dict(msg=msg, status='error', updates=[])

        if isinstance(uploaded, list):
            # the form might send empty strings, so we strip them
            uploaded = [uf for uf in uploaded if uf]
        else:
            uploaded = [uploaded]
        
        result = attachments.put(asset, uploaded[0], name)
        print (result)
        
        new_attachment = Attach(result['file_name'], result['file_path'])
        
        # create Note for this attachment
        action = u'[%s v%03d]' % (_('attachment to'), asset.current.ver)
        task = asset.current_task
        new_note = Note(user, action, text=comment, task=task)
        new_note.attachment = new_attachment
        asset.current.notes.append(new_note)
        session.refresh(asset.current.annotable)

#        # check that uploaded file extension matches asset name
#        name, ext = os.path.splitext(asset.name)
#        for uf in uploaded:
#            uf_name, uf_ext = os.path.splitext(uf)
#            if not uf_ext == ext:
#                msg = '%s %s' % (_('Uploaded file must be of type:'), ext)
#                return dict(msg=msg, status='error', updates=[])

#        # commit file to repo
#        if comment is None or comment=='None':
#            comment = ''
#        header = u'[%s %s v%03d]' % (_('published'), asset.path,
#                                                            asset.current.ver+1)
#        text = comment and u'%s\n%s' % (header, comment) or header
#        repo_id = repo.commit(proj, asset, uploaded, text, user.user_name)
#        if not repo_id:
#            msg = '%s %s' % (_('The latest version is already:'), uploaded)
#            return dict(msg=msg, status='info', updates=[])

#        # create a new version
#        newver = AssetVersion(asset, asset.current.ver+1, user, repo_id)
#        #text = u'[%s v%03d]\n%s' % (_('published'), newver.ver, comment)
#        task = newver.asset.current_task
#        text = u'%s' % comment
#        action = u'[%s v%03d]' % (_('published'), newver.ver)
#        newver.notes.append(Note(user, action, text, task))
#        session.flush()
#        session.refresh(asset)

#        # create thumbnail and preview
#        preview.make_thumb(asset)
#        preview.make_preview(asset)

#        msg = '%s %s v%03d' % (_('Published'), asset.path, newver.ver)
#        updates = [dict(item=asset, type='updated', topic=TOPIC_ASSETS, extra_data = dict(actions_display_status = self.wa.main(asset, user.id)))]

#        # log into Journal
#        journal.add(user, '%s - %s' % (msg, asset))

#        # notify clients
#        notify.send(updates)

#        return dict(msg=msg, status='ok', updates=updates)
        return dict(msg='attached', status='ok', updates=[])
