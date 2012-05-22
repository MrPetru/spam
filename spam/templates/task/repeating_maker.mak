function(data) {
    % if w.value:
        var field = '<div class="da_cambiare">';
        if (data['shots'] != []){
            maker_t = ${w.child.maker() | n};
            field += maker_t(data);
            field += '</div>';
            return field;
        };
    % else:
        return '<div class="da_cambiare"></div>'
    % endif
}
