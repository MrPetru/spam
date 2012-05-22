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

from spam.lib.helpers import widget_actions
from tg import app_globals as G

# for tasks
from spam.model import Task
from spam.model import task_get_all, task_get

import logging
log = logging.getLogger(__name__)

from spam.lib.widgets import TableAssetShort
t_assets = TableAssetShort()

from spam.lib.widgets import AssetActions, TaskActions, TaskNotes
a_actions = AssetActions()
t_actions = TaskActions()
t_notes = TaskNotes()

from spam.lib.widgets import TaskAssetDescription
asset_description = TaskAssetDescription()

from spam.lib.widgets import FormTaskNew
f_new = FormTaskNew(action=url('/task'))

from spam.model import User, user_get
from spam.lib.helpers import widget_actions

from hashlib import sha1

class Controller(RestController):
    """
        manipulate with tasks
    """
    
    wa = widget_actions()
    
    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.task.get_one')
    def get_one(self, project, asset_id):
        asset = asset_get(project, asset_id)
        a_actions.data = asset.__json__()
        a_actions.extra_data = dict(project=project)
        
        t_actions.data = asset.__json__()
        t_actions.extra_data = dict(project=project)
        
        tmpl_context.a_actions = a_actions
        tmpl_context.t_actions = t_actions
        if asset.current_task:
            notes = asset.current_task.noteslist
            previous_task = task_get(asset.current_task.previous_task_id)
            task_data = asset.current_task.__json__()
        else:
            notes = []
            previous_task = None
            task_data = {}
        
        #previous_task = task_get(asset.current_task.previous_task_id)
        if previous_task:
            previous_task = previous_task.__json__()
            
        tmpl_context.asset_description = asset_description
        
        return dict(asset = asset.__json__(), task = task_data, asset_raw = [asset],
                    previous_task = (previous_task or None), notes=notes)
    
    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.task.get_all')
    def get_all(self, proj):
        
        session = session_get()
        project = tmpl_context.project
        user = tmpl_context.user
        
        # get all tasks for current user
        tasks = task_get_all().filter_by(receiver=user).all()
        
        # get all current associated asset for current user
        assets = []
        for t in tasks:
            if t.parent_asset != None:
                assets.append(t.parent_asset)
                
        asset_list = session.query(Asset).filter_by(owner=user).all()
        for a in asset_list:
            if a not in assets:
                assets.append(a)
                
        # group asset based on path
        asset_group = {}
        for a in assets:
            tmp_path = a.path.replace('/'+a.name, '')
            if tmp_path not in asset_group.keys():
                asset_group.update({tmp_path:[a]})
            else:
                asset_group[tmp_path].append(a)
                
        asset_group_list = []
        for k in asset_group.keys():
            d = dict(id=sha1(k.encode('utf-8')).hexdigest(), path=k, assets=asset_group[k])
            asset_group_list.append(d)
        
        tmpl_context.t_assets = t_assets
        
        return dict(page='user_tasks', sidebar=('projects', project.id),
            assets_groups=asset_group_list)


    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.forms.form')
    def new(self, proj, asset_id, **kwargs):
        """Display a NEW form."""
        project = tmpl_context.project
        
        sender = tmpl_context.user.id
        
        f_new.value = dict(proj=project.id,
                           asset_id=asset_id,
                           sender=sender,
                           project_name_=project.name,
                          )

        query = session_get().query(User)
        users = query.order_by('user_name')
        user_choices = ['']
        user_choices.extend([u.user_name for u in users])
        f_new.child.children.receiver.options = user_choices

        tmpl_context.form = f_new
        return dict(title=_('Create a new task'))
        

    @project_set_active
    @require(is_project_user())
    @expose('json')
    @expose('spam.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, proj, asset_id, sender, receiver, name, description=u''):
        """Create a new task"""
        
        user = tmpl_context.user
        session = session_get()
        
        asset = asset_get(proj, asset_id)
        sender = user_get(sender)
        receiver = user_get(receiver)
        
        old_task = asset.current_task
        new_task = Task(name, description, asset, sender, receiver)
        new_task.previous_task = old_task
        
        action = '[%s]' % (_('task was created created'))
        asset.current.notes.append(Note(user, action, description, new_task))
        
        # insert data in database
        session.add(new_task)
        session.flush()
        msg = '%s %s' % (_('Updated Asset:'), asset.name)

        # notify clients
        updates = [dict(item=asset, type='updated', topic=TOPIC_ASSETS,
                extra_data = dict(actions_display_status = self.wa.main(asset, user.id)))]
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=updates)
