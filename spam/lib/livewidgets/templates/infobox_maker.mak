<%namespace name="utils" file="utils.mak"/>
function(data) {
    var display_array = data.actions_display_status;
    if (display_array[${w.index | n}]){
        var title = $.sprintf('${w.help_text | n}', data);
        var css_class = $.sprintf('${w.css_class | n}', data);
        var field = '<div class="' + css_class + '" title="' + title + '">';
        field += '</div>';
        return field;
    }
    else {
        return '';
    };
};

