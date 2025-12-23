const toggle = document.getElementById('theme-toggle');

// Default: DARK (no class needed)
toggle.textContent = "☀️";

toggle.addEventListener('click', () => {
    document.body.classList.toggle('light');

    const isLight = document.body.classList.contains('light');
    toggle.textContent = isLight ? "🌙" : "☀️";
});

