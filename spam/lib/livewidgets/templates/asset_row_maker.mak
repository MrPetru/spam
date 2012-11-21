<%inherit file="item_layout_maker.mak"/>

path_string = data["path"].split("/");
path_string.push("from:"+data["task_sender"]);
path_string.push("to:"+data["task_receiver"]);

if (data['modified'][data['user_id']]) {
    path_string.push("modified");
};

content += '<tr class="item-' + data["id"] + ' actiondescription status ' +data["status"] + '">';
content += '<input type="hidden" class="actionurl" value="/opam/task/'+ data["proj_id"]+'/' + data["id"] +'"/>';
content += '<input type="hidden" class="filtertags" value="'+data["status"]+','+data["owner_user_name"]+','+path_string +'"/>';
    $.each(field_makers, function() {
        if (this.condition(data)) {
            var css_class = this.css_class;
            var field_maker = this.maker;
            content += '<td class="'+this.parent_css_class+'">' + field_maker(data) + '</td>';
        }
    });
content += '</tr>'
