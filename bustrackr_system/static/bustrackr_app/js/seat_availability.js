// Opens the seat update modal and fills the fields dynamically
console.log("seat-availability.js loaded successfully!");

function openSeatModal(scheduleId, plate, capacity, availableSeats, operation) {
    document.getElementById("scheduleIdField").value = scheduleId;
    document.getElementById("operationField").value = operation;

    document.getElementById("modalBusPlate").innerText = plate;
    document.getElementById("modalCapacity").innerText = capacity;
    document.getElementById("modalAvailable").innerText = availableSeats;

    const modal = new bootstrap.Modal(document.getElementById("seatUpdateModal"));
    modal.show();
}

