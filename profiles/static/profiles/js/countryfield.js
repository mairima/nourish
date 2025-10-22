// Make form read-only until "Edit" is clicked
(function () {
  var form = document.getElementById('profile-update-form');
  if (!form) return;

  var fields = form.querySelectorAll('input, select, textarea');
  var editBtn = document.getElementById('profile-edit-btn');
  var cancelBtn = document.getElementById('profile-cancel-btn');
  var submitBtn = document.getElementById('profile-submit-btn');

  function setEditing(on) {
    fields.forEach(function (el) { el.disabled = !on; });
    submitBtn.disabled = !on;
    cancelBtn.classList.toggle('d-none', !on);
    editBtn.classList.toggle('d-none', on);
  }

  // Start read-only
  setEditing(false);

  editBtn.addEventListener('click', function (e) {
    e.preventDefault();
    setEditing(true);
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  cancelBtn.addEventListener('click', function (e) {
    e.preventDefault();
    form.reset();
    setEditing(false);
  });
})();