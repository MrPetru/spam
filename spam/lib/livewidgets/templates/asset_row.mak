<%
    a_path = "%(path)s" % w.data
    path_list = a_path.split('/')
    path_string = ''
    
    path_list.append("from:%(task_sender)s" % w.data)
    path_list.append("to:%(task_receiver)s" % w.data)
    if w.data['modified'].has_key(w.data['user_id']):
        if w.data['modified'][w.data['user_id']]:
            path_list.append('modified')
        
    for i, val in enumerate(path_list):
        if i == 0:
            path_string = val
        else:
            path_string += ',%s' % val
%>


<tr class="item-${w.item_id} ${w.widgets_class} status ${w.item_status}">
    <input type='hidden' class='actionurl' value='${"/opam/task/%(proj_id)s/%(id)s" % w.data}'/>
    <input type='hidden' class='filtertags' value='${"%(status)s,%(owner_user_name)s," % w.data}${path_string}'/>
    % for c in w.children:
        <td class="${c.parent_css_class}">
            ${c.display() | n}
        </td>
    % endfor
</tr>
