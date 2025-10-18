document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggleSidebar");

  if (sidebar && toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("w-64");
      sidebar.classList.toggle("w-20");

      // Toggle text visibility
      sidebar.querySelectorAll("span").forEach((span) => {
        span.classList.toggle("hidden");
      });

      // Toggle icon direction
      const icon = toggleBtn.querySelector("i");
      icon.classList.toggle("bi-chevron-left");
      icon.classList.toggle("bi-chevron-right");
    });
  }
});
