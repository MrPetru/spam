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
from datetime import datetime
from hashlib import sha1

from spam.lib.helpers import widget_actions
from spam.model import attach_get
from spam.model import modifier_send
from spam.model import modifier_delete_all

class Controller(RestController):
    """
        manipulate with attachemts
    """
    
    wa = widget_actions()
    
    _custom_actions = ['attach', 'download']
    
    @project_set_active
    @asset_set_active
    #@require(is_asset_owner())
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
    #@require(is_asset_owner())
    @expose('json')
    @validate(f_attach, error_handler=get_attach)
    def post_attach(self, proj, asset_id, uploaded, comment=None,
                                                                uploader=None):
        """Put a new attachment"""
        
        session = session_get()
        asset = asset_get(proj, asset_id)
        user = tmpl_context.user

#        if not asset.checkedout or user != asset.owner:
#            msg = '%s %s' % (_('Cannot publish Asset:'), asset.path)
#            return dict(msg=msg, status='error', updates=[])

        if isinstance(uploaded, list):
            # the form might send empty strings, so we strip them
            uploaded = [uf for uf in uploaded if uf]
        else:
            uploaded = [uploaded]
            
        if uploaded[0] != u'':
            result = attachments.put(asset, uploaded[0])
            new_attachment = Attach(result['file_name'], result['file_path'], result['preview_path'])
        else:
            new_attachment = None
            
        for m in asset.modified_entries:
            if m.user != user:
                m.modify()
        
        # create Note for this attachment
        action = u'[%s v%03d]' % (_('commented'), asset.current.ver)
        task = asset.current_task
        
        sender = task.sender
        receiver = task.receiver
        modifier_send(asset, sender, receiver, action, user)
        
        if new_attachment:
            if task.last_attach:
                new_attachment.order = task.last_attach.order + 1
            else:
                new_attachment.order = 1
        task.last_attach = new_attachment
        new_note = Note(user, action, text=comment, task=task)
        new_note.attachment = new_attachment
        asset.current.notes.append(new_note)
        session.refresh(asset.current.annotable)

        msg = '%s %s v%03d' % (_('Commented'), asset.path, asset.current.ver)
        updates = [dict(item=asset, type='updated', topic=TOPIC_ASSETS, extra_data = dict(actions_display_status = self.wa.main(asset, user.id)))]

        # log into Journal
        journal.add(user, '%s - %s' % (msg, asset))

        # notify clients
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=updates)
        
    @project_set_active
    @require(is_project_user())
    @expose()
    def download(self, proj, attach_id):
        """Return a version of an asset from the repository as a file 
        attachment in the response body."""
        
        attach = attach_get(proj, attach_id)
        
        name, ext = os.path.splitext(attach.file_name)
        
        #file_name = "%s_%s_attach_%03d%s" % (attach.note.annotable.annotated.asset.name, attach.note.task.name, 1, ext)
        file_name = "%s_attach_%03d%s" % (attach.note.task.name, attach.order, ext)
        file_name = file_name.replace(" ", "_")

        f = attachments.get(proj, attach)
        
#        if assetver.asset.is_sequence:
#            name = os.path.split(assetver.path)[0]
#            path = '%s.zip' % name
#        else:
#            path = assetver.path
            
        path = attach.file_path
        
        # set the correct content-type so the browser will know what to do
        content_type, encoding = mimetypes.guess_type(path)
        response.headers['Content-Type'] = content_type
        response.headers['Content-Disposition'] = (
                                        ('attachment; filename=%s' %
                                            file_name).encode())
        
        # copy file content in the response body
        shutil.copyfileobj(f, response.body_file)
        f.close()
        return
