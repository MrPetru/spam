
    <div class="leftside">
	    <div class="assetname">${'%(name)s' % asset}</div>
	    <div class="assetinfo" >version: ${'%(current_fmtver)s' % asset} | owner: ${'%(owner_user_name)s' % asset} | last change by: ${'%(current_header)s' % asset}</div>

		    <div class="maxithumbnail"><img src="/repo/${'%(thumbnail)s' % asset}" width="320" height="180" alt="thumbnail" /></div>
		    <div class="description">
			    <span>Asset Description</span>
			    <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;${'%(description)s' % asset}</p>
		    </div>
	
        <div class="tasks">
	        <span>Task List:</span>
	        <div class="tasklist">
	        % if (task != {} ):
		        <div class="maintask">
			        <div class="taskhead">
				        <div class="sender"><strong>${'%(name)s' % task}</strong></div>
				        <div class="taskactions">${c.t_actions.display() | n}</div>
				        <div class="receiver">from: <strong>${'%(sender_name)s' % task}</strong> to: <strong>${'%(receiver_name)s' % task}</strong> date: ${'%(send_date)s' % task}</div>
				
			        </div>
			        <div class="taskbody">
				        % for n in notes:
				            <div>
				                <div class="actionbody">${'%(text)s' % n}</div>
				        		<div class="actionheader"> ${'%(action)s' % n} by ${'%(user_name)s' % n} at ${'%(created)s' % n}</div>
###				                % if n.has_key('attachment'):
###				                    <div> ${n['attachment']['file_name']} </div)
###				                % endif
				            </div>
				        % endfor
			        </div>
		        </div>
		        <div class="lasttask">
		            % if previous_task:
			            <div class="taskhead">
				            <div class="sender"><strong>${'%(name)s' % previous_task}</strong></div>
				            <div class="expand">EXPAND</div>
				            <div class="receiver">from: <strong>${'%(sender_name)s' % previous_task}</strong> to: <strong>${'%(receiver_name)s' % previous_task}</strong> date: ${'%(send_date)s' % previous_task}</div>
				
			            </div>
			        % else:
			            <div class="taskhead">
			                <strong>THERE IS NO PREVIOUS TASKS</strong>
			            </div>
                    % endif
		        </div>
		        <div class="oldtasks">
						<hr><hr><hr><hr>
		        </div>
		    % else:
		        NO TASK WAS DEFINED
		    % endif
	        </div>
        </div>
    </div>

<div class="assetactions">
${c.a_actions.display() | n}
</div>

