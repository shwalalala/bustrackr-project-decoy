document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".toast-item");

    toasts.forEach((toast, index) => {

        // Show animation
        setTimeout(() => {
            toast.classList.remove("opacity-0", "-translate-y-5");
            toast.classList.add("opacity-100", "translate-y-0");
        }, 100 * index);

        // Auto hide after 3 seconds
        setTimeout(() => {
            toast.classList.add("opacity-0", "-translate-y-5");

            // Remove element after fade-out
            setTimeout(() => toast.remove(), 500);
        }, 3000 + index * 100);

         console.log("Toast items found:", document.querySelectorAll(".toast-item").length);

    });

});
