<div class="${w.css_class}">
        % for c in w.children:
                ${c.display() | n}
        % endfor
</div>
