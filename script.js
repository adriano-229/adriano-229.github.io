const updateExpandButtons = () => {
  document.querySelectorAll(".expand-button").forEach((button) => {
    const preview = button.previousElementSibling;
    if (!preview.classList.contains("is-expanded")) {
      const isTruncated = preview.scrollHeight > preview.clientHeight;
      preview.classList.toggle("is-truncated", isTruncated);
      button.hidden = !isTruncated;
    }
  });
};

document.querySelectorAll(".expand-button").forEach((button) => {
  button.addEventListener("click", () => {
    const preview = button.previousElementSibling;
    const expanded = preview.classList.toggle("is-expanded");
    button.hidden = false;
    button.setAttribute("aria-expanded", String(expanded));
    button.textContent = expanded ? "↑ Show less" : "↓ Show more";
  });
});

updateExpandButtons();
window.addEventListener("resize", updateExpandButtons);
