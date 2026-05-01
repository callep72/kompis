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
