<tr class="item-${w.item_id} status ${w.item_status}">
    % for c in w.children:
        <td class="${c.parent_css_class}">
            ${c.display() | n}
        </td>
    % endfor
</tr>
