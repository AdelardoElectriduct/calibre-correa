const PALETTE = ["#b08d57","#7c8b99","#8c4a38"];
const RADAR_LABELS = ["Diseño","Robustez","Precisión","Versatilidad","Precio"];
function radarValues(p){
  return [p.val.diseno,p.val.robustez,p.val.precision,p.val.versatilidad,p.val.precio];
}

function renderCompare(){
  const checked = Array.from(document.querySelectorAll('#chips input:checked')).map(i=>i.value).slice(0,3);
  const elegidos = PRODUCTS.filter(p=>checked.includes(p.id));
  const out = document.getElementById("compareOut");

  if(elegidos.length<2){
    out.innerHTML = '<p class="empty-note">Elige dos o tres relojes arriba para verlos enfrentados.</p>';
    return;
  }

  const campos = [["Precio","precio"],["Movimiento","movimiento"],["Diámetro de caja","diametro"],
                  ["Resistencia al agua","resistencia"],["Cristal","cristal"],["Reserva de marcha","reserva"]];
  const specMap = p => ({
    precio: p.precio + " €",
    movimiento: p.specs.find(s=>s[0]==="Movimiento")[1],
    diametro: p.specs.find(s=>s[0]==="Diámetro de caja")[1],
    resistencia: p.specs.find(s=>s[0]==="Resistencia al agua")[1],
    cristal: p.specs.find(s=>s[0]==="Cristal")[1],
    reserva: p.specs.find(s=>s[0]==="Reserva de marcha")[1],
  });
  const mapped = elegidos.map(specMap);

  const filas = campos.map(([label,key])=>
    `<tr><td><b>${label}</b></td>${mapped.map(m=>`<td>${m[key]}</td>`).join("")}</tr>`
  ).join("");

  out.innerHTML = `
    <table class="compare-table">
      <tr><th></th>${elegidos.map(p=>`<th>${p.marca}<br>${p.modelo}</th>`).join("")}</tr>
      ${filas}
      <tr><td></td>${elegidos.map(p=>`<td><a class="btn btn-primary" style="padding:8px 14px;font-size:0.85rem;" href="${p.enlace}" target="_blank" rel="nofollow noopener">Ver en Amazon</a></td>`).join("")}</tr>
    </table>
    <h2 style="margin-top:40px;">Valoraciones superpuestas</h2>
    <canvas class="radar" id="radarCompare" style="max-width:440px;"></canvas>
    <div class="legend">${elegidos.map((p,i)=>`<span><span class="dot" style="background:${PALETTE[i%3]}"></span>${p.marca}</span>`).join("")}</div>
  `;
  const c = document.getElementById("radarCompare");
  drawRadar(c, elegidos.map((p,i)=>({values:radarValues(p), color:PALETTE[i%3]})), RADAR_LABELS);
}

document.querySelectorAll('#chips input').forEach(el=>{
  el.addEventListener('change', ()=>{
    const checked = document.querySelectorAll('#chips input:checked');
    if(checked.length>3){ el.checked = false; }
    renderCompare();
  });
});
