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
# Mr. Petru <petrea.email@gmail.com>
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
from spam.lib.widgets import FormAssetPublish, FormAssetStatus
from spam.lib.widgets import TableAssets, TableAssetHistory
#from spam.lib.widgets import BoxStatus
from spam.lib import repo, preview
from spam.lib.notifications import notify, TOPIC_ASSETS
from spam.lib.journaling import journal
from spam.lib.decorators import project_set_active, asset_set_active
from repoze.what.predicates import Any
from spam.lib.predicates import is_project_user, is_project_admin
from spam.lib.predicates import is_asset_supervisor, is_asset_artist
from spam.lib.predicates import is_asset_owner

from tg import app_globals as G

# for tasks
from spam.model import Task
from spam.model import task_get_all, task_get

import logging
log = logging.getLogger(__name__)

from spam.lib.widgets import TableAssetShort
t_assets = TableAssetShort()

from spam.lib.widgets import TaskAssetDescription
asset_description = TaskAssetDescription()

from spam.lib.widgets import OldTasks
o_tasks = OldTasks()

from spam.lib.widgets import FormTaskNew
f_new = FormTaskNew(action=url('/task'))

from spam.model import User, user_get
from spam.lib.helpers import widget_actions

from hashlib import sha1

from spam.lib import attachments
from spam.model import Attach, Scene, Libgroup, Category

from spam.model import modifier_send, modifier_delete_all

class Controller(RestController):
    """
        manipulate with tasks
    """
    
    wa = widget_actions()
    
    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.task.get_one')
    def get_one(self, proj, asset_id):
        
        project = tmpl_context.project
        asset = asset_get(project, asset_id)
        user = tmpl_context.user
        
        old_tasks = []
        if asset.current_task:
            ct = asset.current_task
            while ct.previous_task:
                old_tasks.append(ct.previous_task)
                ct = ct.previous_task

        for m in asset.modified_entries:
            if m.user == user:
                m.accesed()
                
        tmpl_context.asset_description = asset_description
        tmpl_context.o_tasks = o_tasks

        return dict(asset = [asset], old_tasks = old_tasks)
    
    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.task.get_all')
    def get_all(self, proj):
        
        session = session_get()
        project = tmpl_context.project
        user = tmpl_context.user
        
        # get all tasks
        tasks = task_get_all().filter(Task.parent_asset!=None).all()
        
        all_filter_values = ['wip', 'idle', 'approved', 'submitted', 'rejected', 'library', 'scene', 'None', 'modified']
        
        # get all current associated asset for current user
        assets = []
        for t in tasks:
            if t.parent_asset.project == project:
				# if current user is in project admin list the show all tasks
                if user in project.admins:
                    assets.append(t.parent_asset)
                    all_filter_values.append(t.parent_asset.name)
                    continue
                if (t.receiver == user or t.sender == user or t.parent_asset.owner == user):
                    assets.append(t.parent_asset)
                    all_filter_values.append(t.parent_asset.name)
                else:
                    if not t.receiver:
                        if (user in t.parent_asset.artists) or (user in t.parent_asset.supervisors):
                            assets.append(t.parent_asset)
                            all_filter_values.append(t.parent_asset.name)
        
        tmpl_context.t_assets = t_assets
        
        # get prject users
        for u in project.users:
            if u.user_name not in all_filter_values:
                all_filter_values.append(u.user_name)
                all_filter_values.append('from:%s' % u.user_name)
                all_filter_values.append('to:%s' % u.user_name)
                
        # get project scenes and shots
        scenes = session.query(Scene).filter(Scene.project == project).all()
        for sc in scenes:
            if sc.name not in all_filter_values:
                all_filter_values.append(sc.name)
                for sh in sc.shots:
                    if sh.name not in all_filter_values:
                        all_filter_values.append(sh.name)
        
        # get project libgroups
        libgroups = session.query(Libgroup).filter(Libgroup.project == project).all()
        for lg in libgroups:
            if lg.name not in all_filter_values:
                all_filter_values.append(lg.name)
                
        # get all category
        categories = session.query(Category).all()
        for ct in categories:
            if ct.name not in all_filter_values:
                all_filter_values.append(ct.name)
        
        tmpl_context.all_filter_values = all_filter_values
        
        def cpmModified(a, b):
            ma = a.modified_entries
            mb = b.modified_entries
            sa = 0
            sb = 0
            for m in ma:
                if m.user == user:
                    sa = int(m.modified)
            
            for m in mb:
                if m.user == user:
                    sb = int(m.modified)
                
            return sb - sa
            
        def cmpCategory(a, b):
            return a.category.ordering - b.category.ordering
            
        def cmpName(a, b):
            if a.name > b.name:
                return 1
            return -1
        
        assets.sort(cmp=cmpName)
        assets.sort(cmp=cmpCategory)    
        assets.sort(cmp=cpmModified)
        
        return dict(page='user_tasks', sidebar=('projects', project.id),
            assets=assets)


    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.forms.form')
    def new(self, proj, asset_id, **kwargs):
        """Display a NEW form."""
        project = tmpl_context.project
        asset = asset_get(proj, asset_id)
        
        sender = tmpl_context.user.id
        
        f_new.value = dict(proj=project.id,
                           asset_id=asset_id,
                           sender=sender,
                           project_name_=project.name,
                          )

#        query = session_get().query(User)
#        users = query.order_by('user_name')
        users = asset.artists
        user_choices = []
        user_choices.extend([u.user_name for u in users])
        f_new.child.children.receiver.options = user_choices

        tmpl_context.form = f_new
        return dict(title=_('Create a new task'))
        

    @project_set_active
    @require(is_project_user())
    @expose('json')
    @expose('spam.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, proj, asset_id, sender, name, receiver, uploaded, uploader=None, description=u''):
        """Create a new task"""
        
        user = tmpl_context.user
        session = session_get()
        
        asset = asset_get(proj, asset_id)
        sender = user_get(sender)
        if receiver:
            receiver = user_get(receiver)
        else:
            receiver = None
        
        if asset.approved:
            asset.revoke(user)
            
        #########
            
        if isinstance(uploaded, list):
            # the form might send empty strings, so we strip them
            uploaded = [uf for uf in uploaded if uf]
        else:
            uploaded = [uploaded]
        
        if uploaded[0] != u'':
            result = attachments.put(asset, uploaded[0])
            new_attachment = Attach(result['file_name'], result['file_path'], result['preview_path'])
            new_attachment.order = 1
        else:
            new_attachment = None
        
        old_task = asset.current_task
        task_name = u'Submitted For Revision'
        new_task = Task(name, description, asset, sender, receiver)
        new_task.previous_task = old_task
        
        action = '[%s]' % (_('task was created'))
        
        new_note = Note(user, action, description, new_task)
        new_note.attachment = new_attachment
        
        asset.current.notes.append(new_note)
        
        # delete all modifiers entry
        modifier_delete_all(asset)
        
        session.refresh(asset.current.annotable)
        
        # sign asset as modified for receiver
        modifier_send(asset, sender, receiver, action)
        
        #########
        
        # insert data in database
        session.add(new_task)
        session.flush()
        msg = '%s %s' % (_('Updated Asset:'), asset.name)

        updates = [dict(item=asset, type='updated', topic=TOPIC_ASSETS, extra_data = dict(actions_display_status = self.wa.main(asset, user.id)))]
        status = 'ok'

        # log into Journal
        journal.add(user, '%s - %s' % (msg, asset))

        # notify clients
        notify.send(updates)

        return dict(msg=msg, status=status, updates=updates)
        
