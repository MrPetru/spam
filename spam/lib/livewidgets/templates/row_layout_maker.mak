<%inherit file="item_layout_maker.mak"/>
content += '<tr class="item-' + data["id"] + ' status ' +data["status"] + '">';
    $.each(field_makers, function() {
        if (this.condition(data)) {
            var css_class = this.css_class;
            var field_maker = this.maker;
            content += '<td class="'+this.parent_css_class+'">' + field_maker(data) + '</td>';
        }
    });
content += '</tr>'
