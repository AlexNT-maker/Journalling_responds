const weekData  = JSON.parse(document.getElementById("week-data").textContent);
const monthData = JSON.parse(document.getElementById("month-data").textContent);

const moodLabel = (m) => (m==null ? "No entry" : m<=3 ? "Low / Drained" : m<=6 ? "Neutral" : m<=8 ? "Good" : "Great");
const moodColor = (m) => (m==null ? 'rgba(150,150,150,0.6)' : m<=3 ? '#EF553B' : m<=6 ? '#FECB52' : '#00CC96');

function movingAverage(series, window=7){
  const out=[]; for(let i=0;i<series.length;i++){let s=0,c=0;for(let j=i-window+1;j<=i;j++){if(j>=0&&series[j]?.mood!=null){s+=series[j].mood;c++;}}out.push(c?+(s/c).toFixed(2):null);}return out;
}

const savedRange = localStorage.getItem('insightsRange') || 'week';
let currentData = (savedRange === 'month') ? monthData : weekData;

function plotMood(data){
  const el = document.getElementById('mood-chart');
  el.style.opacity = 0; // κρύψε μέχρι να στηθεί

  const dates = data.map(d=>d.date);
  const moods = data.map(d=>d.mood);
  const colors= data.map(m=>moodColor(m));
  const tips  = data.map(d=>`Date: ${d.date}<br>Mood: ${d.mood ?? '—'} (${moodLabel(d.mood)})`);
  const ma7   = movingAverage(data,7);

  const points = { x:dates, y:moods, type:'scatter', mode:'markers',
    marker:{size:9, color:colors, line:{width:0}}, name:'Mood',
    text:tips, hoverinfo:'text', connectgaps:false };

  const trend  = { x:dates, y:ma7, type:'scatter', mode:'lines',
    name:'7‑day avg', line:{width:2}, hoverinfo:'skip', connectgaps:false };

  const isDark = document.documentElement.classList.contains('dark-mode');

  const layout = {
    title:'Mood over Time',
    xaxis:{title:'Date'}, yaxis:{title:'Mood (1‑10)', range:[1,10]},
    template: isDark ? 'plotly_dark' : 'plotly_white',
    margin:{t:50,r:20,b:60,l:50},
    paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)'
  };

  // περιμένουμε 1 frame για να “κάτσει” το theme, μετά κάνουμε render
  requestAnimationFrame(()=>{
    Plotly.newPlot('mood-chart', [points, trend], layout, {responsive:true, displaylogo:false})
      .then(()=>{ el.style.opacity = 1; }); // και εμφανίζουμε ομαλά
  });
}

document.addEventListener('DOMContentLoaded', ()=>{
  const dd = document.getElementById('range-select');
  dd.value = (currentData === monthData) ? 'month' : 'week';
  plotMood(currentData);

  dd.addEventListener('change', ()=>{
    currentData = dd.value === 'month' ? monthData : weekData;
    localStorage.setItem('insightsRange', dd.value);
    plotMood(currentData);
  });

  // ξανασχεδίασε όταν αλλάζει theme (αυτό ήταν το "προαιρετικό αλλά ωραίο")
  const toggle = document.querySelector('.theme-switch__checkbox');
  if (toggle) toggle.addEventListener('change', ()=>plotMood(currentData));
});
