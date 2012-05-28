function(data) {
    var field_makers = [];
    var content = "";
    % for index, field in enumerate(w.children):
        field_makers.push({
             "css_class": "${field.css_class}",
             "condition": function(data) {return (${field.update_condition | n});},
             "maker": ${field.maker().replace('\n', '') | n},
        });
    % endfor
    content += '<div class="item-' + data["id"] + ' taskcomment">';
        $.each(field_makers, function() {
            if (this.condition(data)) {
                var css_calss = this.css_class;
                var field_maker = this.maker;
                content += field_maker(data);
            }
        });
        
    content += '</div>';
    return content;
}

