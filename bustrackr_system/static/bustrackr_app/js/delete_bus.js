function openDeleteBusModal(id) {
        document.getElementById("deleteBusBtn").href = "/delete-bus/" + id + "/";
        var modal = new bootstrap.Modal(document.getElementById('confirmDeleteBus'));
        modal.show();
    }