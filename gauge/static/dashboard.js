$(function () {

    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x -45,
            border: '1px solid #fdd',
            padding: '2px',
            opacity: 0.80,
            color: '#000',
            'background-color': '#fff'
        }).appendTo("body").fadeIn(200);
    }

    $("div.sparkline").each(function (index, elem) {

        var e = $(elem);
        var value_element = e.parent().find('p.value a');
        var timestamp_element = e.parent().find('span.timestamp');
        var original_value = value_element.html();

        var url = "/metric/" + e.data('suite') + "/" + e.data('metric');
        var json_url = url + '.json';

        var significant = e.data('significant');

        if (significant == '1'){
            json_url += "?significant";
            url += "?significant";
        }

        $.getJSON(json_url, function(response) {

            for(var i=0;i<response.data.length;i++){
                for(var y=0; y<response.data[i].data.length;y++){
                    response.data[i].data[y][0] *= 1000;
                }
            }

            var options = {
                xaxis: {mode: "time"},
                yaxis: {show: true},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["white", "yellow"],
                lines: { show: true },
                points: { show: true },
                legend: {
                    show: false
                }
            };

            $.plot(e, response.data, options);


            var previousPoint = null;

            e.bind('plothover', function(event, pos, item) {

                if (item) {
                    if (previousPoint != item.dataIndex) {
                        previousPoint = item.dataIndex;

                        $("#tooltip").remove();

                        var d = new Date(item.datapoint[0]);
                        var date_string = $.plot.formatDate(d, "%0d %b %y");
                        var value = Math.round(item.datapoint[1] * 100000000) / 100000000;
                        var label = "<strong>" + value + "</strong><br/>" + date_string;

                        showTooltip(item.pageX, item.pageY, label);

                    }
                }
                else {
                    $("#tooltip").remove();
                    previousPoint = null;
                }
            });

        });

        e.click(function() {
            window.location = url;
        });

    });
});
