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
"""
Project data model.

This is where the model for the project structure is defined.
"""

import os.path
from datetime import datetime
from hashlib import sha1

from sqlalchemy import Table, ForeignKey, Column, UniqueConstraint
from sqlalchemy import ForeignKeyConstraint, and_, desc
from sqlalchemy.types import Unicode, UnicodeText, Integer, DateTime, Boolean
from sqlalchemy.types import String
from sqlalchemy.orm import relation, synonym, backref

from tg import app_globals as G
from spam.model import DeclarativeBase, metadata
from spam.model import migraterepo_get_version, db_get_version
from spam.model import db_upgrade, db_downgrade
from spam.model.utils import mapped_list, compute_status, add_container_props
from spam.model.auth import User
from spam.model.misc import Taggable, Annotable

import logging
log = logging.getLogger(__name__)


############################################################
# Association tables
############################################################

# Association table for the many-to-many relationship projects-admins.
projects_admins_table = Table('__projects_admins', metadata,
    Column('project_id', Unicode(10), ForeignKey('projects.id',
                                    onupdate="CASCADE", ondelete="CASCADE")),
    Column('user_id', Unicode(40), ForeignKey('users.user_id',
                                    onupdate="CASCADE", ondelete="CASCADE")),
)


############################################################
# Project
############################################################
class Project(DeclarativeBase):
    """Project definition."""
    __tablename__ = 'projects'
    
    # Columns
    id = Column(Unicode(10), primary_key=True)
    name = Column(Unicode(40), unique=True)
    description = Column(Unicode)
    modified = Column(DateTime, default=datetime.now)
    archived = Column(Boolean, default=False)
    
    # Relations
    admins = relation('User', secondary=projects_admins_table,
                                                    backref='projects_as_admin')
    
    # Properties
    @property
    def users(self):
        return (set([s.user for s in self.supervisors]) |
                set([a.user for a in self.artists]) |
                set(self.admins))
    
    @property
    def user_ids(self):
        return [u.user_id for u in self.users]

    @property
    def admin_ids(self):
        return [u.user_id for u in self.admins]

    @property
    def schema_is_uptodate(self):
        proj_version = db_get_version(self.id)
        repo_version = migraterepo_get_version()
        return proj_version==repo_version
    
    @property
    def schema_version(self):
        return db_get_version(self.id)
    
    # Methods
    def touch(self):
        self.modified = datetime.now()
    
    def schema_upgrade(self, version=None):
        db_upgrade(self.id, version)
    
    def schema_downgrade(self, version):
        db_downgrade(self.id, version)
    
    # Special methods
    def __init__(self, id, name=None, description=None):
        self.id = id
        self.name = name or id
        self.description = description

    def __repr__(self):
        return '<Project: %s (%s)>' % (self.id, self.name)
    
    def __json__(self):
        return dict(id=self.id,
                    name=self.name,
                    description=self.description,
                    modified=self.modified.strftime('%Y/%m/%d %H:%M'),
                    archived=self.archived,
                    schema_is_uptodate=self.schema_is_uptodate,
                    admin_ids=self.admin_ids,
                    user_ids=self.user_ids,
                   )


############################################################
# Containers
############################################################
class AssetContainer(DeclarativeBase):
    """Association class for object containers"""
    __tablename__ = 'asset_containers'
        
    # Columns
    id = Column(String(40), primary_key=True)
    association_type = Column(Unicode(50))

    # Properties
    @property
    def owner(self):
        return getattr(self, 'owner_%s' % self.association_type)

    @property
    def categories(self):
        categories = []
        for asset in self.assets:
            if asset.category not in categories:
                categories.append(asset.category)
        
        for cat in categories:
            cat.status = compute_status(self.assets[cat])
        
        categories.sort(cmp=lambda x, y: cmp(x.ordering, y.ordering))
        return categories
    
    @property
    def thumbnail(self):
        categories = self.categories
        for i in range(len(categories)):
            cat = categories.pop()
            for asset in self.assets[cat]:
                if asset.has_preview:
                    return asset.thumbnail
        return ''
    
    @property
    def has_preview(self):
        if not self.thumbnail:
            return False
        return os.path.exists(os.path.join(G.REPOSITORY, self.thumbnail))
    
    # Special methods
    def __init__(self, id, association_type):
        self.id = id
        self.association_type = association_type

    def __repr__(self):
        return '<AssetContainer: %s (%s)>' % (self.id, self.association_type)


