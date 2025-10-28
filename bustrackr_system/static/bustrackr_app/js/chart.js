const ctx = document.getElementById('busUtilizationBar');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Active', 'Idle', 'Maintenance', 'On Trip'],
    datasets: [{
      label: 'Bus Count',
      data: [18, 6, 3, 3],
      backgroundColor: ['#0d6efd', '#0dcaf0', '#ffc107', '#198754'],
      borderRadius: 6,
      barThickness: 40
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true }
    },
    scales: {
      x: {
        ticks: { color: '#fff' },
        grid: { display: false }
      },
      y: {
        ticks: { color: '#fff' },
        grid: { color: 'rgba(255,255,255,0.1)' }
      }
    }
  }
});
