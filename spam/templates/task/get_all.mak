<%inherit file="spam.templates.tab"/>

<textarea id="filtertextarea" rows="1"></textarea>

<script type="text/javascript">
    var taw = $('#filtertextarea').parent().width();
    $('#filtertextarea').width(taw);
    $('#filtertextarea').textext({
        plugins : 'tags prompt focus autocomplete',
        tagsItems : [],
        prompt : 'Add one...',
    })
    .bind({
        getSuggestions: function(e, data)
            {
                var list = [
                            % for i in c.all_filter_values:
                                ${"'%s', " % i}
                            % endfor
                            ],
                textext = $(e.target).textext()[0],
                query = (data ? data.query : '') || ''
                ;
                
            filter_personal = function(list, query) {
                    var new_val = query;
	                if (query.length > 1) {
                        if (query[0] == "+" || query[0] == "-") {
                                if (query.length > 1) {
                                    new_val = query.substring(1, query.length);
                                } else {
                                    new_val = '';
                                }
                        }
                    }
                    
		            var result = [],i, item;
                
		            for(i = 0; i < list.length; i++)
		            {
			            item = list[i];
			            if(item.toLowerCase().indexOf(new_val.toLowerCase()) == 0) {
			                switch (query[0]) {
                                case "+":
			                        result.push("+"+item);
			                        break;
                                case "-":
			                        result.push("-"+item);
			                        break;
                                default:
				                    result.push(item);
				            }
				        }
		            }

		            return result;
	            };
            $(this).trigger(
                'setSuggestions',
                { result : filter_personal(list, query) }
            );
        },
        enterKeyPress: function (e) {
            var all_assets = $('.actiondescription');
            function asset_tags(asset) {
                return $('.filtertags',asset).first().attr('value').split(',');
            }
            
            function s_tags() {
                var text_tags = $('.text-wrap > input').first().attr('value').replace(/"/g, '');
                text_tags = text_tags.substring(1,text_tags.length-1);
                return text_tags.split(',');
            }
            
            var selected_tags = s_tags();
            
            var selected_assets = new Array();


            function contain_element(container, element) {
                for (ii=0; ii<container.length; ii++) {
                    if (element == container[ii]) {
                        return true;
                    }
                }
            }


            function assethastag(asset, tag) {
                var tags = asset_tags(asset);
                return contain_element(tags, tag);
            }


            for (i=0; i < selected_tags.length; i++) {
                var tag = selected_tags[i];
                switch (tag[0]) {
                    case "+":
                        var t = tag.substring(1, tag.length);
                        // select asset from all_assets
                        for (j=0; j< all_assets.length; j++) {
                            if (assethastag(all_assets[j], t)) {
                                if (!contain_element(selected_assets, all_assets[j])) {
                                    selected_assets.push(all_assets[j]);
                                }
                            }
                                    
                        }
                        break;
                        
                    case "-":
                        // remove assets with this tag
                        var t = tag.substring(1, tag.length);
                        if (selected_assets.length > 0) {
                            for (j=0; j< selected_assets.length; j++) {
                                if (assethastag(selected_assets[j], t)) {
                                    delete selected_assets[j];
                                }
                            }
                        } else {
                            for (j=0; j< all_assets.length; j++) {
                                if (!assethastag(all_assets[j], t)) {
                                    selected_assets.push(all_assets[j]);
                                }
                            }
                        }
                        break;
                    default:
                        // asset with all this tags
                        var t = tag;
                        if (selected_assets.length > 0) {
                            for (j=0; j< selected_assets.length; j++) {
                                if (!assethastag(selected_assets[j], t)) {
                                    delete selected_assets[j];
                                }
                            }
                        } else {
                            for (j=0; j< all_assets.length; j++) {
                                if (assethastag(all_assets[j], t)) {
                                    selected_assets.push(all_assets[j]);
                                }
                            }
                        }
                }
            };
            if (selected_assets.length > 0) {
                $.each(all_assets, function (i, element) {
                    $(element).fadeOut();
                });
                $.each(selected_assets, function (i, element) {
                    $(element).fadeIn();
                });
            } else {
                if (selected_tags[0] == '') {
                    $.each(all_assets, function (i, element) {
                        $(element).fadeIn();
                    });
                } else {
                    $.each(all_assets, function (i, element) {
                        $(element).fadeOut();
                    });
                }
                
            }
            //alert('assets:'+selected_assets);
        },
    });
</script>

<table class="usertasks">
<tbody>
<tr>
<td>
    <div class="short_assets">
####        % for group in assets_groups:
####            <div id="${'toggle_%s' % group['id']}" class="toggle ${len(group)==0 and 'hidden' or ''}">
####                <div class="toggle_header title">
####                    <span class="toggle_arrow"/>
####                    <span class="toggle_title">${group['path']}</span>
####                </div>
####                <div class="toggleable">
####                    ${c.t_assets(value=group['assets'], extra_data=dict(user_id=c.user.id),
####                                id ="task_groups_%s" %group['id']).display() | n}
####                </div>
####            </div>
####        % endfor
    ${c.t_assets(value=assets, extra_data=dict(user_id=c.user.id),
                                id ="task_groups").display() | n}
    </div>
</td>
<td>
    <div class="assetdescription">
        <h2>SELECT AN ASSET</h2>
    </div>
</td>
</tr>
</tbody>
</table>
