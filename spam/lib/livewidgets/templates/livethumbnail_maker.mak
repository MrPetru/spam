<%namespace name="utils" file="utils.mak"/>
function(data) {
    var title = $.sprintf('${w.help_text | n}', data);
    var css_class = $.sprintf('${w.css_class | n}', data);
###    if ($.sprintf('%(thumbnail)s', data) == ''){
###    css_class = 'thumbnail_image_not_found';
###    }
###    else {
###    css_class += ' non_e_vuota_e';
###    css_class += $.sprintf('%(thumbnail)s', data);
###    }
    var field = '<div class="${w.widget_class} ' + css_class + '" title="' + title + '">';
    ${utils.render_subfields(w.children) | n}
    field += '</div>';
    return field;
}