class Scene(DeclarativeBase):
    """
    The scene container.
    
    This represents a "film scene" that acts as a container for Shot objects.
    """
    __tablename__ = "scenes"
    __table_args__ = (UniqueConstraint('proj_id', 'name'),
                      ForeignKeyConstraint(['id'], ['taggables.id']),
                      ForeignKeyConstraint(['id'], ['annotables.id']),
                      {})

    # Columns
    id = Column(String(40), primary_key=True)
    proj_id = Column(Unicode(10), ForeignKey('projects.id'))
    name = Column(Unicode(15))
    description = Column(UnicodeText)

    # Relations
    project = relation('Project', viewonly=True,
                       backref=backref('scenes', viewonly=True, order_by=name)
                      )
    
    taggable = relation(Taggable,
                            backref=backref('tagged_scene', uselist=False))
    
    annotable = relation(Annotable,
                            backref=backref('annotated_scene', uselist=False))
    
    # Properties
    @property
    def path(self):
        return os.path.join(G.SCENES, self.name)
    
    @property
    def thumbnail(self):
        for sh in self.shots:
            if sh.has_tags(['key']) and sh.has_preview:
                return sh.thumbnail
        return ''
    
    @property
    def has_preview(self):
        if not self.thumbnail:
            return False
        return os.path.exists(os.path.join(G.REPOSITORY, self.thumbnail))
    
    @property
    def tags(self):
        return self.taggable.tags
    
    @property
    def notes(self):
        return self.annotable.notes
    
    @property
    def status(self):
        return compute_status(self.shots)

    @property
    def key_shots(self):
        return [sh for sh in self.shots if sh.has_tags(['key'])]
    
    # Methods
    def has_tags(self, tag_ids):
        return self.taggable.has_tags(tag_ids)
    
    # Special methods
    def __init__(self, proj, name, description=None):
        self.proj_id = proj
        self.name = name
        self.id = sha1('%s-%s' % (self.proj_id, self.name)).hexdigest()
        self.description = description
        self.taggable = Taggable(self.id, u'scene')
        self.annotable = Annotable(self.id, u'scene')

    def __repr__(self):
        return '<Scene: %s (%s)>' % (self.id, self.path)

    def __json__(self):
        return dict(id=self.id,
                    proj_id=self.proj_id,
                    name=self.name,
                    description=self.description,
                    status=self.status,
                    shots=self.shots,
                    thumbnail=self.thumbnail,
                    has_preview=self.has_preview,
                   )


