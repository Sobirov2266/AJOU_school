function togglePassword() {
    const input = document.getElementById("passwordInput");
    const icon = event.currentTarget.querySelector("i");

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
