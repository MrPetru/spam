## This file is part of SPAM (Spark Project & Asset Manager).
##
## SPAM is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## SPAM is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SPAM.  If not, see <http://www.gnu.org/licenses/>.
##
## Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
## Contributor(s): 
##

<%inherit file="spam.templates.tab"/>

##<h2>${_('tags')}</h2>
##% if c.predicates.is_project_admin():
##<a href="${tg.url('/tag/%s/new' % c.libgroup.id)}"
##   class="button dialog">add tags</a>
##% endif
##${c.b_tags(id="taglist", items=c.libgroup.tags,
##                    taggable_id=c.libgroup.taggable.id,
##                    extra_data=tag_extra_data,
##                    update_listener_adder="notify.add_listener_tab").display(value=c.libgroup.tags) | n}
##<br/>
##<br/>

###<h2>${_('notes')}</h2>
###% if c.predicates.is_project_admin():
###<a href="${tg.url('/note/%s/%s/new' % (c.project.id, c.libgroup.id))}"
###   rel="#overlay" class="overlay button dialog">add note</a>
###% endif
###${c.t_notes(id="notestable",
###        value=c.libgroup.notes,
###        annotable_id=c.libgroup.annotable.id,
###        extra_data=note_extra_data,
###        update_listener_adder="notify.add_listener_tab",
###    ).display() | n}


<h2>${_('description')}</h2>

<div class="bibliaheader">
    % if c.predicates.is_project_admin():
        ${c.action.display() | n }
    % endif
</div>
<div class="bibliabody">
    ${libgroup.description | n }
</div>

<br/>

% if c.libgroup.subgroups:
    <h2>${_('subgroups')}</h2>
    ${c.b_libgroups_status(id="status_%s_subgroups" % c.libgroup.id,
                    items=c.libgroup.subgroups, libgroup_id=c.libgroup.id,
                    update_listener_adder="notify.add_listener_tab").display(value=c.libgroup.subgroups) | n}
    <br/>
    <br/>
% endif

% if c.libgroup.assets:
    <h2>${_('assets')}</h2>
    ${c.b_categories_status(id="status_%s_assets" % c.libgroup.id,
                    items=c.libgroup.categories, container_id=c.libgroup.id,
                    extra_data=cat_extra_data,
                    update_listener_adder="notify.add_listener_tab").display(value=c.libgroup.categories) | n}
    <br/>
    <br/>
% endif

