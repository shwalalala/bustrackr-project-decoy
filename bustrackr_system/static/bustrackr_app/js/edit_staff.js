const editModal = document.getElementById('edit_staff');

editModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;

    const staffId = button.getAttribute('data-id');
    const staffName = button.getAttribute('data-name');

    const form = editModal.querySelector('form');
    const nameInput = editModal.querySelector('#editStaffName');

    nameInput.value = staffName;

    // CORRECTED URL (dash instead of underscore)
    form.action = `/edit-staff/${staffId}/`;
});
