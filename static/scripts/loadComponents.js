async function loadComponent(path, classId) {
  const res = await fetch(path);
  if (!res.ok) {
    console.error("Failed to load component:", path);
    return;
  }
  const html = await res.text();
  document.getElementById(classId).innerHTML = html;
}

loadComponent("/components/header", "header");
loadComponent("/components/footer", "footer");
loadComponent("/components/home", "main");
