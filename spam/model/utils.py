# -*- coding: utf-8 -*-
#
# SPAM Spark Project & Asset Manager
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""Model utilities"""

from sqlalchemy import Table, Column, Integer, String, Unicode
from sqlalchemy.orm import mapper, relation, class_mapper, backref
from sqlalchemy.sql import desc

import logging
log = logging.getLogger(__name__)

class MappedList(list):
    """A custom list to map a collection of objects.
    
    A ``MappedList` can be filtered by an attribute of the contained objects, so
    if we have instances of the ``Box`` class::
        >>> class Box(object):
        ...     def __init__(self, size, content):
        ...             self.content = content
        ...             self.size = size
        ...     def __repr__(self):
        ...             return '<A %s box containing a %s>' % (self.size, self.content)
        ... 
    
    we can build a ``MappedList`` that filters on ``size``::
        >>> ml = MappedList('size', values=[Box('big', 'bicycle'), Box('small', 'candy')])
        >>> ml
        [<A big box containing a bicycle>, <A small box containing a candy>]
        >>> ml['big']
        [<A big box containing a bicycle>]
        >>> ml['small']
        [<A small box containing a candy>]
    
    If we specify an attribute as ``targetattr``, the returned list will contain
    this attribute extracted from the contained objects  instead of the
    objects themselves::
        >>> ml = MappedList('size', targetattr='content', values=[Box('big', 'bicycle'), Box('small', 'candy')])
        >>> ml['big']
        ['bicycle']
        >>> ml['small']
        ['candy']
    
    Since ``MappedList`` is a subclass of ``list`` it can be used as a normal list::
        >>> ml.append(Box('small', 'book'))
        >>> ml['small']
        ['candy', 'book']
        >>> ml[2]
        <A small box containing a book>
    """
    def __init__(self, keyattr, targetattr=None, values=[]):
        self._keyattr = keyattr
        self._targetattr = targetattr
        list.__init__(self, values)
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return list.__getitem__(self, key)
        else:
            result = [x for x in self if getattr(x, self._keyattr)==key]
            if self._targetattr:
                result = [getattr(x, self._targetattr) for x in result]
            return result
        
def mapped_list(keyattr, targetattr=None, values=[]):
    """Factory function for MappedList instances."""
    return lambda: MappedList(keyattr, targetattr, values)
