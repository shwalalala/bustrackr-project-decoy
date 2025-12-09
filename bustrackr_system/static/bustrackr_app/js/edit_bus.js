function openEditBusModal(id, plate, company, type, capacity, status) {
      document.getElementById("editBusForm").action = "/edit-bus/" + id + "/";
      document.getElementById("editBusPlate").value = plate;
      document.getElementById("editBusCompany").value = company;
      document.getElementById("editBusType").value = type;
      document.getElementById("editBusCapacity").value = capacity;
      document.getElementById("editBusStatus").value = status;
      var modal = new bootstrap.Modal(document.getElementById('edit_bus'));
      modal.show();
    }

    function openConfirmSaveModal() {
      var modal = new bootstrap.Modal(document.getElementById('confirmSaveModal'));
      modal.show();
    }

    function submitEditBusForm() {
      document.getElementById("editBusForm").submit();
    }
