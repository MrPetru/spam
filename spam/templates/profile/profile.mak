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

<%inherit file="spam.templates.master"/>

<div class="content">

    
    ${c.user.user_name} - Profile Page - created: ${str(c.user.created)[0:19]}
    <hr />

    <table>
        <tr>
            <td>Name:</td>
            <td>${c.user.display_name}</td>
            <td><div title="edit" class="lw_icon icon_edit "></td>
        </tr>
        <tr>
            <td>Email:</td>
            <td>
                % if c.user.email_address == None:
                    not specified
                % else:
                    ${c.user.email_address}
                % endif
            </td>
            <td><div title="edit" class="lw_icon icon_edit "></div></td>
        </tr>
        <tr>
            <td>Password:</td>
            <td>**********</td>
            <td>
                <a class="dialog" href="${tg.url('./user/get_change_password')}">
                    <div title="edit" class="lw_icon icon_edit "></div>
                </a>
            </td>
        </tr>
    </table>

</div>

