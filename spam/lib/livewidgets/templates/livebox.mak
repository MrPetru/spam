<%inherit file="livecontainer.mak"/>

##<%
##    from spam.lib.jsonify import encode as json_encode
##    sort_list = []
##    sort_headers = {}
##    for index, field in enumerate(fields):
##        if not field.sortable:
##            sort_headers[index] = dict(sorter=False)
##        if field.sort_default:
##            direction = field.sort_direction=='desc' and 1 or 0
##            sort_list.append([index, direction])
##%>

<script type="text/javascript">
##    $(function() {
##        $("#${w.compound_id}").tablesorter({widgets: [${zebra and '"zebra"' or ''}],
##                                 headers: ${json_encode(sort_headers)}
##                                });
##        % if sort_list and items:
##            $("#${w.compound_id}").trigger("sorton", [${json_encode(sort_list)}]);
##        % endif
##    });
</script>

##<div>
    % for row in w.children:
        ${row.display() | n}
    % endfor
##</div>

