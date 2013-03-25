/***********************************************************************
 * One time setup
 **********************************************************************/
function gras_chart_factory_setup(point)
{
    var id = $('gras_stats:first', point).attr('id');
    $('#top_name').append(' - ' + id);
    $('block', point).each(function(index, block)
    {
        var id = $(block).attr('id');
        var container = $('#chart_designer_blocks');
        var div = $('<div />');
        $(div).append('<label>' + id + '</label>');
        var input = $('<input />').attr({
            type: 'checkbox',
            name: id
        });
        input.attr('checked', false);
        $(div).append(input);
        $(container).append(div);
    });
}

/***********************************************************************
 * chart factory dispatcher
 **********************************************************************/
function gras_chart_factory_dispatcher(registry)
{
    //get a list of the selected blocks
    var selected_blocks = new Array();
    $.each($('#chart_designer_blocks input'), function(index, input)
    {
        var input = $(input);
        if (input.is(':checked'))
        {
            selected_blocks.push(input.attr('name'));
        }
    });

    //get the type of chart to create
    var chart_type = $('#chart_type_selector').val();

    //create containers
    var chart_box = $('<table />').attr({class:'chart_container'});
    var tr = $('<tr />');
    var td = $('<td />');
    tr.append(td);

    //call into the factory
    try
    {
        var chart = new registry.chart_factories[chart_type]({
            block_ids:selected_blocks,
            panel:td.get(0),
        });
    }
    catch(err)
    {
        return;
    }

    //setup the title
    var tr_title = $('<tr />');
    var th_title = $('<th />');
    tr_title.append(th_title);
    th_title.text(chart.title);

    //register the chart
    registry.active_charts.push(chart);
    $('#charts_panel').append(chart_box);

    //close button
    var close_div = $('<div/>').attr({class:'chart_designer_block_close'});
    var close_href = $('<a />').attr({href:'#', class:"ui-dialog-titlebar-close ui-corner-all", role:"button"});
    var close_span = $('<span />').attr({class:"ui-icon ui-icon-closethick"}).text('close');
    close_div.append(close_href);
    close_href.append(close_span);
    th_title.append(close_div);
    $(close_href).click(function()
    {
        var index = $.inArray(chart, registry.active_charts);
        registry.active_charts.splice(index, 1);
        chart_box.remove();
    });

    //finish gui building
    chart_box.append(tr_title);
    chart_box.append(tr);
}

/***********************************************************************
 * chart factory init
 **********************************************************************/
function gras_chart_factory_init(registry)
{
    //install callback for chart factory
    $('#chart_factory_button').click(function()
    {
        gras_chart_factory_dispatcher(registry);
    });

    //list of all known chart types
    var chart_options = [
        {key:'overhead_compare', name:'Overhead Compare', factory:GrasChartOverheadCompare},
        {key:'overall_throughput', name:'Overall Throughput', factory:GrasChartOverallThroughput},
        {key:'handler_breakdown', name:'Handler Breakdown', factory:GrasChartHandlerBreakdown},
    ];

    //init the chart selection input
    registry.chart_factories = new Array();
    $.each(chart_options, function(index, options)
    {
        registry.chart_factories[options.key] = options.factory;
        var option = $('<option />').attr({value: options.key});
        option.text(options.name);
        $('#chart_type_selector').append(option);
    });

    //init overall config gui element for rate
    var overall_rate = $('#chart_update_rate');
    overall_rate.val(registry.overall_rate);
    overall_rate.change(function()
    {
        registry.overall_rate = overall_rate.val();
    });

    //init overall config gui element for activity
    registry.overall_active = true;
    var overall_active = $('#chart_active_state');
    overall_active.attr('checked', registry.overall_active);
    overall_active.change(function()
    {
        registry.overall_active = overall_active.is(':checked');
        if (registry.overall_active) gras_query_stats(registry);
        else window.clearInterval(registry.timeout_handle);
    });
}
