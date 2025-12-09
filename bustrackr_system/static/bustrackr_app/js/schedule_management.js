function openEditSchedule(id, busId, route, dep, arr, status) {
  document.getElementById("editScheduleForm").action = "/schedule/edit/" + id + "/";
  
  document.getElementById("editBus").value = busId;
  document.getElementById("editRoute").value = route;
  document.getElementById("editDeparture").value = dep;
  document.getElementById("editArrival").value = arr;
  document.getElementById("editStatus").value = status;

  // Show the Bootstrap modal
  var modal = new bootstrap.Modal(document.getElementById("editScheduleModal"));
  modal.show();
}