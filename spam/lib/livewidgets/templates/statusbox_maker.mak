###function(data, id) {
###    var field = '<div class="statusiconbox">';
###    
###    $.each(field_makers, function() {
###        if (this.condition(data)) {
###            var css_class = this.css_class;
###            var field_maker = this.maker;
###            field += '<div>' + field_maker(data) + '</div>';
###        }
###    });
###    return field;
###};


<%namespace name="utils" file="utils.mak"/>

function(data) {
    
        var field = '<div >';
        ${utils.render_subfields(w.children) | n}
        field += '</div>';
        return field;
        
}
