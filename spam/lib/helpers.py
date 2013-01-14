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

#from webhelpers import date, feedgenerator, html, number, misc, text

## help classes
class widget_actions():
        
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
            1, # 14, the asset was modified?
            ]
        if isinstance(asset, dict):
            return [0]*15

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
                            
        display_flags[4] = int(asset_json['checkedout'] and
                                (cur_user == asset_json['owner_id'] or cur_user in asset_json['supervisor_ids']))
        
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
        
        display_flags[12] = int((cur_user == asset_json['owner_id'] and
                                asset_json['checkedout'] and
                                not asset_json['submitted'] and
                                not asset_json['approved']) or 
                                ((cur_user in asset_json['supervisor_ids']) and 
                                asset_json['submitted']))
                                
        display_flags[13] = int((cur_user in asset_json['supervisor_ids']) or
                                (cur_user in asset_json['supervisor_ids'] and receiver == u''))
                   
        display_flags[14] = 0 # if no entries would be foud then return 0
        for m in asset.modified_entries:
            if m.user_id == cur_user:
                display_flags[14] = int(m.modified)
        
        return (display_flags)
        
