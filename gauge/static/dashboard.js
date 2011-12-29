$(function () {

    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
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

        var url = "/metric/" + e.data('control') + "/" + e.data('experiment') + "/" + e.data('metric');

        $.getJSON(url + '.json', function(response) {

            var options = {
                xaxis: {show: false, mode: "time"},
                yaxis: {show: true},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["white", "yellow"],
                lines: { show: true },
                points: { show: true }
            };

            $.plot(e, response.data, options);


            var previousPoint = null;

            e.bind('plothover', function(event, pos, item) {

                if (item) {
                    if (previousPoint != item.dataIndex) {
                        previousPoint = item.dataIndex;

                        $("#tooltip").remove();
                        var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);

                        var d = new Date(1324740756 * 1000);
                        var label = $.plot.formatDate(d, "%y-%m-%d");

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
