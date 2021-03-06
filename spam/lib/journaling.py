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
"""Journaling system."""

from spam.model import session_get, Journal
from spam.lib.notifications import notify


class Journaler(object):
    """Helper to write a journal entry in the database and send a stomp
    notification.
    
    This helper saves a couple of lines of code for each journal write."""
    def add(self, user, text):
        entry = Journal(user, text)
        session_get().add(entry)
        notify.send(entry, update_type='added')

journal = Journaler()
