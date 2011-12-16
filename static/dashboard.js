$(function () {
    $("div.sparkline").each(function (index, elem) {

        var e = $(elem);
        var value_element = e.parent().find('p.value a');
        var timestamp_element = e.parent().find('span.timestamp');
        var original_value = value_element.html();

        var url = "/metric/" + e.data('control') + "/" + e.data('experiment') + "/" + e.data('metric');

        $.getJSON(url + '.json', function(response) {

            var options = {
                xaxis: {show: false, mode: "time"},
                yaxis: {show: false, min: 0},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["white", "yellow"]
            };

            $.plot(e, response.data, options);

            e.bind('plothover', function(event, pos, item) {
                if (item) {
                    value_element.html(item.datapoint[1]);
                    var d = dddash.format_timestamp(item.datapoint[0], response.period);
                    timestamp_element.html(d);
                } else {
                    value_element.html(original_value);
                    timestamp_element.html('&nbsp;');
                }
            });
        });

        e.click(function() {
            window.location = url;
        });

    });
});