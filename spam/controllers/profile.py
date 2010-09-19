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
"""Profile Page controller"""

from tg import expose, url, tmpl_context, require
from tg.decorators import paginate
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from sqlalchemy import desc
from spam.lib.base import SPAMBaseController
from spam.model import session_get, Journal
from spam.lib.widgets import TableJournal
from repoze.what.predicates import in_group, not_anonymous
from tg.controllers import RestController

import logging
log = logging.getLogger(__name__)

class Controller(RestController):
    """Controller for the profile page"""
    
    @require(not_anonymous())
    @expose('json')
    @expose('spam.templates.profile.profile')
    def default(self):
        """Return a `full` page with a paginated table of journal entries."""
        
        return dict(page="%s's profile" % tmpl_context.user.user_name,
                                                    sidebar=('user', 'profile'))
