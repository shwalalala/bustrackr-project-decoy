 function openConfirmRegisterModal() {
        let confirmModal = new bootstrap.Modal(document.getElementById('confirmRegisterBusModal'));
        confirmModal.show();
    }

    function submitRegisterBus() {
        document.querySelector('#registerBusModal form').submit();
    }