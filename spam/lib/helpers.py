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
"""WebHelpers used in spam."""

from webhelpers import date, feedgenerator, html, number, misc, text

## help classes
class widget_actions():
    display_flags = [
        1, # 0,  history - vedi tutta la histori
        1, # 1,  addnote - agiunge una nota
        1, # 2,  download - download last version 
        1, # 3,  checkout - prendi in carrico
        0, # 4,  release - lasciare l'incarico
        0, # 5,  publish - publicare una nuova versione
        0, # 6,  submit - manda per essere revisionato
        0, # 7,  recall - richiama dalla revisione
        0, # 8,  approve - approvare il asset
        0, # 9,  sendback - rimandare in dietro per fare le modifiche
        0, # 10, delete - cancelare l'asset
        0, # 11, revoke - anulare l'approvazione
        1, # 12, open - apri il asset tramite il servizio locale di spam
        ]
    
    user_type_flags = [
        0, # 0, admin
        0, # 1, supervisor
        0, # 2, artist
        0, # 3, owner
        ]
        
    asset_status_flags = [
        0, # 0, checked_in
        0, # 1, submited true=submited, false=(not-submited or sent back_to)
        ]
        
    def set_user_type_flags(self, asset, user):
        #reset user_type_flags
        self.user_type_flags = [0,0,0,0]

        # set flags in user_type_flags based on proprietes of user
        for admin in asset.admins:
            if admin.id == user:
                self.user_type_flags[0] = 1
        for supervisor in asset.supervisors:
            if supervisor.id == user:
                self.user_type_flags[1] = 1
        for artist in asset.artists:
            if artist.id == user:
                self.user_type_flags[2] = 1
        if asset.owner_id == user:
            self.user_type_flags[3] = 1
        #print (asset.owner_id, 'asset owner')
        # for debug        
        #print(self.user_type_flags, '[admin, supervisor, user] for user:', user)
        
    def set_asset_status_flags(self, asset):
    #    # reset asset_status_flags 
    #    self.asset_status_flags = [0,0]

        if asset.checkedout:
            self.display_flags[3] = 0
        
        if asset.checkedout and (not self.user_type_flags[1]) and (not self.user_type_flags[3]):
            self.display_flags[4] = 0
        
        if not asset.checkedout and self.user_type_flags[1]:
            self.display_flags[4] = 0
        
        if asset.submitted and self.user_type_flags[3]:
            self.display_flags[6] = 0
            self.display_flags[5] = 0
            
        if asset.submitted and not self.user_type_flags[1]:
            self.display_flags[12] = 0
            
        if not asset.submitted and self.user_type_flags[3]:
            self.display_flags[7] = 0
            
        if not asset.submitted:# and user_type_flags[1]:
            self.display_flags[9] = 0
            self.display_flags[8] = 0
            
        if asset.approved:
            self.display_flags[8] = 0
            self.display_flags[9] = 0
            self.display_flags[4] = 0
            self.display_flags[7] = 0
            self.display_flags[5] = 0
            self.display_flags[3] = 0
            
        if asset.approved and not self.user_type_flags[1]:
            self.display_flags[4] = 0
            
        if not asset.approved and not asset.submitted:
            self.display_flags[9] = 0
            
        if not asset.approved:
            self.display_flags[11] = 0
            

    def list_union(self,list_A, list_B): # A union B
        union = []
        if len(list_A)==0:
            if len(list_B)==0:
                return (union)
            else:
                return (list_B)
        elif len(list_B)==0:
            return (list_A)
        else:
            for index in range(len(list_A)):
                union.append(list_A[index] or list_B[index])
            return (union)
            
    def set_display_flags_by_user(self):
        # set display_flags based on user type
        admin_display_status=supervisor_display_status=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        artist_display_status = owner_display_status = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        if self.user_type_flags[0]:
            # set display for admin
            admin_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                0, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                0, # 8,  approuve
                0, # 9,  sendback
                1, # 10, delete
                0, # 11, revoke
                0, # 12, open
                ]
        if self.user_type_flags[1]:
            # set display for supervisor
            supervisor_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                1, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                1, # 8,  approve
                1, # 9,  sendback
                0, # 10, delete
                1, # 11, revoke
                1, # 12, open
                ]
            
        if self.user_type_flags[2]:
            # set display for user
            artist_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                1, # 3,  checkout
                0, # 4,  release
                0, # 5,  publish
                0, # 6,  submit
                0, # 7,  recall
                0, # 8,  approve
                0, # 9,  sendback
                0, # 10, delete
                0, # 11, revoke
                0, # 12, open
                ]
        if self.user_type_flags[3]:
            # set display for user
            owner_display_status = [
                1, # 0,  history
                1, # 1,  addnote
                1, # 2,  download
                0, # 3,  checkout
                1, # 4,  release
                1, # 5,  publish
                1, # 6,  submit
                1, # 7,  recall
                0, # 8,  approve
                0, # 9,  sendback
                0, # 10, delete
                0, # 11, revoke
                1, # 12, open
                ]
        #print (self.list_union(admin_display_status, self.list_union(supervisor_display_status,artist_display_status)))
        self.display_flags = self.list_union(
            admin_display_status, self.list_union(
                supervisor_display_status,self.list_union(artist_display_status, owner_display_status)))
        
    def old_main(self, asset, cur_user):
        self.set_user_type_flags(asset, cur_user)
        self.set_display_flags_by_user()
        self.set_asset_status_flags(asset)
        
        #print (asset.category_id)
        #print (asset.owner_id)
        #print (self.display_flags)
        return (self.display_flags)
        
    def main(self, asset, cur_user):
        display_flags = [
            1, # 0,  history - vedi tutta la histori
            0, # 1,  addnote - agiunge una nota
            1, # 2,  download - download last version 
            1, # 3,  checkout - prendi in carrico
            0, # 4,  release - lasciare l'incarico
            0, # 5,  publish - publicare una nuova versione
            0, # 6,  submit - manda per essere revisionato
            0, # 7,  recall - richiama dalla revisione
            0, # 8,  approve - approvare il asset
            0, # 9,  sendback - rimandare in dietro per fare le modifiche
            0, # 10, delete - cancelare l'asset
            0, # 11, revoke - anulare l'approvazione
            1, # 12, open - apri il asset tramite il servizio locale di spam
            0, # 13, new_task - crea un nuovo task
            ]
        asset_json = asset.__json__()
        if asset.current_task:
            if asset.current_task.receiver:
                receiver = asset.current_task.receiver.id
            else:
                receiver = u'TO ALL GROUP'
        else:
            receiver = u''
            
        display_flags[0] = 1
        display_flags[1] = int(not receiver == u'')
        display_flags[2] = 1
        display_flags[3] = int(not asset_json['checkedout'] and (not asset_json['approved']) and 
                            ((cur_user in asset_json['supervisor_ids']) or 
                            (cur_user in asset_json['artist_ids']) or (cur_user == receiver)))
                            
        display_flags[4] = int(asset_json['checkedout'] and ((cur_user in 
                            asset_json['artist_ids']) or (cur_user in 
                            asset_json['supervisor_ids']) or (cur_user == asset_json['owner_id'])))
        
        display_flags[5] = int(cur_user == asset_json['owner_id'] and 
                                (not asset_json['approved']) and
                                (not asset_json['submitted']))
        
        display_flags[6] = int(cur_user == asset_json['owner_id'] and
                                not asset_json['approved'] and
                                not asset_json['submitted'] and
                                receiver != u'' and (asset_json['current_ver'] > 0))
        display_flags[7] = int(cur_user == asset_json['owner_id'] and
                                not asset_json['approved'] and
                                asset_json['submitted'])
                                
        display_flags[8] = int(not asset_json['approved'] and
                                asset_json['submitted'] and
                                cur_user in asset_json['supervisor_ids'])
                                
        display_flags[9] = int(asset_json['submitted'] and
                                cur_user in asset_json['supervisor_ids'] and
                                not asset_json['approved'])
                                
        display_flags[10] = int(cur_user in asset_json['supervisor_ids'])
        
        display_flags[11] = 0
        
        display_flags[12] = int(cur_user == asset_json['owner_id'] and
                                asset_json['checkedout'] and
                                not asset_json['submitted'] and
                                not asset_json['approved'])
                                
        display_flags[13] = int((cur_user in asset_json['supervisor_ids'] and
                                asset_json['approved']) or
                                (cur_user in asset_json['supervisor_ids'] and receiver == u''))
        
        return (display_flags)
        
