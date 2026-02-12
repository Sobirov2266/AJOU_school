<script>
  document.querySelectorAll('[data-modal-open]').forEach(btn => {
    btn.onclick = () => {
      document.getElementById(btn.dataset.modalOpen).classList.add('open');
    };
  });

  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.onclick = () => {
      btn.closest('.modal').classList.remove('open');
    };
  });
</script>
