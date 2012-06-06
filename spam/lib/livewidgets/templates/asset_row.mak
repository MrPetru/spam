<%
    a_path = "%(path)s" % w.data
    path_list = a_path.split('/')
    path_string = ''
    for i, val in enumerate(path_list):
        if i == 0:
            path_string = val
        else:
            path_string += ',%s' % val
%>


<tr class="item-${w.item_id} ${w.widgets_class} status ${w.item_status}">
    <input type='hidden' class='actionurl' value='${"/spam/task/%(proj_id)s/%(id)s" % w.data}'/>
    <input type='hidden' class='filtertags' value='${"%(status)s,%(owner_user_name)s," % w.data}${path_string}'/>
    % for c in w.children:
        <td class="${c.parent_css_class}">
            ${c.display() | n}
        </td>
    % endfor
</tr>
