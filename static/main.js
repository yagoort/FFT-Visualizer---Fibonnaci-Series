// Show loading animation on form submit and file upload
window.addEventListener('DOMContentLoaded', function() {
  var form = document.querySelector('form');
  var loading = document.getElementById('loading');
  if (form && loading) {
    form.addEventListener('submit', function() {
      loading.style.display = 'flex';
    });
    var fileInput = document.getElementById('csvfile');
    if (fileInput) {
      fileInput.addEventListener('change', function() {
        loading.style.display = 'flex';
      });
    }
  }
});
