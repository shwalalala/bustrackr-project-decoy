

document.addEventListener("DOMContentLoaded", function() {
        const ctx = document.getElementById('tripStatusChart');
        if (ctx) {
            // 2. READ DATA SAFELY IN JAVASCRIPT
            // Using try-catch to be extra safe
            try {
                const labels = JSON.parse(document.getElementById('chart-labels-data').textContent);
                const data = JSON.parse(document.getElementById('chart-data-data').textContent);

                new Chart(ctx.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: labels, 
                        datasets: [{
                            label: 'Trips',
                            data: data, 
                            backgroundColor: [
                                '#198754', // Green
                                '#ffc107', // Yellow
                                '#dc3545'  // Red
                            ],
                            borderWidth: 0,
                            borderRadius: 4,
                            barPercentage: 0.5
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                ticks: { color: '#cbd5e1', stepSize: 1 }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { color: '#cbd5e1' }
                            }
                        }
                    }
                });
            } catch (error) {
                console.error("Error loading chart data:", error);
            }
        }
    });

    // --- Modal Functions ---
    function openEditBusModal(id, plate, company, type, capacity, status) {
      document.getElementById("editBusForm").action = "/edit-bus/" + id + "/";
      document.getElementById("editBusPlate").value = plate;
      document.getElementById("editBusCompany").value = company;
      document.getElementById("editBusType").value = type;
      document.getElementById("editBusCapacity").value = capacity;
      document.getElementById("editBusStatus").value = status;
      new bootstrap.Modal(document.getElementById('edit_bus')).show();
    }
    function submitEditBusForm() { document.getElementById("editBusForm").submit(); }
    function openConfirmRegisterModal() { new bootstrap.Modal(document.getElementById('confirmRegisterBusModal')).show(); }
    function submitRegisterBus() { document.querySelector('#registerBusModal form').submit(); }
    function openDeleteBusModal(id) {
        document.getElementById("deleteBusBtn").href = "/delete-bus/" + id + "/";
        new bootstrap.Modal(document.getElementById('confirmDeleteBus')).show();
    }