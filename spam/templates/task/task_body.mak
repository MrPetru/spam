<div class = 'taskbody'>
% for c in w.children:
    ${c.display() | n }
% endfor

</div>