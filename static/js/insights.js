const weekData  = JSON.parse(document.getElementById("week-data").textContent);
const monthData = JSON.parse(document.getElementById("month-data").textContent);

// --- helpers ---
const moodLabel = (m) => {
  if (m == null) return "No entry";
  if (m <= 3) return "Low / Drained";
  if (m <= 6) return "Neutral";
  if (m <= 8) return "Good";
  return "Great";
};

const moodColor = (m) => {
  if (m == null) return 'rgba(150,150,150,0.6)';
  // κόκκινο -> κίτρινο -> πράσινο
  if (m <= 3) return '#EF553B';
  if (m <= 6) return '#FECB52';
  return '#00CC96';
};

function movingAverage(series, window=7) {
  const out = [];
  for (let i=0; i<series.length; i++) {
    let sum = 0, count = 0;
    for (let j=i-window+1; j<=i; j++) {
      if (j>=0 && series[j]?.mood != null) {
        sum += series[j].mood;
        count += 1;
      }
    }
    out.push(count ? +(sum / count).toFixed(2) : null);
  }
  return out;
}

// --- state ---
const savedRange = localStorage.getItem('insightsRange') || 'week';
let currentData = (savedRange === 'month') ? monthData : weekData;

// --- plot ---
function plotMood(data) {
  const dates = data.map(d => d.date);
  const moods = data.map(d => d.mood);
  const colors = data.map(m => moodColor(m));
  const tooltips = data.map(d => `Date: ${d.date}<br>Mood: ${d.mood ?? '—'} (${moodLabel(d.mood)})`);
  const ma7 = movingAverage(data, 7);

  const points = {
    x: dates,
    y: moods,
    type: 'scatter',
    mode: 'markers',
    marker: { size: 9, color: colors, line: {width: 0} },
    name: 'Mood',
    text: tooltips,
    hoverinfo: 'text',
    connectgaps: false
  };

  const trend = {
    x: dates,
    y: ma7,
    type: 'scatter',
    mode: 'lines',
    name: '7‑day avg',
    line: { width: 2 },
    hoverinfo: 'skip',
    connectgaps: false
  };

  const layout = {
    title: 'Mood over Time',
    xaxis: { title: 'Date' },
    yaxis: { title: 'Mood (1‑10)', range: [1,10] },
    template: 'plotly_dark',
    margin: { t: 50, r: 20, b: 60, l: 50 }
  };

  Plotly.newPlot('mood-chart', [points, trend], layout, {responsive:true, displaylogo:false});
}

// --- init ---
document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.getElementById('range-select');
  dropdown.value = (currentData === monthData) ? 'month' : 'week';
  plotMood(currentData);

  dropdown.addEventListener('change', () => {
    currentData = dropdown.value === 'month' ? monthData : weekData;
    localStorage.setItem('insightsRange', dropdown.value);
    plotMood(currentData);
  });
});