class Shot(DeclarativeBase):
    """
    The shot container.

    This represents a "film shot" that acts as a container for Asset objects.
    """
    __tablename__ = "shots"
    __table_args__ = (UniqueConstraint('parent_id', 'name'),
                      ForeignKeyConstraint(['id'], ['asset_containers.id']),
                      ForeignKeyConstraint(['id'], ['taggables.id']),
                      ForeignKeyConstraint(['id'], ['annotables.id']),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    parent_id = Column(String(40), ForeignKey('scenes.id'))
    name = Column(Unicode(15))
    description = Column(UnicodeText)
    location = Column(Unicode(255))
    action = Column(UnicodeText)
    frames = Column(Integer)
    handle_in = Column(Integer)
    handle_out = Column(Integer)
    
    # Relations
    parent = relation(Scene,
                        backref=backref('shots', order_by=name, lazy=False))
    
    container = relation(AssetContainer,
                            backref=backref('owner_shot', uselist=False))
    
    taggable = relation(Taggable, backref=backref('tagged_shot', uselist=False))
    
    annotable = relation(Annotable,
                            backref=backref('annotated_shot', uselist=False))
    
    # Properties
    @property
    def project(self):
        return self.parent.project
    
    @property
    def proj_id(self):
        return self.parent.proj_id
    
    @property
    def path(self):
        return os.path.join(self.parent.path, self.name)
    
    @property
    def parent_name(self):
        return self.parent.name
    
    @property
    def tags(self):
        return self.taggable.tags
    
    @property
    def notes(self):
        return self.annotable.notes
    
    @property
    def status(self):
        return compute_status(self.assets)

    # Methods
    def has_tags(self, tag_ids):
        return self.taggable.has_tags(tag_ids)
    
    # Special methods
    def __init__(self, parent, name, description=None, action=None,
                       location=None, frames=0, handle_in=0, handle_out=0):
        self.parent = parent
        self.name = name
        self.description = description
        self.location = location
        self.frames = frames
        self.handle_in = handle_in
        self.handle_out = handle_out
        self.action = action
        hashable = '%s-%s' % (parent.id, self.name)
        log.debug('Shot.__init__: %s' % hashable)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()
        self.container = AssetContainer(self.id, u'shot')
        self.taggable = Taggable(self.id, u'shot')
        self.annotable = Annotable(self.id, u'shot')

    def __repr__(self):
        return '<Shot: %s (%s)>' % (self.id, self.path)

    def __json__(self):
        return dict(id=self.id,
                    proj_id=self.proj_id,
                    parent_id=self.parent_id,
                    parent_name=self.parent_name,
                    name=self.name,
                    description=self.description,
                    location=self.location,
                    action=self.action,
                    frames=self.frames,
                    handle_in=self.handle_in,
                    handle_out=self.handle_out,
                    status=self.status,
                    categories=self.categories,
                    thumbnail=self.thumbnail,
                    has_preview=self.has_preview,
                    container_type=self.container.association_type,
                   )

add_container_props(Shot)

class Libgroup(DeclarativeBase):
    """Library group"""
    __tablename__ = "libgroups"
    __table_args__ = (UniqueConstraint('parent_id', 'name'),
                      ForeignKeyConstraint(['id'], ['asset_containers.id']),
                      ForeignKeyConstraint(['id'], ['taggables.id']),
                      ForeignKeyConstraint(['id'], ['annotables.id']),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    proj_id = Column(Unicode(10), ForeignKey('projects.id'))
    parent_id = Column(String(40), ForeignKey('libgroups.id'))
    name = Column(Unicode(40))
    description = Column(UnicodeText)
    
    # Relations
    project = relation('Project',  backref=backref('libgroups', primaryjoin=
        'and_(Project.id==Libgroup.proj_id, Libgroup.parent_id==None)',
        viewonly=True, order_by=name))
    
    subgroups = relation('Libgroup', primaryjoin=parent_id==id,
                             foreign_keys=[parent_id], lazy=False, join_depth=5,
                             backref=backref('parent', remote_side=[id]))
    
    container = relation(AssetContainer, backref=backref('owner_libgroup',
                                                                uselist=False))
    
    taggable = relation(Taggable, backref=backref('tagged_libgroup',
                                                                uselist=False))
    
    annotable = relation(Annotable, backref=backref('annotated_libgroup',
                                                                uselist=False))
    
    # Properties
    @property
    def path(self):
        if self.parent_id:
            path = self.parent.path
        else:
            path = G.LIBRARY
        path = os.path.join(path, self.name)
        return path
    
    @property
    def tags(self):
        return self.taggable.tags
    
    @property
    def notes(self):
        return self.annotable.notes
    
    @property
    def status(self):
        subgroups_status = compute_status(self.subgroups)
        assets_status = compute_status(self.assets)
        return compute_status((subgroups_status, assets_status))
            
    # Methods
    def has_tags(self, tag_ids):
        return self.taggable.has_tags(tag_ids)
    
    # Special methods
    def __init__(self, proj, name, parent=None, description=None):
        self.proj_id = proj
        self.name = name
        if parent: self.parent_id = parent.id
        self.description = description
        hashable = '%s-%s' % (self.parent_id, self.name)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()
        self.container = AssetContainer(self.id, u'libgroup')
        self.taggable = Taggable(self.id, u'libgroup')
        self.annotable = Annotable(self.id, u'libgroup')

    def __repr__(self):
        return '<Libgroup: %s (%s)>' % (self.id, self.path)

    def __json__(self):
        return dict(id=self.id,
                    proj_id=self.proj_id,
                    parent_id=self.parent_id,
                    name=self.name,
                    description=self.description,
                    subgroups=self.subgroups,
                    status=self.status,
                    categories=self.categories,
                    thumbnail=self.thumbnail,
                    has_preview=self.has_preview,
                    container_type=self.container.association_type,
                   )

add_container_props(Libgroup)

############################################################
# Categories
############################################################
class Category(DeclarativeBase):
    """Asset category"""
    __tablename__ = "categories"
    
    # Columns
    id = Column(Unicode(40), primary_key=True)
    ordering = Column(Integer)
    naming_convention = Column(Unicode(255))
    name = synonym('id')
    
    # Special methods
    def __init__(self, id, ordering=0, naming_convention=''):
        self.id = id
        self.ordering = ordering
        self.naming_convention = naming_convention

    def __repr__(self):
        return '<Category: %s (%s)>' % (self.id, self.ordering)
    
    def __json__(self):
        return dict(id=self.id,
                    ordering=self.ordering,
                    naming_convention=self.naming_convention,
                    status=hasattr(self, 'status') and self.status or None,
                    name=self.name,
                   )


class Supervisor(DeclarativeBase):
    """Category supervisor"""
    __tablename__ = "supervisors"
    __table_args__ = (UniqueConstraint('proj_id', 'category_id', 'user_id'),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    proj_id = Column(Unicode(10), ForeignKey('projects.id'))
    category_id = Column(Unicode(40), ForeignKey('categories.id'))
    user_id = Column(Unicode(40), ForeignKey('users.user_id'))

    # Relations
    project = relation('Project', backref=backref('supervisors',
                collection_class=mapped_list('category', targetattr='user')))

    category = relation('Category', backref=backref('supervisors',
                collection_class=mapped_list('project', targetattr='user')))

    user = relation('User', backref='_supervisor_for')
    
    # Special methods
    def __init__(self, proj, category, user):
        self.proj_id = proj
        self.category = category
        self.user = user
        hashable = '%s-%s-%s' % (proj, category.id, user.user_id)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<Supervisor: (%s) "%s" %s>' % (self.proj_id, self.category.id,
                                                            self.user.user_name)

    def __json__(self):
        return dict(id=self.id,
                    proj_id=self.proj_id,
                    category_id=self.category_id,
                    user_id=self.user_id,
                   )


class Artist(DeclarativeBase):
    """Category artist"""
    __tablename__ = "artists"
    __table_args__ = (UniqueConstraint('proj_id', 'category_id', 'user_id'),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    proj_id = Column(Unicode(10), ForeignKey('projects.id'))
    category_id = Column(Unicode(40), ForeignKey('categories.id'))
    user_id = Column(Unicode(40), ForeignKey('users.user_id'))

    # Relations
    project = relation('Project', backref=backref('artists',
                collection_class=mapped_list('category', targetattr='user')))

    category = relation('Category', backref=backref('artists',
                collection_class=mapped_list('project', targetattr='user')))

    user = relation('User', backref='_artist_for')
    
    # Special methods
    def __init__(self, proj, category, user):
        self.proj_id = proj
        self.category = category
        self.user = user
        hashable = '%s-%s-%s' % (proj, category.id, user.user_id)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<Artist: (%s) "%s" %s>' % (self.proj_id, self.category.id,
                                                            self.user.user_name)

    def __json__(self):
        return dict(id=self.id,
                    proj_id=self.proj_id,
                    category_id=self.category_id,
                    user_id=self.user_id,
                   )

############################################################
# Assets
############################################################
class Asset(DeclarativeBase):
    """Asset"""
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint('parent_id', 'category_id', 'name'),
                      ForeignKeyConstraint(['id'], ['taggables.id']),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    name = Column(Unicode(50))
    parent_id = Column(String(40), ForeignKey('asset_containers.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    checkedout = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    submitted = Column(Boolean, default=False)
    submitter_id = Column(Integer, ForeignKey('users.user_id'))
    submitted_date =  Column(DateTime)
    approved = Column(Boolean, default=False)
    approver_id = Column(Integer, ForeignKey('users.user_id'))
    approved_date =  Column(DateTime)

    # Relations
    category = relation('Category', backref=backref('assets'))
    
    owner = relation('User', primaryjoin=owner_id==User.user_id,
                                        backref=backref('checkedout_assets'))

    parent = relation('AssetContainer', backref=backref('assets',
                                    collection_class=mapped_list('category')))

    taggable = relation(Taggable, backref='tagged_asset')
    
    submitted_by = relation('User', primaryjoin=submitter_id==User.user_id,
                                        backref=backref('submitted_assets'))
    
    approved_by = relation('User', primaryjoin=approver_id==User.user_id,
                                        backref=backref('approved_assets'))

    # Properties
    @property
    def proj_id(self):
        return self.parent.owner.project.id
    
    @property
    def project(self):
        return self.parent.owner.project
    
    @property
    def path(self):
        path = os.path.join(self.parent.owner.path, self.category.id)
        if self.is_sequence:
            name, ext = os.path.splitext(self.name)
            dirname = name.rstrip('.#')
            path = os.path.join(path, dirname)
        return os.path.join(path, self.name)
    
    @property
    def thumbnail(self):
        for ver in self.versions:
            if ver.has_preview:
                return ver.thumbnail
        return None
    
    @property
    def has_preview(self):
        if not self.thumbnail:
            return False
        return os.path.exists(os.path.join(G.REPOSITORY, self.thumbnail))
    
    @property
    def current(self):
        return self.versions[0]
    
    @property
    def is_sequence(self):
        return G.pattern_seq.match(self.name) and True or False
    
    @property
    def tags(self):
        return self.taggable.tags
    
    @property
    def status(self):
        if self.approved:
            return 'approved'
        elif self.submitted:
            return 'submitted'
        elif self.checkedout:
            return 'wip'
        elif self.current.ver == 0:
            return 'new'
        else:
            return 'idle'
    
    @property
    def supervisors(self):
        return (set(self.project.supervisors[self.category]) |
                set(self.project.admins))
    
    @property
    def artists(self):
        return (set(self.project.artists[self.category]) |
                set(self.project.admins))
    
    # Methods
    def has_tags(self, tag_ids):
        return self.taggable.has_tags(tag_ids)
    
    def checkout(self, user):
        self.checkedout = True
        self.owner = user

    def release(self):
        self.checkedout = False
        self.owner = None

    def submit(self, user):
        self.submitted = True
        self.submitted_by = user
        self.submitted_date = datetime.now()
    
    def recall(self, user):
        self.submitted = False
        self.submitted_by = None
        self.submitted_date = None
    
    def sendback(self, user):
        self.submitted = False
        self.submitted_by = None
        self.submitted_date = None
    
    def approve(self, user):
        self.approved = True
        self.approved_by = user
        self.approved_date = datetime.now()
    
    def revoke(self, user):
        self.approved = False
        self.approved_by = None
        self.approved_date = None
        self.submitted = False
        self.submitted_by = None
        self.submitted_date = None
    
    # Special methods
    def __init__(self, parent, category, name, user):
        self.parent = parent
        self.category = category
        self.name = name
        hashable = '%s-%s-%s' % (parent.id, category.id, name)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()
        self.taggable = Taggable(self.id, u'asset')
        
        #create version zero
        AssetVersion(self, 0, user, '')
    
    def __repr__(self):
        return '<Asset: %s (%s)>' % (self.id, self.path)

    def __json__(self):
        return dict(id=self.id,
                    name=self.name,
                    proj_id=self.proj_id,
                    project=self.project,
                    parent_id=self.parent_id,
                    parent=self.parent.owner,
                    category=self.category,
                    status=self.status,
                    checkedout=self.checkedout,
                    submitted=self.submitted,
                    approved=self.approved,
                    owner=self.owner,
                    owner_id=self.owner and self.owner.user_id or None,
                    owner_user_name=self.owner and self.owner.user_name or None,
                    owner_display_name=(self.owner and self.owner.display_name
                                                                    or None),
                    path=self.path,
                    current=self.current,
                    current_id=self.current.id,
                    current_ver=self.current.ver,
                    current_fmtver=self.current.fmtver,
                    current_header=(self.current.notes and
                                        self.current.notes[0].header or ''),
                    current_summary=(self.current.notes and
                                        self.current.notes[0].summary or ''),
                    is_sequence=self.is_sequence,
                    thumbnail=self.thumbnail,
                    has_preview=self.has_preview,
                    supervisor_ids=[u.user_id for u in self.supervisors],
                    artist_ids=[u.user_id for u in self.artists],
                    #'repopath': self.repopath,
                    #'basedir': self.basedir,
                    #'repobasedir': self.repobasedir,
                    #'preview_small_repopath': self.preview_small_repopath,
                    #'preview_large_repopath': self.preview_large_repopath,
                    #'flow': self.flow,
                    #'waiting_for_approval': self.waiting_for_approval,
                   )


class AssetVersion(DeclarativeBase):
    """Asset version"""
    __tablename__ = "asset_versions"
    __table_args__ = (UniqueConstraint('asset_id', 'ver'),
                      ForeignKeyConstraint(['id'], ['annotables.id']),
                      {})
    
    # Columns
    id = Column(String(40), primary_key=True)
    asset_id = Column(String(40), ForeignKey('assets.id'))
    ver = Column(Integer)
    repoid = Column(String(50))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    # Relations
    asset = relation('Asset', backref=backref('versions', order_by=desc(ver),
                                         cascade="all, delete, delete-orphan"))
    
    user = relation('User')
    
    annotable = relation(Annotable, backref=backref('annotated_asset_version',
                                                                uselist=False))
    
    # Properties
    @property
    def project(self):
        return self.asset.project
    
    @property
    def path(self):
        if self.asset:
            base, ext = os.path.splitext(self.asset.path)
            return '%s_v%03d%s' % (base, self.ver, ext)
        return None
    
    @property
    def fmtver(self):
        return 'v%03d' % self.ver
    
    @property
    def notes(self):
        return self.annotable.notes
    
    @property
    def thumbnail(self):
        if self.asset:
            name, ext = os.path.splitext(self.asset.name)
            name = name.replace('.#', '')
            name = '%s_v%03d-thumb.png' % (name, self.ver)
            return os.path.join(self.asset.proj_id, G.PREVIEWS,
                    self.asset.parent.owner.path, self.asset.category.id, name)
        return None
    
    @property
    def has_preview(self):
        if not self.thumbnail:
            return False
        return os.path.exists(os.path.join(G.REPOSITORY, self.thumbnail))
    
    # Special methods
    def __init__(self, asset, ver, user, repoid, has_preview=False,
                                                            preview_ext=None):
        self.asset = asset
        self.ver = ver
        self.user = user
        self.repoid = repoid
        #self.has_preview = has_preview
        #self.preview_ext = preview_ext
        hashable = '%s-%s' % (asset.id, ver)
        self.id = sha1(hashable.encode('utf-8')).hexdigest()
        self.annotable = Annotable(self.id, u'asset_version')

    def __repr__(self):
        return '<AssetVersion: %s v%03d (%s)>' % (self.asset_id, self.ver,
                                                                self.asset.path)

    def __json__(self):
        return dict(id=self.id,
                    asset_id=self.asset_id,
                    ver=self.ver,
                    fmtver=self.fmtver,
                    path=self.path,
                    thumbnail=self.thumbnail,
                    has_preview=self.has_preview,
                    #'preview_small_repopath': self.preview_small_repopath,
                    #'preview_large_repopath': self.preview_large_repopath,
                    #'strftime': self.strftime,
                   )

