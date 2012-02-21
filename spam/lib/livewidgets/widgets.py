# -*- coding: utf-8 -*-
#
# This file is part of tw2.livewidgets.
#
# tw2.livewidgets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tw2.livewidgets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tw2.livewidgets.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""A collection of ToscaWidget2 that can update in realtime"""

import tw2.core as twc
import tw2.forms as twf

def _maker(self, cls, displays_on=None, **kw):
    """Render a javascript function with prototype: ``function(data) {}``
    that returns the HTML for this field
    """
    if not self:
        return cls.req(**kw).maker(displays_on)
    else:
        if not self.parent:
            self.prepare()
        mw = twc.core.request_local().get('middleware')
        if displays_on is None:
            if self.parent is None:
                displays_on = mw and mw.config.default_engine or 'string'
            else:
                displays_on = twc.template.get_engine_name(
                                                self.parent.template, mw)
        v = {'w':self}
        if mw and mw.config.params_as_vars:
            for p in self._params:
                if hasattr(self, p):
                    v[p] = getattr(self, p)
        eng = mw and mw.engines or twc.template.global_engines
        return eng.render(self.maker_template, displays_on, v)


# Widgets
class LiveWidget(twc.Widget):
    """Base class for LiveWidgets"""
    maker_template = twc.Param('A mako template rendering a javascript function'
        ' with prototype: ``function(data){}`` that returns the HTML for this '
        'field', default='mako:spam.lib.livewidgets.templates.default_maker')
    label = twc.Param('Widget label', default='')
    display_w = twc.Param('display or not widget', default=1)
    display_w2 = twc.Param('display or not widget', default=1)
    type_w = twc.Param('display or not widget', default=1)
    help_text = twc.Param('Tooltip text', default='')
    update_condition = twc.Param('Javascript condition used to filter updates',
        default='true')
    css_class = twc.Param('Custom CSS class', default='')
    show_header = twc.Param('Show widget id in headers', default=True)
    widgets_class = twc.Variable('Base CSS class for the widget', default='')
    data = twc.Variable('A dictionary used to expand formatting strings in '
        'templates', default = {})

    maker = twc.util.class_or_instance(_maker)
    
##    def prepare(self):
##        super(LiveWidget, self).prepare()
##        if hasattr(self, 'parent') and hasattr(self.parent, 'display_w'):
##            if hasattr(self, 'type_w'):
##                self.display_w = self.parent.display_w
##                #self.type_w = self.parent.type_w
##                self.display_w2 = (self.display_w or self.type_w)
##        

