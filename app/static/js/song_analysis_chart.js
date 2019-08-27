function createChart(labels, initialData) {
    // Setting up data
    var chartData = {
        labels: labels,
        datasets: [{
            label: 'stat',
            backgroundColor: 'rgba(30, 215, 96, 0.2)',
            borderColor: 'rgb(30, 215, 96)',
            pointBackgroundColor: 'rgb(30, 215, 96)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(30, 215, 96)',
            data: initialData
        }]
    }
    // Creating Chart
    var ctx = document.getElementById('chart').getContext('2d');
    window.myBar = new Chart(ctx, {
        type: 'radar',
        data: chartData,
        options: {
            responsive: false,
            title: {
                display: false,
                text: 'Song Statistics',
                fontColor: 'rgba(255, 255, 255, 0.7)'
            },
            legend: {
                display: false
            },
            scale: {
                ticks: {
                    min: 0,
                    max: 1,
                    stepSize: 0.2,
                    fontColor: 'rgba(255, 255, 255, 0.7)',
                    showLabelBackdrop: false
                },
                pointLabels: {
                    fontColor: 'rgba(255, 255, 255, 0.7)'
                },
                gridLines: {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                angleLines: {
                    color: 'rgba(255, 255, 255, 0.7)'
                }
            }
        }
    });
}

function updateChart(newChartData) {
    chartData.datasets[0].data = newChartData;
}