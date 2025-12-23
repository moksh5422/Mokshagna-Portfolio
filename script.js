const toggle = document.getElementById('theme-toggle');

// Page starts in DARK mode
toggle.textContent = "☀️";

toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');

    toggle.textContent =
        document.body.classList.contains('dark') ? "☀️" : "🌙";
});

