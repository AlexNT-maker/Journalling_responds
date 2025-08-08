const weekData = JSON.parse(document.getElementById("week-data").textContent);
const monthData = JSON.parse(document.getElementById("month-data").textContent);
let currentData = weekData;

function plotMood(data) {
  const dates = data.map(d => d.date);
  const moods = data.map(d => d.mood);
  const tooltips = data.map(d => `Date: ${d.date}<br>Mood: ${d.mood}`);



  const trace = {
    x: dates,
    y: moods,
    type: 'scatter',
    mode: 'lines+markers',
    line: { color: '#636EFA' },
    marker: { size: 8 },
    name: 'Mood',
    text : tooltips,
    hoverinfo: 'text'
  };

  const layout = {
    title: 'Mood over Time',
    xaxis: { title: 'Date' },
    yaxis: { title: 'Mood (1-10)', range: [1, 10] },
    template: 'plotly_dark'
  };

  Plotly.newPlot('mood-chart', [trace], layout, { responsive: true });
}

document.addEventListener('DOMContentLoaded', () => {
  plotMood(currentData);

  const dropdown = document.getElementById('range-select');
  dropdown.addEventListener('change', () => {
    currentData = dropdown.value === 'month' ? monthData : weekData;
    plotMood(currentData);
  });
});
