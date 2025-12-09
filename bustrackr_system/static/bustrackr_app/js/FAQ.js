function toggleFAQ(button) {
    const content = button.nextElementSibling;
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", expanded ? "false" : "true");
    content.style.maxHeight = expanded ? "0" : content.scrollHeight + "px";
}