## help classes
class widget_actions():
    display_flags = [
        1, # 0,  history - vedi tutta la histori
        1, # 1,  addnote - agiunge una nota
        1, # 2,  download - download last version 
        1, # 3,  checkout - prendi in carrico
        0, # 4,  release - lasciare l'incarico
        0, # 5,  publish - publicare una nuova versione
        0, # 6,  submit - manda per essere revisionato
        0, # 7,  recall - richiama dalla revisione
        0, # 8,  approve - approvare il asset
        0, # 9,  sendback - rimandare in dietro per fare le modifiche
        0, # 10, delete - cancelare l'asset
        0, # 11, revoke - anulare l'approvazione
        1, # 12, open - apri il asset tramite il servizio locale di spam
        ]
    
    user_type_flags = [
        0, # 0, admin
        0, # 1, supervisor
        0, # 2, artist
        0, # 3, owner
        ]
        
    asset_status_flags = [
        0, # 0, checked_in
        0, # 1, submited true=submited, false=(not-submited or sent back_to)
        ]
        
    def set_user_type_flags(self, asset, user):
        #reset user_type_flags
        self.user_type_flags = [0,0,0,0]

        # set flags in user_type_flags based on proprietes of user
        for admin in asset.admins:
            if admin.id == user:
                self.user_type_flags[0] = 1
        for supervisor in asset.supervisors:
            if supervisor.id == user:
                self.user_type_flags[1] = 1
        for artist in asset.artists:
            if artist.id == user:
                self.user_type_flags[2] = 1
        if asset.owner_id == user:
            self.user_type_flags[3] = 1
        #print (asset.owner_id, 'asset owner')
        # for debug        
        #print(self.user_type_flags, '[admin, supervisor, user] for user:', user)
        
    def set_asset_status_flags(self, asset):
    #    # reset asset_status_flags 
    #    self.asset_status_flags = [0,0]

        if asset.checkedout:
            self.display_flags[3] = 0
        
        if asset.checkedout and (not self.user_type_flags[1]) and (not self.user_type_flags[3]):
            self.display_flags[4] = 0
        
        if not asset.checkedout and self.user_type_flags[1]:
            self.display_flags[4] = 0
        
        if asset.submitted and self.user_type_flags[3]:
            self.display_flags[6] = 0
            self.display_flags[5] = 0
        
        if asset.submitted and not self.user_type_flags[1]:
            self.display_flags[12] = 0
            
        if not asset.submitted and self.user_type_flags[3]:
            self.display_flags[7] = 0
            
        if not asset.submitted:# and user_type_flags[1]:
            self.display_flags[9] = 0
            self.display_flags[8] = 0
            
        if asset.approved:
            self.display_flags[8] = 0
            self.display_flags[9] = 0
            self.display_flags[4] = 0
            self.display_flags[7] = 0
            self.display_flags[5] = 0
            self.display_flags[3] = 0
            
        if asset.approved and not self.user_type_flags[1]:
            self.display_flags[4] = 0
            
        if not asset.approved and not asset.submitted:
            self.display_flags[9] = 0
            
        if not asset.approved:
            self.display_flags[11] = 0
            

    def list_union(self,list_A, list_B): # A union B
        union = []
        if len(list_A)==0:
            if len(list_B)==0:
                return (union)
            else:
                return (list_B)
        elif len(list_B)==0:
            return (list_A)
        else:
            for index in range(len(list_A)):
                union.append(list_A[index] or list_B[index])
            return (union)
            
    def set_display_flags_by_user(self):
        # set display_flags based on user type
        admin_display_status=supervisor_display_status=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        artist_display_status = owner_display_status = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        if self.user_type_flags[0]:
            # set display for admin
            admin_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                0, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                0, # 8,  approuve
                0, # 9,  sendback
                1, # 10, delete
                0, # 11, revoke
                0, # 12, open
                ]
        if self.user_type_flags[1]:
            # set display for supervisor
            supervisor_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                1, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                1, # 8,  approve
                1, # 9,  sendback
                0, # 10, delete
                1, # 11, revoke
                1, # 12, open
                ]
            
        if self.user_type_flags[2]:
            # set display for user
            artist_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                1, # 3,  checkout
                0, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                0, # 8,  approve
                0, # 9,  sendback
                0, # 10, delete
                0, # 11, revoke
                0, # 12, open
                ]
        if self.user_type_flags[3]:
            # set display for user
            owner_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                1, # 4,  release
                1, # 5,  publish
                1, # 6,  submit
                1, # 7,  recall
                0, # 8,  approve
                0, # 9,  sendback
                0, # 10, delete
                0, # 11, revoke
                1, # 12, open
                ]
        #print (self.list_union(admin_display_status, self.list_union(supervisor_display_status,artist_display_status)))
        self.display_flags = self.list_union(
            admin_display_status, self.list_union(
                supervisor_display_status,self.list_union(artist_display_status, owner_display_status)))
        
    def main(self, asset, cur_user):
        self.set_user_type_flags(asset, cur_user)
        self.set_display_flags_by_user()
        self.set_asset_status_flags(asset)
        
        #print (asset.category_id)
        #print (asset.owner_id)
        #print (self.display_flags)
        return (self.display_flags)

class LiveCompoundWidget(LiveWidget, twc.CompoundWidget):
    """Base class for compound LiveWidgets

    If the ``key`` of the compound widget corresponds to an element
    in its parent ``data``, the widget will exted ``data`` with the subelements
    prefixing their names with its ``key``
    """
    children = []

    @classmethod
    def post_define(cls):
        # a compound widget must have id=None to propagate the object or
        # dictionary received from its ItemLayout parent as "value" to its
        # children, so if "id" is set we copy it to "key" (if "key" is not
        # already set) and then reset it
        id = getattr(cls, 'id', None)
        cls.key = cls.key or id or ''
        if id:
            cls.id = None

    def prepare(self):
        # extend data with subelements
        newdata = {}
        if self.key in self.data:
            if isinstance(self.data[self.key], dict):
                for k, v in self.data[self.key].iteritems():
                    newdata['%s_%s' % (self.key, k)] = v
            elif hasattr(self.data[self.key], '__dict__'):
                for k, v in self.data[self.key].__dict__.iteritems():
                    newdata['%s_%s' % (self.key, k)] = v
        self.data.update(newdata)
        if hasattr(self, 'parent') and hasattr(self.parent, 'display_w'):
            if hasattr(self, 'type_w'):
                self.display_w = self.parent.display_w
                #self.type_w = self.parent.type_w
                self.display_w2 = (self.display_w or self.type_w)

        # prepare data for children
        for c in self.children:
            c.data = self.data

        # we call super().prepare() after updating children data so if one of
        # our children is a LiveCompoundWidget, it can propagate it to its
        # own children
        super(LiveCompoundWidget, self).prepare()


