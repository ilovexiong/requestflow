$(document).ready(function() {
    $('#render_traces_bulk').click(function() {
        $.post("/render_traces_bulk", {"traces":$("#tracetest").val()}, function(data) {
            if (data["status"] == "success") {
                treeChart(data["message"]);
            } else {
                $("#tree_chart").html(data["message"]);
            }
        });
        return false;
    });

    $('#render_live_trace').click(function() {
        $.post("/render_live_trace", {"tracking_id":$("#tracking_id").val()}, function(data) {
            if (data["status"] == "success") {
                treeChart(data["message"]);
            } else {
                $("#tree_chart").html(data["message"]);
            }
        });
        return false;
    });

    function treeChart(dataset) {
      $("#tree_chart").html("");
      var chart = d3.timeline().stack().margin({left:150, right:30, top:0, bottom:0});
      var svg = d3.select("#tree_chart").append("svg").attr("width", 500).datum(dataset).call(chart);
    }
});