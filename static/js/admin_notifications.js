// Global admin toast notifications (Django messages)
// Rendered once in admin_panel/base.html

(function () {
    function hideToast(toast) {
        if (!toast || toast.classList.contains('is-hiding')) return;
        toast.classList.add('is-hiding');
        window.setTimeout(function () {
            toast.remove();
        }, 200);
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-admin-toast-close]');
        if (!btn) return;
        var toast = btn.closest('.admin-toast');
        hideToast(toast);
    });

    window.setTimeout(function () {
        document.querySelectorAll('.admin-toast[data-autodismiss="1"]').forEach(function (toast) {
            hideToast(toast);
        });
    }, 4000);
})();
