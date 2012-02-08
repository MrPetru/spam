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
"""Note controller"""

from tg import expose, url, tmpl_context, redirect, validate, require
from tg.controllers import RestController
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from spam.model import session_get, annotable_get, note_get, Note, AssetVersion
from spam.lib.widgets import FormNoteNew, FormNoteConfirm
from spam.lib.widgets import TableNotes
from spam.lib.notifications import notify, TOPIC_NOTES, TOPIC_ASSETS, TOPICS
from repoze.what.predicates import in_group
from spam.lib.decorators import project_set_active
from spam.lib.predicates import is_project_user, is_project_admin

import logging
log = logging.getLogger(__name__)

# form widgets
f_new = FormNoteNew(action=url('/note'))
f_confirm = FormNoteConfirm(action=url('/note'))

# live widgets
t_notes = TableNotes(id='t_notes')

class Controller(RestController):
    """REST controller for managing notes.

    In addition to the standard REST verbs this controller defines the following
    REST-like methods:
        * ``pin``  (:meth:`pin`)
        * ``unpin`` (:meth:`unpin`)
    """
    
    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.notes.get_all')
    def get_all(self, proj, annotable_id):
        """Return a html fragment with a list of notes for this object."""
        annotable = annotable_get(annotable_id)
        t_notes.value = annotable.notes
        t_notes.update_filter = annotable.id
        t_notes.extra_data = dict(proj=tmpl_context.project.id)
        tmpl_context.t_notes = t_notes
        return dict()

    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.notes.get_all')
    def _default(self, proj, annotable_id, *args, **kwargs):
        """Catch request to `note/<something>' and pass them to :meth:`get_all`,
        because RESTController doesn't dispatch to get_all when there are
        arguments.
        """
        return self.get_all(proj, annotable_id)

    @project_set_active
    @require(is_project_user())
    @expose('json')
    @expose('spam.templates.notes.get_one')
    def get_one(self, proj, annotable_id, note_id):
        """This method is currently unused, but is needed for the 
        RESTController to work."""
        note = note_get(note_id)
        return dict(note=note)

    @project_set_active
    @require(is_project_user())
    @expose('spam.templates.forms.form')
    def new(self, proj, annotable_id, **kwargs):
        """Display a NEW form."""
        project = tmpl_context.project
        session = session_get()
        annotable = annotable_get(annotable_id)
        
        f_new.value = dict(proj=project.id, annotable_id=annotable.id)
        tmpl_context.form = f_new
        return dict(title='%s %s' % (_('Add a note to:'),
                                                    annotable.annotated.path))
    
    @project_set_active
    @require(is_project_user())
    @expose('json')
    #@expose('spam.templates.forms.result')
    @validate(f_new, error_handler=new)
    def post(self, proj, annotable_id, text):
        """Add notes to a ``annotable`` obect."""
        session = session_get()
        user = tmpl_context.user
        annotable = annotable_get(annotable_id)
        ob = annotable.annotated

        note = Note(user, text)
        annotable.notes.append(note)
        session.refresh(annotable)

        msg = '%s %s' % (_('Added note to:'), annotable.annotated.path)

        updates = [dict(item=note, type='added', topic=TOPIC_NOTES,
                                                        filter=ob.annotable.id)]
        if isinstance(ob, AssetVersion):
            updates.append(dict(item=ob.asset, topic=TOPIC_ASSETS))
        else:
            updates.append(dict(item=ob, topic=TOPICS[ob.__class__]))
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=[])
    
    @project_set_active
    @require(is_project_admin())
    @expose('spam.templates.forms.form')
    def get_delete(self, proj, note_id, **kwargs):
        """Display a DELETE confirmation form."""
        project = tmpl_context.project
        note = note_get(note_id)
        f_confirm.custom_method = 'DELETE'
        f_confirm.value = dict(proj=project.id,
                               note_id=note.id,
                               text_=note.text)
        tmpl_context.form = f_confirm
        return dict(title='%s %s?' % (
                        _('Are you sure you want to delete note:'), note.id))

    @project_set_active
    @require(is_project_admin())
    @expose('json')
    @expose('spam.templates.forms.result')
    @validate(f_confirm, error_handler=get_delete)
    def post_delete(self, proj, note_id):
        """Delete a note."""
        session = session_get()
        note = note_get(note_id)
        ob = note.annotated
        
        session.delete(note)
        session.refresh(ob.annotable)
        
        msg = '%s %s' % (_('Deleted note:'), note.id)

        updates = [dict(item=note, type='deleted', topic=TOPIC_NOTES,
                                                        filter=ob.annotable.id)]
        if isinstance(ob, AssetVersion):
            updates.append(dict(item=ob.asset, topic=TOPIC_ASSETS))
        else:
            updates.append(dict(item=ob, topic=TOPICS[ob.__class__]))
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=updates)
    
    # Custom REST-like actions
    _custom_actions = ['pin', 'unpin']

    @project_set_active
    @require(is_project_admin())
    @expose('json')
    @validate(f_confirm)
    def pin(self, proj, note_id):
        """Pin a note."""
        session = session_get()
        note = note_get(note_id)
        ob = note.annotated

        if note.sticky:
            msg = '%s %s' % (_('Note is already pinned:'), note.id)
            return dict(msg=msg, status='info', updates=[])

        note.sticky = True
        session.refresh(ob.annotable)

        msg = '%s %s' % (_('Pinned note:'), note.id)

        updates = [
            dict(item=note, topic=TOPIC_NOTES, filter=ob.annotable.id),
            dict(item=ob, topic=TOPICS[ob.__class__]),
            ]
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=updates)
    
    @project_set_active
    @require(is_project_admin())
    @expose('json')
    @validate(f_confirm)
    def unpin(self, proj, note_id):
        """Un-pin a note."""
        session = session_get()
        note = note_get(note_id)
        ob = note.annotated

        if not note.sticky:
            msg = '%s %s' % (_('Note is not pinned:'), note.id)
            return dict(msg=msg, status='info', updates=[])

        note.sticky = False
        session.refresh(ob.annotable)

        msg = '%s %s' % (_('Un-pinned note:'), note.id)

        updates = [
            dict(item=note, topic=TOPIC_NOTES, filter=ob.annotable.id),
            dict(item=ob, topic=TOPICS[ob.__class__]),
            ]
        notify.send(updates)

        return dict(msg=msg, status='ok', updates=updates)
    

