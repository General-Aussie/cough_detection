const checkbox = document.getElementById('understand');
const continueBtn = document.getElementById('continue');

checkbox.addEventListener('change', () => {
  continueBtn.disabled = !checkbox.checked;
});
