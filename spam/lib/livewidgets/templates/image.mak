% if ((w.src % w.data) != "/spam") and ((w.src % w.data) != ""):
    <img src="${w.src % w.data}" class="${w.widget_class} ${w.css_class % w.data}" title="${w.help_text % w.data}"></img>
% endif
