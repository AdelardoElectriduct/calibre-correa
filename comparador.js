function drawRadar(canvas, series, labels){
  const ctx = canvas.getContext("2d");
  const w = canvas.width = canvas.clientWidth * 2;
  const h = canvas.height = canvas.clientWidth * 2;
  ctx.clearRect(0,0,w,h);
  const cx = w/2, cy = h/2, R = w*0.34;
  const n = labels.length;
  const angle = i => (Math.PI*2*i/n) - Math.PI/2;

  ctx.strokeStyle = "rgba(243,238,228,0.16)";
  ctx.lineWidth = 2;
  for(let ring=1; ring<=4; ring++){
    ctx.beginPath();
    for(let i=0;i<=n;i++){
      const a = angle(i%n);
      const r = R*ring/4;
      const x = cx + r*Math.cos(a), y = cy + r*Math.sin(a);
      i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
    }
    ctx.stroke();
  }
  ctx.fillStyle = "#f3eee4";
  ctx.font = (w*0.028)+"px Inter, sans-serif";
  ctx.textAlign = "center";
  labels.forEach((label,i)=>{
    const a = angle(i);
    const x = cx + (R+w*0.09)*Math.cos(a);
    const y = cy + (R+w*0.09)*Math.sin(a);
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.lineTo(cx+R*Math.cos(a), cy+R*Math.sin(a));
    ctx.strokeStyle = "rgba(243,238,228,0.12)";
    ctx.stroke();
    ctx.fillText(label, x, y);
  });
  series.forEach(s=>{
    ctx.beginPath();
    s.values.forEach((v,i)=>{
      const a = angle(i);
      const r = R*(v/10);
      const x = cx + r*Math.cos(a), y = cy + r*Math.sin(a);
      i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
    });
    ctx.closePath();
    ctx.fillStyle = s.color + "33";
    ctx.strokeStyle = s.color;
    ctx.lineWidth = w*0.006;
    ctx.fill();
    ctx.stroke();
  });
}
