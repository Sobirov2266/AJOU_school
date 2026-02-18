function togglePassword() {
    const input = document.getElementById("passwordInput");
    if (!input) return;
    const icon = event.currentTarget.querySelector("i");
    if (!icon) return;

    if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.replace("fa-eye-slash", "fa-eye");
    }
}

function showFileName(input) {
    const label = document.getElementById("fileName");
    if (input.files.length > 0) {
        label.textContent = input.files[0].name;
    }
}

// Phone input UX:
// - Always start with '+'
// - Only digits after '+'
// - Limit to 12 digits after '+' (total length 13)
document.addEventListener("DOMContentLoaded", () => {
    const phoneInput = document.querySelector('input[name="parent_phone"]');
    if (!phoneInput) return;

    const normalize = () => {
        let v = phoneInput.value || "";
        v = v.trim();

        if (!v) {
            phoneInput.value = "+";
            return;
        }

        if (!v.startsWith("+")) v = "+" + v;

        // Keep only digits after '+'
        const digits = v.slice(1).replace(/\D+/g, "").slice(0, 12);
        phoneInput.value = "+" + digits;
    };

    phoneInput.addEventListener("focus", normalize);
    phoneInput.addEventListener("input", normalize);
});
