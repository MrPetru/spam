
##<div class="category_container">
##    <div id="toggle_%(cat.type)">
##        <div class="toggle_header"></div>
##        <div class="toggleable"></div>
##    </div>
##</div>


<div id="${'container_%s' % w.parent_container_id}" class="${'update_on_%s' % w.update_on_topic}">
    % for c in w.children:
        ${c.display() | n }
    % endfor
</div>