class Box(LiveCompoundWidget):
    """A simple container widget

    Box is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:spam.lib.livewidgets.templates.box'
    maker_template = 'mako:spam.lib.livewidgets.templates.box_maker'

    widget_class = 'lw_box'
        
class BoxAction(LiveCompoundWidget):
    """A simple container widget

    Box is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    display_data = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default=[])
    template = 'mako:spam.lib.livewidgets.templates.box'
    maker_template = 'mako:spam.lib.livewidgets.templates.box_maker'

    widget_class = 'lw_box'
    def prepare(self):
        wa = widget_actions()
        self.display_data=wa.main(self.value, self.parent.parent.user.id)
        super(BoxAction, self).prepare()
        

class Link(LiveCompoundWidget):
    """A link widget

    Link is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:spam.lib.livewidgets.templates.link'
    maker_template = 'mako:spam.lib.livewidgets.templates.link_maker'
    dest = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default='')

    widget_class = 'lw_link'

class ActionButton(LiveCompoundWidget):
    """An button widget

    Button is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:spam.lib.livewidgets.templates.actionbutton'
    maker_template = 'mako:spam.lib.livewidgets.templates.actionbutton_maker'
    action = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default='')
    index = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default=None)
    display_cond = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default=0)
    dialog = twc.Param('Whether the button target should open in a dialog '
        '(the button will have a "dialog" css class, creating the dialog is '
        'left to the application)', default=False)

    widget_class = 'lw_actionbutton'
    
    def prepare(self):
        #print(self.parent.parent.parent.extra_data)
        self.display_cond = self.parent.display_data[int(self.index)]
        super(ActionButton, self).prepare()

