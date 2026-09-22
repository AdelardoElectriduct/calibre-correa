document.getElementById("calcBtn").addEventListener("click", ()=>{
  const v = parseFloat(document.getElementById("muneca").value);
  const out = document.getElementById("resultadoCalc");
  if(!v || v<10 || v>26){
    out.innerHTML = '<div class="tool-result">Introduce una circunferencia de muñeca válida, entre 12 y 24 cm.</div>';
    return;
  }
  let min, max, rango, recomendacion;
  if(v<15){ min=34; max=38; rango="34–38 mm"; recomendacion="Muñecas finas: un diámetro mayor de 40mm suele quedar desproporcionado."; }
  else if(v<17){ min=36; max=40; rango="36–40 mm"; recomendacion="Rango versátil: la mayoría de relojes de 40mm encajan bien."; }
  else if(v<19){ min=40; max=44; rango="40–44 mm"; recomendacion="Buen margen para diseños deportivos algo más grandes."; }
  else{ min=42; max=46; rango="42–46 mm"; recomendacion="Muñecas anchas: cajas pequeñas pueden verse hundidas, prioriza 42mm o más."; }

  let matchesHtml = "";
  if(typeof PRODUCTS !== "undefined"){
    const matches = PRODUCTS.filter(p => p.diametro_mm >= min && p.diametro_mm <= max);
    if(matches.length){
      matchesHtml = `<div style="margin-top:18px;">
        <p style="color:var(--paper-dim);font-size:0.9rem;margin-bottom:10px;">De nuestro catálogo, estos encajan en ese rango:</p>
        <div class="picker-grid">${matches.map(p => `
          <div class="picker-card">
            <div class="top"><a href="/reloj-${p.id}.html" aria-hidden="true" tabindex="-1"><div class="watchface" style="width:52px;height:52px;">${p.illustration}</div></a>
            <div><h4>${p.marca} ${p.modelo}</h4><div class="meta">${p.precio} € · ${p.diametro_mm} mm</div></div></div>
            <a href="/reloj-${p.id}.html" class="btn btn-ghost" style="text-align:center;">Ver ficha</a>
          </div>`).join("")}</div>
      </div>`;
    }
  }

  out.innerHTML = `<div class="tool-result">Diámetro de caja recomendado: <b>${rango}</b>.<br>${recomendacion}</div>${matchesHtml}`;
});
