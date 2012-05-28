<%def name="render_subfields(subfields)">
    % for index, subfield in enumerate(subfields):
        if (${subfield.update_condition | n}) {
            var subfield_maker_${str(index)} = ${subfield.maker() | n};
            field += subfield_maker_${str(index)}(data);
            if ("${w.key}" == "current_task") {
                ##alert("ce key ${w.key}" );
            };
        };
    % endfor
</%def>

<%def name="render_subitems(subfields)">
    % for index, subfield in enumerate(subfields):
        if (${subfield.update_condition | n}) {
            var subfield_maker_${str(index)} = ${subfield.maker() | n};
            if (typeof(data["${w.key}"])=='object') {
                var newdata = data;
                $.each(data["${w.key}"], function(i, item) {
                    newdata['${w.key}_'+i] = item;
                    ##alert("${w.key}_"+i + "____" + item);
                });
                field += subfield_maker_${str(index)}(newdata);
                ##alert(field);
            } else {
                field += subfield_maker_${str(index)}(data);
            }
        }
    % endfor
</%def>
