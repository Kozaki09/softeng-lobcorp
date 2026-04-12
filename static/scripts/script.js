const modal = document.getElementById("disclaimerModal");
const agreeBtn = document.getElementById("agreeBtn");

// Check if user already agreed before
if (localStorage.getItem("disclaimerAccepted")) {
    modal.style.display = "none";
}

// When user clicks agree 
agreeBtn.addEventListener("click", () => {
    localStorage.setItem("disclaimerAccepted", "true");
    modal.style.display = "none";
console.log("Disclaimer accepted, modal hidden.");
});
