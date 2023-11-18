const barChart = (chartId, x, y) => {
    const barColors = ["blue", "purple"];
    new Chart(chartId, {
        type: "bar",
        data: {
            labels: x,
            datasets: [{
                backgroundColor: barColors,
                data: y
            }]
        },
        options: {
            legend: {
                display: false,
            },
            title: {
                legendText: ['day', 'day'],
            }
        }
    });
}