const dial = document.getElementById("heroDial");
if(dial){
  for(let i=0;i<12;i++){
    const t = document.createElement("div");
    t.className = "tick";
    t.style.transform = `rotate(${i*30}deg)`;
    dial.appendChild(t);
  }
  const now = new Date();
  const hourHand = document.createElement("div");
  hourHand.className = "hand short";
  hourHand.style.transform = `rotate(${(now.getHours()%12)*30 + now.getMinutes()*0.5}deg)`;
  const minHand = document.createElement("div");
  minHand.className = "hand";
  minHand.style.transform = `rotate(${now.getMinutes()*6}deg)`;
  dial.appendChild(hourHand);
  dial.appendChild(minHand);
  const pin = document.createElement("div");
  pin.className = "pin";
  dial.appendChild(pin);
}
