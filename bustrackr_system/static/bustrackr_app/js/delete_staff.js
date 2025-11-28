document.addEventListener("DOMContentLoaded", function () {
  const deleteModal = document.getElementById("delete_staff");

  deleteModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    const staffId = button.getAttribute("data-id");
    const staffName = button.getAttribute("data-name");

    document.getElementById("deleteStaffId").value = staffId;
    document.getElementById("deleteStaffName").textContent = staffName;

    // Set form action dynamically
    const form = document.getElementById("deleteStaffForm");
    form.action = `/delete-staff/${staffId}/`;
  });
});