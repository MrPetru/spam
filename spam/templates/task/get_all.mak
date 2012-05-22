<%inherit file="spam.templates.tab"/>

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

<div class="assetdescription">
</div>