class Button(LiveCompoundWidget):
    """An button widget

    Button is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:spam.lib.livewidgets.templates.button'
    maker_template = 'mako:spam.lib.livewidgets.templates.button_maker'
    action = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary and used as "href" '
        'attribute', default='')
    dialog = twc.Param('Whether the button target should open in a dialog '
        '(the button will have a "dialog" css class, creating the dialog is '
        'left to the application)', default=False)

    widget_class = 'lw_button'


class Text(LiveWidget):
    """A simple text widget"""
    template = 'mako:spam.lib.livewidgets.templates.text'
    maker_template = 'mako:spam.lib.livewidgets.templates.text_maker'
    text = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary, ``None`` defaults to the '
        'widget\'s value', default=None)

    widget_class = 'lw_text'

    def prepare(self):
        super(Text, self).prepare()

        # use widget value if "text" was not given
        self.text = self.text or str(self.value) or ''


class Image(LiveWidget):
    """An image widget"""
    template = 'mako:spam.lib.livewidgets.templates.image'
    maker_template = 'mako:spam.lib.livewidgets.templates.image_maker'
    src = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary, ``None`` defaults to the '
        'widget\'s value', default=None)

    widget_class = 'lw_image'

    def prepare(self):
        super(Image, self).prepare()
        if self.id == 'thumbnail':
            if self.value == '' or self.value == None:
                self.parent.css_class = 'thumbnail_image_not_found'
                self.src = ''
                self.help_text = ''
        else:
            # use widget value if "src" was not given
            self.src = self.src or self.value or ''


class Icon(LiveWidget):
    """An icon widget"""
    template = 'mako:spam.lib.livewidgets.templates.icon'
    maker_template = 'mako:spam.lib.livewidgets.templates.icon_maker'
    icon_class = twc.Param('The css class identifying this icon', default='')

    widget_class = 'lw_icon'


# Layouts
class ItemLayout(twc.CompoundWidget, LiveWidget):
    """Base class for LiveWidget layouts"""
    maker_template = twc.Param('A mako template rendering a javascript function'
        ' with prototype: ``function(data){}`` that returns the HTML for this '
        'layout', default='mako:spam.lib.livewidgets.templates.default_maker')
    append_selector = twc.Param('A jQuery selector that will be used to '
        'determine where to append new items', default='')

    def prepare(self):
        # set item_id
        self.item_id = getattr(self.value, 'id', '')

        # extract a dictionary from value
        if isinstance(self.value, dict):
            self.data = self.value
        elif hasattr(self.value, '__json__'):
            self.data = self.value.__json__()
        else:
            self.data = getattr(self.value, '__dict__', {})
            

        # extend data with parent's extra_data
        if self.parent and hasattr(self.parent, 'extra_data'):
            self.data.update(self.parent.extra_data)

        # prepare data for children
        for c in self.children:
            c.data = self.data

        # we call super().prepare() after updating children data so if one of
        # our children is a LiveCompoundWidget, it can propagate it to its
        # own children
        super(ItemLayout, self).prepare()

    maker = twc.util.class_or_instance(_maker)


class ListItemLayout(ItemLayout):
    """A compound widget that wraps its children in a <li> element"""
    template = 'mako:spam.lib.livewidgets.templates.list_item_layout'
    maker_template = 'mako:spam.lib.livewidgets.templates.list_item_layout_maker'
    append_selector = 'ul'


class RowLayout(ItemLayout):
    """A compound widget that wraps its children in a <tr> element"""
    template = 'mako:spam.lib.livewidgets.templates.row_layout'
    maker_template = 'mako:spam.lib.livewidgets.templates.row_layout_maker'
    append_selector = 'table tbody'
    


# Containers
class LiveContainer(twc.RepeatingWidget, LiveWidget):
    """Base class for LiveWdigets containers"""
    container_class = twc.Param('CSS class for the container element',
        default='')
    extra_data = twc.Param('Additional data that will be appended to each '
        'items\'s data', default={})
    update_topic = twc.Param('The topic this container is listening to for '
        'updates', default=None)
    update_filter = twc.Param('A class used to filter updates', default=None)
    callbacks = twc.Param('A javascript object providing custom callbacks for '
        'update events', default='{}')
    children = twc.Required

    resources = [
        twc.JSLink(modname=__name__, filename='static/livewidgets.js'),
#        twc.JSLink(modname=__name__, filename='static/jquery.js'),
    ]

class LiveRepeating(twc.RepeatingWidget, LiveWidget):
    """Base class for LiveWdigets containers"""
    container_class = twc.Param('CSS class for the container element',
        default='')
    extra_data = twc.Param('Additional data that will be appended to each '
        'items\'s data', default={})
    ##children = twc.Required
    
    def prepare(self):
        #self.data = dict()

        # extend data with parent's extra_data
        if self.parent and hasattr(self.parent, 'extra_data'):
            self.data.update(self.parent.extra_data)

        # prepare data for children
        self.child.data = self.data
        super(LiveRepeating, self).prepare()
    
    maker = twc.util.class_or_instance(_maker)
    

class LiveList(LiveContainer):
    """A repeating widget that render its values as an <ul> element"""
    template = 'mako:spam.lib.livewidgets.templates.livelist'
    child = ListItemLayout

    container_class = 'lw_livelist'


class LiveTable(LiveContainer):
    """A repeating widget that render its values as an <table> element"""
    show_headers = twc.Param('Show table headers', default=True)

    template = 'mako:spam.lib.livewidgets.templates.livetable'
    child = RowLayout

    container_class = 'lw_livetable'

class StatusBox(ItemLayout): ## this is a compound widget for LiveBox
    """ used inside LiveBox """
    template = 'mako:spam.lib.livewidgets.templates.statusbox'
    maker_template = 'mako:spam.lib.livewidgets.templates.statusbox_maker'
    append_selector = 'lw_statusbox'
    update_condition = 'false'
    
class LiveBox(LiveContainer):
    """ when used in summary page as a container """
    ## is a container like LiveTable and LiveList
    ## that handling update of his children but nom him self
    ## this widget don't have a maker_template 
    template = 'mako:spam.lib.livewidgets.templates.livebox' 
    child = StatusBox # must be a  compound widget like RowLayout
    container_class = 'lw_livebox'
    
class StatusIconBox(LiveRepeating):
    """Custom livewidget to show a box of status icons."""
    params = []
    template = 'mako:spam.lib.livewidgets.templates.statusiconbox'
    maker_template = 'mako:spam.lib.livewidgets.templates.statusiconbox_maker'
    update_condition = 'true'
    child = StatusBox
    css_class = 'statusiconbox'
    show_header = False
    sortable = False

class LiveThumbnail(LiveCompoundWidget):
    """A simple container widget

    Box is a compound widget, and can contain other widgets like ``Text``,
    ``Image`` or ``Icon``
    """
    template = 'mako:spam.lib.livewidgets.templates.livethumbnail'
    maker_template = 'mako:spam.lib.livewidgets.templates.livethumbnail_maker'
    
    src = twc.Param('A formatting string the will be expanded with the '
        'widget\'s ItemLayout value as a dictionary, ``None`` defaults to the '
        'widget\'s value', default='')

    widget_class = 'lw_thumbnail'
    css_class = 'thumbnail'
    children = [
        Image(
            id='thumbnail',
            help_text='thumbnail',
            css_class='thumbnail',
            condition='data.has_preview',
            src='/repo/%(thumbnail)s',
            )
    ]


class CategoryContainer(twc.RepeatingWidget):
    """Top level container for Assets Categories"""
    
    template = 'mako:spam.lib.livewidgets.templates.categorycontainer'
    parent_container_id =  twc.Param('Parent container id: shot id or librarygroup id', default='')
    update_on_topic = twc.Param('topic that define if widget needed to be updatetd', default='')
    child = Box(widget_class="toggle expanded", children=[Text(id='id')])
    

# DEBUG stuff
class Dummy(object):
    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)


