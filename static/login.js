const checkbox = document.getElementById('understand');
const continueBtn = document.getElementById('continue');

checkbox.addEventListener('change', () => {
  continueBtn.disabled = !checkbox.checked;
});

const cont = document.getElementById('continue');
const section = document.getElementById('section2');

cont.addEventListener("click", () => {
    section.classList.add("remov");
});