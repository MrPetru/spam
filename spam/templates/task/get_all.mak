<%inherit file="spam.templates.tab"/>

<table class="usertasks">
<tbody>
<tr>
<td>
    <div class="short_assets">
        % for group in assets_groups:
            <div id="${'toggle_%s' % group['id']}" class="toggle ${len(group)==0 and 'hidden' or ''}">
                <div class="toggle_header title">
                    <span class="toggle_arrow"/>
                    <span class="toggle_title">${group['path']}</span>
                </div>
                <div class="toggleable">
                    ${c.t_assets(value=group['assets'], extra_data=dict(user_id=c.user.id),
                                id ="task_groups_%s" %group['id']).display() | n}
                </div>
            </div>
        % endfor
    </div>
</td>
<td>
    <div class="assetdescription">
        <h2>NO ASSET SELECTED </h2>
    </div>
</td>
</tr>
</tbody>
</table>
