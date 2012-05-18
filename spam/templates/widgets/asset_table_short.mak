
<table>
    <tbody>
        % for row in w.children:
            ${row.display() | n}
        % endfor
    </tbody>
</table>
