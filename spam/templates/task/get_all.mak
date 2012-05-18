<%inherit file="spam.templates.tab"/>

<div class="short_assets">
    % for cat in sorted(assets.iterkeys()):
        <div id="${'toggle_%s' % assets[cat][0].id}" class="toggle ${len(assets[cat])==0 and 'hidden' or ''}">
            <div class="toggle_header title">
                <span class="toggle_arrow"/>
                <span class="toggle_title">${cat}</span>
            </div>
            <div class="toggleable">
                ${c.t_assets(value=assets[cat]).display() | n}
            </div>
        </div>
    % endfor
</div>

<div class="assetdescription">
ASSET DESCRIPTION
</div>
