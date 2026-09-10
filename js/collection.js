const STORAGE_KEY = "watchbox-selection";
const SIZE_KEY = "watchbox-size";

function loadState(){
  let size = parseInt(localStorage.getItem(SIZE_KEY) || "3", 10);
  let sel = [];
  try { sel = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); } catch(e){ sel = []; }
  sel = sel.filter(id => PRODUCTS.some(p=>p.id===id)).slice(0, size);
  return {size, sel};
}
function saveState(state){
  localStorage.setItem(SIZE_KEY, String(state.size));
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.sel));
}

let state = loadState();

function renderAll(){
  document.querySelector(`input[name="boxsize"][value="${state.size}"]`).checked = true;
  renderRoller();
  renderScore();
  renderPicker();
}

function renderRoller(){
  const el = document.getElementById("rollerSlots");
  let html = "";
  for(let i=0;i<state.size;i++){
    const id = state.sel[i];
    if(id){
      const p = PRODUCTS.find(x=>x.id===id);
      html += `<div class="roller-slot" style="background:${p.color}" ontouchstart="this.classList.toggle('tilted')">${p.initials}<br><span style="font-size:0.6rem;font-weight:400;">${p.marca}</span></div>`;
    }else{
      html += `<div class="roller-slot empty">+</div>`;
    }
  }
  el.innerHTML = html;
}

function renderScore(){
  const el = document.getElementById("scoreBlock");
  const selected = state.sel.map(id=>PRODUCTS.find(p=>p.id===id));
  if(selected.length===0){
    el.innerHTML = `<div class="score-block"><p style="color:var(--paper-dim)">Elige al menos un reloj para ver la valoración de tu colección.</p></div>`;
    return;
  }
  if(selected.length===1){
    el.innerHTML = `<div class="score-block"><p style="color:var(--paper-dim)">Con un solo reloj no medimos variedad, tiene que cubrir todo por sí solo. Súbelo a caja de 3 o 6 para ver cómo se complementa una colección.</p></div>`;
    return;
  }

  const catSet = new Set();
  const movSet = new Set();
  const prices = [];
  selected.forEach(p=>{
    p.categorias.forEach(c=>catSet.add(c));
    const mov = p.specs.find(s=>s[0]==="Movimiento")[1].split(" ")[0];
    movSet.add(mov);
    prices.push(parseInt(p.precio,10));
  });

  const varietyCatScore = Math.min(10, (catSet.size/6)*10);
  const varietyMovScore = Math.min(10, (movSet.size/3)*10);
  const spread = Math.max(...prices) - Math.min(...prices);
  const priceScore = Math.min(10, (spread/421)*10);
  const final = Math.round(varietyCatScore*0.4 + varietyMovScore*0.3 + priceScore*0.3);

  let label;
  if(final<=3) label = "Colección muy enfocada — ideal si ya sabes exactamente qué estilo te gusta.";
  else if(final<=6) label = "Colección con cierta variedad, cubre varios estilos sin dispersarse.";
  else label = "Colección muy versátil: tienes un reloj para casi cualquier ocasión.";

  const tips = [];
  if(!catSet.has("cuarzo")) tips.push("Te falta un cuarzo: más precisión diaria y cero mantenimiento.");
  if(!catSet.has("resistentes")) tips.push("Ningún reloj de 100 m o más: piénsalo si nadas o buceas con él puesto.");
  if(!catSet.has("vestir")) tips.push("No tienes ninguno de vestir para ocasiones formales.");
  if(movSet.size===1) tips.push("Todos comparten el mismo tipo de movimiento, prueba a mezclar automático, manual o cuarzo.");
  if(spread<150) tips.push("Los precios están muy juntos: una colección con más rango de precio suele cubrir más ocasiones.");

  el.innerHTML = `
    <div class="score-block">
      <span class="score-num">${final}/10</span>
      <p style="margin-top:6px;">${label}</p>
      ${tips.length ? `<ul class="tips">${tips.map(t=>`<li>${t}</li>`).join("")}</ul>` : ""}
    </div>`;
}

function renderPicker(){
  const el = document.getElementById("pickerGrid");
  el.innerHTML = PRODUCTS.map(p=>{
    const isIn = state.sel.includes(p.id);
    const full = state.sel.length >= state.size;
    const disabled = (!isIn && full) ? "disabled" : "";
    return `<div class="picker-card">
      <div class="top">${watchfaceHtml(p)}<div><h4>${p.marca} ${p.modelo}</h4><div class="meta">${p.precio} €</div></div></div>
      <button class="${isIn?'added':''}" ${disabled} onclick="toggle('${p.id}')">${isIn ? "Quitar de la caja" : "Añadir a la caja"}</button>
      <a href="/reloj-${p.id}.html" style="font-size:0.78rem;color:var(--steel);">Ver ficha</a>
    </div>`;
  }).join("");
}

function watchfaceHtml(p){
  return `<div class="watchface" style="background:${p.color};width:52px;height:52px;font-size:0.9rem;">${p.initials}</div>`;
}

function toggle(id){
  if(state.sel.includes(id)){
    state.sel = state.sel.filter(x=>x!==id);
  }else if(state.sel.length < state.size){
    state.sel.push(id);
  }
  saveState(state);
  renderAll();
}

document.querySelectorAll('input[name="boxsize"]').forEach(r=>{
  r.addEventListener("change", ()=>{
    state.size = parseInt(r.value,10);
    state.sel = state.sel.slice(0, state.size);
    saveState(state);
    renderAll();
  });
});

renderAll();
