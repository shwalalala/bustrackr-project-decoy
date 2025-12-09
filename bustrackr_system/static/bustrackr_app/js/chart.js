document.addEventListener("DOMContentLoaded", function() {
    const chartCanvas = document.getElementById('busUtilizationBar');
    
    if (chartCanvas) {
        // Destroy existing chart if it exists (prevents duplication glitches)
        if (window.myBusChart) {
            window.myBusChart.destroy();
        }

        const ctx = chartCanvas.getContext('2d');

        // Access the data passed from the HTML
        const labels = window.reportData ? window.reportData.labels : ['No Data'];
        const data = window.reportData ? window.reportData.data : [0];

        window.myBusChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Trips',
                    data: data,
                    backgroundColor: [
                        '#198754', // Green (On Time)
                        '#ffc107', // Yellow (Delayed)
                        '#dc3545'  // Red (Cancelled)
                    ],
                    borderColor: [
                        '#198754',
                        '#ffc107',
                        '#dc3545'
                    ],
                    borderWidth: 1,
                    barPercentage: 0.5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false 
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)' 
                        },
                        ticks: {
                            color: '#cbd5e1', 
                            stepSize: 1
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#cbd5e1' 
                        }
                    }
                }
            }
        });
    }
});