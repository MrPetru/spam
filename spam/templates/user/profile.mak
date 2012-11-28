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
## Petru Ciobanu <petrea.email@gmail.com>
##

<%inherit file="spam.templates.master"/>

<div class="content">
    
    ${_('Your Details, registered:')} ${str(c.user.created)[0:19]}
    <hr />
    <br />
    ${_('Username:')} <b>${c.user.user_name}</b>
    <br />
    ${_('Display Name:')} <b>${c.user.display_name}</b>
    <br />
    % if c.user.email_address == None:
        ${_('Email Address:')} <b> ${_('not specified')}
    % else:
        ${_('Email Address:')} <b>${c.user.email_address}
    % endif
    </b>
    <br /><br />
    
    <a class="button dialog" href="${tg.url('./%s/edit') % c.user.user_name}">${_('edit details')}</a>
   
    <a class="button dialog" href="${tg.url('./get_change_password')}">${_('change password')}</a>

</div>

