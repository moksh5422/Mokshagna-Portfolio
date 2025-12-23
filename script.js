const toggle = document.getElementById("theme-toggle");

// DARK MODE DEFAULT
toggle.textContent = "☀️";

toggle.addEventListener("click", () => {
    document.body.classList.toggle("light");

    toggle.textContent =
        document.body.classList.contains("light") ? "🌙" : "☀️";
});
