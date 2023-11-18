const lineChart = (chartId, x, y) => {
    new Chart(chartId, {
        type: "line",
        data: {
            labels: x,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,0.1)",
                data: y
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: Math.min(...y) / 2,
                        max: Math.max(...y) * 1.5,
                        beginAtZero: true,
                        callback: function (value) {
                            if (value % 1 === 0) {
                                return value;
                            }
                        }
                    }
                }],
            },
            title: {
                display: false,
            }
        }
    });
}