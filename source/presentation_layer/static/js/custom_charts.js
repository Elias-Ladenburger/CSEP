function getAnswerChart(chartName, getURL, type="pie") {
    jQuery.ajax({
            url: getURL,
            method: 'GET',
            success: function (data) {
                renderAnswerChart(chartName, data, type)
            }
        })
}

function renderAnswerChart(chartName, data, type="pie") {
    let chart = new CanvasJS.Chart(chartName, {
        theme: "light1", // "light1", "light2", "dark1", "dark2"
        exportEnabled: false,
        animationEnabled: false,
        title: {
            text: "Participant Answers"
        },
        data: [{
            type: type, // alternative types: "pie", "column"
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 16,
            indexLabel: "{label}",
            dataPoints: data
        }]
    });
    chart.render();
}