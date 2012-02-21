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

function(data) {
    % if w.value:
        var field = '<div class="statusiconbox">';
        if (data['shots'] != []){
            maker_t = ${w.child.maker() | n};
            field += maker_t(data);
            field += '</div>';
            return field;
        };
    % else:
        return '<div class="statusiconbox"></div>'
    % endif
}

##<div>
##    ${w.child.display()}
##</div>

