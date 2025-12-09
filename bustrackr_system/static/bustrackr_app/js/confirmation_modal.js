// Universal Confirmation Modal System

// Opens confirmation modal and stores the form + modal to reopen
function openConfirmModal(formId, modalIdToReopen, message) {
    document.getElementById("formToSubmit").value = formId;
    document.getElementById("modalToReopen").value = modalIdToReopen;
    document.getElementById("confirmMessage").innerText = message;

    var confirmModal = new bootstrap.Modal(document.getElementById("confirmSaveModal"));
    confirmModal.show();
}

// For Cancel button — reopen previous modal
function cancelConfirmation() {
    let modalId = document.getElementById("modalToReopen").value;

    var confirmSaveModal = bootstrap.Modal.getInstance(document.getElementById("confirmSaveModal"));
    confirmSaveModal.hide();

    if (modalId) {
        var originalModal = new bootstrap.Modal(document.getElementById(modalId));
        setTimeout(() => originalModal.show(), 300);
    }
}

// Seat Update → Confirmation Modal
function openConfirmSeatModal() {
    document.getElementById("formToSubmit").value = "seatUpdateForm";
    document.getElementById("confirmMessage").textContent = 
        "Are you sure you want to update the seat availability?";
    
    const modal = new bootstrap.Modal(document.getElementById("confirmSaveModal"));
    modal.show();
}

function submitChosenForm() {
    const formId = document.getElementById("formToSubmit").value;
    document.getElementById(formId).querySelector("#seatRealSubmitBtn").click();
}

