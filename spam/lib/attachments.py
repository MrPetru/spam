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

import sys, os, time, thread, shutil, tempfile
from tg import app_globals as G
from datetime import datetime
from hashlib import sha1
from spam.lib import preview

import logging
log = logging.getLogger(__name__)

def put(asset, filename):
    #image_types = ['.png', '.jpg', '.tif']
    
    hashable = '%s' % (datetime.now())
    target_name = sha1(hashable.encode('utf-8')).hexdigest()
    
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
    try:
        shutil.move(uploaded_file, final_file_path)
    except OSError:
        # copy with stats failed, try to do a normal copy
        shutil.copyfile(uploaded_file, final_file_path)
        os.unlink(uploaded_file)
    
    images = ['.png', '.jpg', '.tif', '.tiff']
    video = ['.mp4', '.avi', '.mov']
    docs = ['.txt', '.doc', '.odt']
    
    if (ext in images) or (ext.lower() in images):
        preview.make_attach_thumb(final_file_path, os.path.join(previews_path,target_name) + '.png')
        #final_previews_path = '/themes/default/images/attach_image.png'
        final_previews_path = os.path.join('/repo',asset.proj_id, G.ATTACHMENTS, G.PREVIEWS,
                                dirname, target_name + '.png')
    elif (ext in video) or (ext.lower() in video):
        final_previews_path = u'/themes/default/images/attach_video.png'
    elif (ext in docs) or (ext.lower() in docs):
        final_previews_path = u'/themes/default/images/attach_document.png'
    else:
        final_previews_path = u'/themes/default/images/attach_other.png'
        
    #final_previews_path = os.path.join(previews_path, target_name)
    
    #create_thumb
    #create_preview
    # save final previews
#    
#    
#    dirname, basename = os.path.split(asset.path)
#    name, ext = os.path.splitext(basename)

    return (dict(file_name=target_name + ext, file_path=os.path.join(asset.proj_id,
                            G.ATTACHMENTS, dirname, target_name + ext),
            preview_path=final_previews_path))
#            preview_path=os.path.join(asset.proj_id, G.ATTACHMENTS, G.PREVIEWS,
#                            dirname, target_name + ext)))

    
def get(proj, attach):
    """Return the file corresponding to the given attach file path."""
    
    prj_repository = os.path.join(G.REPOSITORY)
    
    target_file_name = os.path.join(prj_repository, attach.file_path)
    
    temp = tempfile.NamedTemporaryFile()
    temp.file = open(target_file_name, "r")
    
    return temp
