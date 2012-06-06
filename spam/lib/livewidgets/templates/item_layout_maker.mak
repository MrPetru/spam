function(data) {
    var field_makers = [];
    var path_string = "";
    var content = "";
    % for index, field in enumerate(w.children):
        field_makers.push({
             "css_class": "${field.css_class}",
             "parent_css_class": "${field.parent_css_class}",
             "condition": function(data) {return (${field.update_condition | n});},
             "maker": ${field.maker().replace('\n', '') | n},
        });
    % endfor
    ${self.body()}
    return content;
}

