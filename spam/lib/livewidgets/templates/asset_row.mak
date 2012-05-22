<tr class="item-${w.item_id} ${w.widgets_class} status ${w.item_status}">
    <input type='hidden' value='${"/spam/task/%(proj_id)s/%(id)s" % w.data}'/>
    % for c in w.children:
        <td class="${c.parent_css_class}">
            ${c.display() | n}
        </td>
    % endfor
</tr>
