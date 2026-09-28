const themeBtn = document.getElementById("themeToggle");
function setIcon(){
  const light = document.documentElement.getAttribute("data-theme") === "light";
  themeBtn.textContent = light ? "🌙" : "☀️";
  themeBtn.setAttribute("aria-label", light ? "Cambiar a modo oscuro" : "Cambiar a modo claro");
}
if(themeBtn){
  setIcon();
  themeBtn.addEventListener("click", ()=>{
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    try{ localStorage.setItem("theme", next); }catch(e){}
    setIcon();
  });
}
