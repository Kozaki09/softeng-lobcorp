const session = "{{ session }}";

if (session) {
    document.getElementById("home").style.display = "block";
    document.getElementById("subscribe").style.display = "block";
} else {
    document.getElementById("login").style.display = "block";
    document.getElementById("register").style.display = "block";
}