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

    var e = $("#graph");
    var url = "/metric/" + e.data('suite') + "/" + e.data('metric') + ".json?days=365&detail";

    var significant = e.data('significant');

    if (significant == '1'){
        url += "&significant";
    }

    var hover = {
        show: function(x, y, message) {
            $('<div id="hover">').html(message)
                .css({top: y, left: x})
                .appendTo('body')
                .show();
        },
        hide: function() {
            $("#hover").remove();
        }
    };

    $.getJSON(url, function(response) {

        for(var i=0;i<response.data.length;i++){
            for(var y=0; y<response.data[i].data.length;y++){
                response.data[i].data[y][0] *= 1000;
            }
        }

        var options = {
            xaxis: {
                mode: "time",
                tickColor: "rgba(0,0,0,0)",
                show: true
            },
            yaxis: {min: 0, ticks: 10},
            grid: {borderWidth: 0, hoverable: true, color: "white"},
            lines: { show: true },
            points: { show: true },
            legend: {
                show: true,
                backgroundColor: 'rgba(0,0,0,1)',
                labelFormatter: function(string, series){
                    if (string.indexOf("_base") != -1){
                        string = string.replace("_base", "");
                        return string.toUpperCase() + " " + $('.control.branch').html();

                    } else if (string.indexOf("_changed") != -1){
                        string = string.replace("_changed", "");
                        return string.toUpperCase() + " " + $('.experiment.branch').html();

                    }
                    return string;
                },
                margin: [-100, 0]
            }
        };
        var plot = $.plot(e, response.data, options);

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
});
