const advancedGroupElement = document.querySelector(".advanced-section");
const formSelect           = document.querySelector("#form-type");
const IS_PREMIUM           = formSelect.querySelector('option[value="advanced"]')?.disabled === false;

formSelect.addEventListener("change", (e) => {
  const form = e.target.value;
  const fbs = document.getElementById('fbs');
  const mode_label = document.getElementById("mode-label");

  switch (form) {
    case "basic":
      advancedGroupElement.classList.add("hidden");
      mode_label.innerHTML = "Basic Mode (Home-Accessible Inputs)";
      fbs.innerHTML = "Fasting Blood Sugar &gt; 120 mg/dl (optional)";
      fbs.removeAttribute('required');
      break;
    case "advanced":
      // Always show the section — free users see the gate card, premium see inputs
      advancedGroupElement.classList.remove("hidden");
      mode_label.innerHTML = "Advanced Mode (Clinical/Diagnostic Inputs)";
      fbs.innerHTML = "Fasting Blood Sugar &gt; 120 mg/dl";
      fbs.setAttribute('required', ''); 
      break;
  }
});