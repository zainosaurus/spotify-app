var barChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'Dataset 1',
        color: '#cfecfe',
        borderWidth: 1,
        data: [
            1, 2, 3, 4, 5, 6, 7
        ]
    }]

};
$(document).ready(function() {
    var ctx = document.getElementById('chart').getContext('2d');
    window.myBar = new Chart(ctx, {
        type: 'bar',
        data: barChartData,
        options: {
            responsive: true,
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Chart.js Bar Chart'
            }
        }
    });
});

function updateChart(newChartData) {
    barChartData.datasets
}