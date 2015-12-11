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
"""The base Controller API."""

import tw2.core as twc
from tg import TGController, tmpl_context, config, url
from tg import request

from spam.lib import predicates
from spam.lib.widgets import ListProjects

# JQuery and plugins
# js_jquery_spamkit = twc.JSLink(link=url('/js/jquery.spamkit.js'))
# js_jquery = twc.JSLink(link=url('/js/extern/jquery-1.4.2.min.js'))
js_jquery = twc.JSLink(link=url('/js/extern/jquery-1.4.2.min.js'))
js_jquery_tools = twc.JSLink(link=url('/js/extern/jquery.tools.min.js'))
js_jquery_ui = twc.JSLink(link=url('/js/extern/jquery-ui-1.8.4.custom.min.js'))
js_jquery_jstree = twc.JSLink(link=url('/js/extern/jquery.jstree.min.js'))
js_jquery_cookies = twc.JSLink(link=url('/js/extern/jquery.cookie.js'))
js_jquery_sprintf = twc.JSLink(link=url('/js/extern/jquery.sprintf-1.0.2.js'))
js_jquery_tablesorter = twc.JSLink(link=url('/js/extern/jquery.tablesorter-2.0.3.min.js'))

# SPAM
js_spam = twc.JSLink(link=url('/js/spam.js'))

js_cleditor = twc.JSLink(link=url('/cleditor/jquery.cleditor.js'))
css_cleditor = twc.CSSLink(link=url('/cleditor/jquery.cleditor.css'))

js_textext = twc.JSLink(link=url('/js/textext.js'))

# widgets
w_startup_js = twc.Widget(
        template='mako:spam.templates.widgets.startup_js',
        resources=[js_jquery, js_jquery_ui, js_jquery_tools, js_cleditor, css_cleditor, js_textext, js_jquery_jstree,
                   js_jquery_cookies, js_jquery_sprintf, js_jquery_tablesorter, js_spam],
)
l_projects = ListProjects()


class BaseController(TGController):
    """Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.
    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        request.identity = request.environ.get('repoze.who.identity')
        tmpl_context.identity = request.identity
        return TGController.__call__(self, environ, start_response)


class SPAMBaseController(TGController):
    """ Base class for the controllers in SPAM.

    This base controller initialize and expose some items to templates.
    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        request.identity = request.environ.get('repoze.who.identity')
        tmpl_context.identity = request.identity
        if request.identity:
            tmpl_context.user = request.identity['user']

        # set the theme
        tmpl_context.theme = config.get('theme', 'default')

        # widgets
        tmpl_context.w_startup_js = w_startup_js
        tmpl_context.l_projects = l_projects

        # custom predicates
        tmpl_context.predicates = predicates

        return TGController.__call__(self, environ, start_response)
