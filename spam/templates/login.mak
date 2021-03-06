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
<script type="text/javascript">
    var formInUse = false;
    $("#loginform input").focus(function(e) {
        formInUse = true;
    });

    $(function() {
        if(!formInUse)
            $("#login_field").focus();
    });
</script>

<div id="loginform">
<form action="${tg.url('/login_handler')}" method="POST" class="loginfields">
    <h2><span>Login</span></h2>
    <input type="hidden" id="came_from" name="came_from" value="${came_from.encode('utf-8')}"></input>
    <input type="hidden" id="logins" name="__logins" value="${login_counter.encode('utf-8')}"></input>
    <label for="login">Username:</label><input type="text" id="login_field" name="login" class="text" tabindex="1"></input>
    <label for="password">Password:</label><input type="password" id="password_field" name="password" class="text" tabindex="2"></input>
    <input type="submit" id="submit" value="Login" tabindex="3"/>
</form>
</div>

