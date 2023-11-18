const pieChart = (chartId, x, y) => {
    const pieColors = ["red", "green","blue","orange","brown"];
    new Chart(chartId, {
        type: "pie",
        data: {
            labels: x,
            datasets: [{
                backgroundColor: pieColors,
                data: y
            }]
        },
        options: {
            title: {
                display: false,
            }
        }
    });
}