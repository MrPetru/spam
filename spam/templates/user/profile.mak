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
    
    Profile Page - created: ${str(c.user.created)[0:19]}
    <hr />
    
    <img src="http://www.gravatar.com/avatar/2445c0701dc412883154fe6cedf09ff3?s=140&d=http%3A%2F%2Fgithub.com%2Fimages%2Fgravatars%2Fgravatar-140.png" width="120" heght="160" /> 
    <br /><br />
    Username: <b>${c.user.user_name}</b>
    <br />
    Display Name: <b>${c.user.display_name}</b>
    <br />
    % if c.user.email_address == None:
        Email Address: <b>not specified
    % else:
        Email Address: <b>${c.user.email_address}
    % endif
    </b>
    <br /><br />
    
    <a class="button dialog" href="${tg.url('./%s/edit') % c.user.user_name}">${_('edit details')}</a>
   
    <a class="button dialog" href="${tg.url('./get_change_password')}">${_('change password')}</a>

</div>

