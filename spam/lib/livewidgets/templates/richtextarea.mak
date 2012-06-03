
<%!
    from tg import url
%>

<script type="text/javascript" src="${url('/cleditor/jquery.cleditor.js')}"></script>
<link rel="stylesheet" type="text/css" href="${url('/cleditor/jquery.cleditor.css')}" />
    
<%namespace name="tw" module="tw2.core.mako_util"/>\
<textarea ${tw.attrs(attrs=w.attrs)}>${w.value or ''}</textarea>

<script type="text/javascript">

    $.cleditor.defaultOptions.width = 400;
    $.cleditor.defaultOptions.height = 'auto';
    if ( $("#comment").length != 0 ) {
        $("#comment").cleditor();
    } else {
        $("#description").cleditor();
    };

</script>
