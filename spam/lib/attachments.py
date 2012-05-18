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

"""Preview and thumbnailing module."""

import sys, os, time, thread, shutil
from tg import app_globals as G

import logging
log = logging.getLogger(__name__)

def put(asset, filename, target_name):
    #image_types = ['.png', '.jpg', '.tif']
    
    uploaded_file = os.path.join(G.UPLOAD, filename)
    name, ext = os.path.splitext(filename)
    repo_path = os.path.join(G.REPOSITORY, asset.proj_id)
    
    dirname, basename = os.path.split(asset.path)
    final_dir_path = os.path.join(G.REPOSITORY, asset.proj_id, G.ATTACHMENTS, dirname)

    if not os.path.exists(final_dir_path):
        os.makedirs(final_dir_path)
    
    previews_path = os.path.join(G.REPOSITORY, asset.proj_id, G.ATTACHMENTS, G.PREVIEWS, dirname)
    if not os.path.exists(previews_path):
        os.makedirs(previews_path)
        
    final_file_path = os.path.join(final_dir_path, target_name + ext)
    shutil.move(uploaded_file, final_file_path)
    
    final_previews_path = os.path.join(previews_path, target_name)
    #create_thumb
    #create_preview
    # save final previews
#    
#    
#    dirname, basename = os.path.split(asset.path)
#    name, ext = os.path.splitext(basename)

    return (dict(file_name=target_name + ext, file_path=os.path.join(G.ATTACHMENTS, dirname, target_name + ext),
            preview_path=os.path.join(G.ATTACHMENTS, G.PREVIEWS, dirname, target_name + ext)))  


def get(asset, name):
    pass
