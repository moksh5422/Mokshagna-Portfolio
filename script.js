const toggle = document.getElementById('theme-toggle');

// Default to dark mode
document.body.classList.add('dark');
toggle.textContent = "☀️";

// Toggle + remember preference
toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');

    const isDark = document.body.classList.contains('dark');
    toggle.textContent = isDark ? "☀️" : "🌙";
});

