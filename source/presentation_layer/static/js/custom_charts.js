function renderAnswerChart(chartName, data, type="pie") {
    let chart = new CanvasJS.Chart(chartName, {
        theme: "light1", // "light1", "light2", "dark1", "dark2"
        exportEnabled: false,
        animationEnabled: false,
        title: {
            text: "Results"
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