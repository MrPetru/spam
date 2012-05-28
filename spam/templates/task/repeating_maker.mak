function(data) {
    var field = '<div class="${w.css_class}">';
    $.each(data["${w.key}"], function(i, item) {
        ##alert(i + "____" + item);
        maker_t = ${w.child.maker() | n};
        field += maker_t(item);
    });
    field += '</div>';
    return field;
}
