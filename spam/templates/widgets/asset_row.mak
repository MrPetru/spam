<tr class="item-${w.item_id} actiondescription status ${w.item_status}" id="${w.item_id}">
    <input type='hidden' value='${"/spam/task/%(proj_id)s/%(id)s" % w.data}'/>
    % for c in w.children:
        <td class="${c.parent_css_class}">
            ${c.display() | n}
        </td>
    % endfor
</tr>
