const advancedGroupElement = document.querySelector(".advanced-section");
console.log(advancedGroupElement)
document.querySelector(".form").addEventListener("change", (e) => {
  const form = e.target.value;

  console.log(form);
  switch (form) {
    case "basic":
      advancedGroupElement.classList.add("hidden");
      break;
    case "advanced":
      advancedGroupElement.classList.remove("hidden");
      break;
  }
});