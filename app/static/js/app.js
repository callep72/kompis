// Dark/light mode toggle
const toggle = document.getElementById('theme-toggle');
if (toggle) {
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        toggle.querySelector('i').className =
            theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
        localStorage.setItem('theme', theme);
    }
    applyTheme(document.documentElement.getAttribute('data-bs-theme') || 'light');
    toggle.addEventListener('click', () => {
        applyTheme(document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark');
    });
}

// Auto-generate slug from name in category form
const nameInput = document.querySelector('input[name="name"]');
const slugInput = document.querySelector('input[name="slug"]');

if (nameInput && slugInput && !slugInput.value) {
    nameInput.addEventListener('input', () => {
        slugInput.value = nameInput.value
            .toLowerCase()
            .replace(/å/g, 'a').replace(/ä/g, 'a').replace(/ö/g, 'o')
            .replace(/[^a-z0-9/]+/g, '-')
            .replace(/^-|-$/g, '');
    });
}
