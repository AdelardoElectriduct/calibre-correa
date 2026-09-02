document.getElementById("calcBtn").addEventListener("click", ()=>{
  const v = parseFloat(document.getElementById("muneca").value);
  const out = document.getElementById("resultadoCalc");
  if(!v || v<10 || v>26){
    out.innerHTML = '<div class="tool-result">Introduce una circunferencia de muñeca válida, entre 12 y 24 cm.</div>';
    return;
  }
  let rango, recomendacion;
  if(v<15){ rango="34–38 mm"; recomendacion="Muñecas finas: un diámetro mayor de 40mm suele quedar desproporcionado."; }
  else if(v<17){ rango="36–40 mm"; recomendacion="Rango versátil: la mayoría de relojes de 40mm encajan bien."; }
  else if(v<19){ rango="40–44 mm"; recomendacion="Buen margen para diseños deportivos algo más grandes."; }
  else{ rango="42–46 mm"; recomendacion="Muñecas anchas: cajas pequeñas pueden verse hundidas, prioriza 42mm o más."; }
  out.innerHTML = `<div class="tool-result">Diámetro de caja recomendado: <b>${rango}</b>.<br>${recomendacion}</div>`;
});
