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
"""build-client paster command."""

from paste.script import command
from mrapps.mrclientmaker import ClientMaker
from spam.commands import pylonsenv
pylonsenv.setup()

from spam.controllers import root as _root, category, tag as _tag
from spam.controllers import note as _note, project, scene, shot, libgroup
from spam.controllers import asset

def build_client(filename):
    """Builds a standalone client for SPAM using mrClientMaker."""
    root = _root.RootController()
    cat = category.Controller()
    tag = _tag.Controller()
    note = _note.Controller()
    proj = project.Controller()
    sc = scene.Controller()
    sh = shot.Controller()
    lib = libgroup.Controller()
    ast = asset.Controller()

    maker = ClientMaker('SPAM')

    # Root
    maker.add_call(root.upload)
    maker.add_call(root.repo)
    
    # Category
    group = 'category'
    target = '%s.json' % group
    maker.add_call(cat.get_one, group, 'get', '%s/get_one.json' % group, 'category', True)
    maker.add_call(cat.post, group, 'new', target, 'category')
    maker.add_call(cat.put, group, 'edit', target, _method='PUT')
    maker.add_call(cat.post_delete, group, 'delete', target, _method='DELETE')

    # Tag
    group = 'tag'
    target = '%s.json' % group
    maker.add_call(tag.get_one, group, 'get', '%s/get_one.json' % group, 'tag', True)
    maker.add_call(tag.post, group, 'new', target)
    maker.add_call(tag.post_delete, group, 'delete', target, _method='DELETE')
    maker.add_call(tag.remove, group, 'remove', target, _method='REMOVE')

    # Note
    group = 'note'
    target = '%s.json' % group
    maker.add_call(note.get_one, group, 'get', '%s/get_one.json' % group, 'note', True)
    maker.add_call(note.post, group, 'new', target, 'note')
    maker.add_call(note.post_delete, group, 'delete', target, _method='DELETE')
    maker.add_call(note.pin, group, 'pin', target, _method='PIN')
    maker.add_call(note.unpin, group, 'unpin', target, _method='UNPIN')

    # Project
    group = 'project'
    target = '%s.json' % group
    maker.add_call(proj.get_one, group, 'get', '%s/get_one.json' % group, 'project', True)
    maker.add_call(proj.post, group, 'new', target, 'project')
    maker.add_call(proj.put, group, 'edit', target, _method='PUT')
    maker.add_call(proj.post_delete, group, 'delete', target, _method='DELETE')
    maker.add_call(proj.post_archive, group, 'archive', target, _method='ARCHIVE')
    maker.add_call(proj.post_activate, group, 'activate', target, _method='ACTIVATE')

    # Scene
    group = 'scene'
    target = '%s.json' % group
    maker.add_call(sc.get_one, group, 'get', '%s/get_one.json' % group, 'scene', True)
    maker.add_call(sc.post, group, 'new', target, 'scene')
    maker.add_call(sc.put, group, 'edit', target, _method='PUT')
    maker.add_call(sc.post_delete, group, 'delete', target, _method='DELETE')

    # Shot
    group = 'shot'
    target = '%s.json' % group
    maker.add_call(sh.get_one, group, 'get', '%s/get_one.json' % group, 'shot', True)
    maker.add_call(sh.post, group, 'new', target, 'shot')
    maker.add_call(sh.put, group, 'edit', target, _method='PUT')
    maker.add_call(sh.post_delete, group, 'delete', target, _method='DELETE')

    # Libgroup
    group = 'libgroup'
    target = '%s.json' % group
    maker.add_call(lib.get_one, group, 'get', '%s/get_one.json' % group, 'libgroup', True)
    maker.add_call(lib.post, group, 'new', target, 'libgroup')
    maker.add_call(lib.put, group, 'edit', target, _method='PUT')
    maker.add_call(lib.post_delete, group, 'delete', target, _method='DELETE')

    # Asset
    group = 'asset'
    target = '%s.json' % group
    maker.add_call(ast.get_one, group, 'get', '%s/get_one.json' % group, 'asset', True)
    maker.add_call(ast.post, group, 'new', target, 'asset')
    maker.add_call(ast.post_delete, group, 'delete', target, _method='DELETE')
    maker.add_call(ast.checkout, group, 'checkout', target, _method='CHECKOUT')
    maker.add_call(ast.release, group, 'release', target, _method='RELEASE')
    maker.add_call(ast.post_publish, group, 'publish', target, 'version', _method='PUBLISH')
    maker.add_call(ast.post_submit, group, 'submit', target, _method='SUBMIT')
    maker.add_call(ast.post_recall, group, 'recall', target, _method='RECALL')
    maker.add_call(ast.post_sendback, group, 'sendback', target, _method='SENDBACK')
    maker.add_call(ast.post_approve, group, 'approve', target, _method='APPROVE')
    maker.add_call(ast.post_revoke, group, 'revoke', target, _method='REVOKE')
    maker.add_call(ast.download, group, 'download', target, _method='DOWNLOAD')

    output = open(filename, 'w+')
    output.write(maker.render())
    output.close()

class BuildClient(command.Command):
    """Paster command to build a standalone SPAM client."""
    max_args = 1
    min_args = 0

    usage = ""
    summary = "Build a standalone SPAM client"
    group_name = "SPAM"

    parser = command.Command.standard_parser(verbose=True)
    parser.add_option('--filename',
                      default='spam/spamclient.py',
                      help="save output in <filename>")

    def command(self):
        build_client(self.options.filename)
        print('Saved output in <%s>' % self.options.filename)
        return

