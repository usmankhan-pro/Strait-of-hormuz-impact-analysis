const DATA_URL = "./strait_of_hormuz_closure_impacts_cleaned.csv";
const RISK_ORDER = ["Critical", "High", "Severe", "Moderate", "Low"];
const COLORS = { ink: "#34423b", muted: "#7b8780", grid: "#e7ebe5", rust: "#bd4f34", teal: "#327b75", gold: "#bf8a3d" };
const LOCATIONS = {
  "Saudi Arabia": [23.8859, 45.0792], Iraq: [33.2232, 43.6793], "United Arab Emirates": [23.4241, 53.8478], Kuwait: [29.3117, 47.4818], Qatar: [25.3548, 51.1839], Iran: [32.4279, 53.688], China: [35.8617, 104.1954], India: [20.5937, 78.9629], Japan: [36.2048, 138.2529], "South Korea": [35.9078, 127.7669], Singapore: [1.3521, 103.8198], Thailand: [15.87, 100.9925], Pakistan: [30.3753, 69.3451], Germany: [51.1657, 10.4515], "United States": [37.0902, -95.7129]
};
const number = (row, key) => Number(row[key]) || 0;
const byId = (id) => document.getElementById(id);
let allRows = [];
let activeView = "map";
let currentRows = [];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (char === '"' && quoted && text[index + 1] === '"') { cell += '"'; index += 1; }
    else if (char === '"') quoted = !quoted;
    else if (char === "," && !quoted) { row.push(cell); cell = ""; }
    else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[index + 1] === "\n") index += 1;
      row.push(cell); cell = "";
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
    } else cell += char;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const headers = rows.shift()?.map((header) => header.trim()) ?? [];
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, (values[index] ?? "").trim()])));
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

function initializeFilters() {
  const regions = [...new Set(allRows.map((row) => row.Region))].sort();
  for (const region of regions) byId("regionFilter").add(new Option(region, region));
  const risks = [...new Set(allRows.map((row) => row.Economic_Impact_Risk))].sort((a, b) => RISK_ORDER.indexOf(a) - RISK_ORDER.indexOf(b));
  byId("riskFilters").innerHTML = risks.map((risk) => `<label class="risk-option"><input type="checkbox" value="${escapeHtml(risk)}" checked /><span>${escapeHtml(risk)}</span></label>`).join("");
  document.querySelectorAll("#regionFilter, #roleFilter, #dependencyMin, #dependencyMax, #riskFilters input").forEach((control) => control.addEventListener("input", updateDashboard));
  byId("dependencyMin").addEventListener("input", keepRangeValid);
  byId("dependencyMax").addEventListener("input", keepRangeValid);
  byId("resetFilters").addEventListener("click", resetFilters);
  byId("mobileToggle").addEventListener("click", () => {
    const expanded = byId("mobileToggle").getAttribute("aria-expanded") !== "true";
    byId("mobileToggle").setAttribute("aria-expanded", String(expanded));
    byId("mobileToggle").innerHTML = `Filters and scenario <span aria-hidden="true">${expanded ? "⌃" : "⌄"}</span>`;
    document.querySelector(".sidebar").classList.toggle("open", expanded);
  });
  byId("daysInput").addEventListener("input", () => { byId("daysValue").value = byId("daysInput").value; updateDashboard(); });
  byId("priceInput").addEventListener("input", () => { byId("priceValue").value = byId("priceInput").value; updateDashboard(); });
  byId("downloadCsv").addEventListener("click", downloadFilteredCsv);
  document.querySelectorAll(".view-tab").forEach((tab) => tab.addEventListener("click", () => activateView(tab.dataset.view)));
}

function keepRangeValid(event) {
  const min = byId("dependencyMin");
  const max = byId("dependencyMax");
  if (Number(min.value) > Number(max.value)) {
    if (event.target === min) max.value = min.value;
    else min.value = max.value;
  }
  updateDashboard();
}

function resetFilters() {
  byId("regionFilter").value = "All";
  byId("roleFilter").value = "All";
  byId("dependencyMin").value = 0;
  byId("dependencyMax").value = 100;
  document.querySelectorAll("#riskFilters input").forEach((input) => { input.checked = true; });
  updateDashboard();
}

function filteredRows() {
  const activeRisks = new Set([...document.querySelectorAll("#riskFilters input:checked")].map((input) => input.value));
  const min = Number(byId("dependencyMin").value);
  const max = Number(byId("dependencyMax").value);
  return allRows.filter((row) => (byId("regionFilter").value === "All" || row.Region === byId("regionFilter").value)
    && (byId("roleFilter").value === "All" || row.Role === byId("roleFilter").value)
    && activeRisks.has(row.Economic_Impact_Risk)
    && number(row, "Hormuz_Transit_Dependency_Pct") >= min
    && number(row, "Hormuz_Transit_Dependency_Pct") <= max);
}

function updateDashboard() {
  currentRows = filteredRows();
  byId("dependencyLabel").textContent = `${byId("dependencyMin").value}–${byId("dependencyMax").value}%`;
  renderMetrics(currentRows);
  renderTable(currentRows);
  if (currentRows.length) {
    renderScenario(currentRows);
    renderActiveCharts();
  } else {
    clearCharts();
  }
}

function renderMetrics(rows) {
  const volume = rows.reduce((sum, row) => sum + number(row, "Daily_Volume_Affected_Mbd"), 0);
  const dependency = rows.length ? rows.reduce((sum, row) => sum + number(row, "Hormuz_Transit_Dependency_Pct"), 0) / rows.length : 0;
  const gdp = rows.length ? rows.reduce((sum, row) => sum + number(row, "Estimated_GDP_Impact_Pct"), 0) / rows.length : 0;
  byId("kpiCountries").textContent = `${rows.length} / ${allRows.length}`;
  byId("kpiVolume").textContent = volume.toFixed(1);
  byId("kpiVolumeFoot").textContent = `${(volume / 26.3 * 100).toFixed(1)}% of the full sample`;
  byId("kpiDependency").textContent = dependency.toFixed(1);
  byId("kpiPeak").textContent = `Peak ${rows.length ? Math.max(...rows.map((row) => number(row, "Hormuz_Transit_Dependency_Pct"))).toFixed(0) : 0}%`;
  byId("kpiGdp").textContent = gdp.toFixed(1);
  byId("kpiCritical").textContent = `${rows.filter((row) => row.Economic_Impact_Risk === "Critical").length} critical-tier countries`;
}

function baseLayout(extra = {}) {
  return {
    autosize: true, paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: "DM Sans, Segoe UI, sans-serif", size: 10, color: COLORS.muted },
    margin: { l: 55, r: 18, t: 17, b: 45 },
    xaxis: { gridcolor: COLORS.grid, zerolinecolor: COLORS.grid, linecolor: COLORS.grid, automargin: true },
    yaxis: { gridcolor: COLORS.grid, zerolinecolor: COLORS.grid, linecolor: COLORS.grid, automargin: true },
    legend: { orientation: "h", y: 1.1, x: 0, font: { size: 9 } },
    hoverlabel: { bgcolor: "#202b32", font: { color: "#ffffff", size: 10 } },
    ...extra
  };
}
const chartConfig = { responsive: true, displayModeBar: false };
function chart(id, data, layout) { return Plotly.react(id, data, layout, chartConfig); }

function renderMap(rows) {
  const points = rows.filter((row) => LOCATIONS[row.Country]);
  return chart("mapChart", [{
    type: "scattergeo", mode: "markers", text: points.map((row) => row.Country),
    lat: points.map((row) => LOCATIONS[row.Country][0]), lon: points.map((row) => LOCATIONS[row.Country][1]),
    customdata: points.map((row) => [row.Region, row.Role, number(row, "Hormuz_Transit_Dependency_Pct"), number(row, "Daily_Volume_Affected_Mbd"), number(row, "Estimated_GDP_Impact_Pct"), row.Economic_Impact_Risk, row.Alternative_Route_Availability]),
    marker: {
      size: points.map((row) => Math.max(7, Math.sqrt(number(row, "Daily_Volume_Affected_Mbd")) * 12)),
      color: points.map((row) => Math.abs(number(row, "Estimated_GDP_Impact_Pct"))),
      colorscale: [[0, "#e8e9df"], [1, COLORS.rust]], cmin: 0,
      cmax: Math.max(...points.map((row) => Math.abs(number(row, "Estimated_GDP_Impact_Pct")))) || 1,
      colorbar: { title: { text: "GDP impact (%)", side: "right" }, thickness: 10, outlinewidth: 0, tickfont: { size: 8 } },
      opacity: 0.84, line: { width: 1.3, color: "#ffffff" }
    },
    hovertemplate: "<b>%{text}</b><br>%{customdata[0]} · %{customdata[1]}<br>Dependency: %{customdata[2]:.0f}%<br>Volume: %{customdata[3]:.1f} Mbd<br>GDP impact: %{customdata[4]:.1f}%<br>Risk: %{customdata[5]}<br>Alternative route: %{customdata[6]}<extra></extra>"
  }], baseLayout({
    margin: { l: 0, r: 0, t: 5, b: 5 }, showlegend: false,
    geo: { projection: { type: "natural earth" }, showframe: false, showcoastlines: true, coastlinecolor: "#c9d2cb", showland: true, landcolor: "#e7ebe4", showocean: true, oceancolor: "#edf2ef", showcountries: true, countrycolor: "#d5dcd5", showlakes: true, lakecolor: "#edf2ef", bgcolor: "rgba(0,0,0,0)" }
  }));
}

function renderBar(id, rows, key, color, suffix, label) {
  const sorted = [...rows].sort((a, b) => number(a, key) - number(b, key));
  return chart(id, [{ type: "bar", orientation: "h", y: sorted.map((row) => row.Country), x: sorted.map((row) => number(row, key)), marker: { color: sorted.map((row) => row.Role === "Exporter" ? COLORS.rust : COLORS.teal), opacity: 0.88 }, customdata: sorted.map((row) => row.Role), hovertemplate: `%{y}<br>${label}: %{x:.1f}${suffix}<br>%{customdata}<extra></extra>` }], baseLayout({ margin: { l: 115, r: 22, t: 8, b: 38 }, showlegend: false, xaxis: { title: label, gridcolor: COLORS.grid, zerolinecolor: COLORS.grid, automargin: true }, yaxis: { gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 9 } }, bargap: 0.28 }));
}

function renderRoleChart(rows) {
  const roles = ["Exporter", "Importer"].filter((role) => rows.some((row) => row.Role === role));
  return chart("gdpRoleChart", roles.map((role) => {
    const values = rows.filter((row) => row.Role === role).map((row) => number(row, "Estimated_GDP_Impact_Pct"));
    return { type: "box", name: role, y: values, boxpoints: "all", jitter: 0.25, pointpos: 0, marker: { color: role === "Exporter" ? COLORS.rust : COLORS.teal, size: 7 }, line: { color: role === "Exporter" ? COLORS.rust : COLORS.teal }, fillcolor: role === "Exporter" ? "rgba(189,79,52,.15)" : "rgba(50,123,117,.15)", hovertemplate: `${role}<br>GDP impact: %{y:.1f}%<extra></extra>` };
  }), baseLayout({ margin: { l: 55, r: 20, t: 10, b: 45 }, showlegend: false, yaxis: { title: "Estimated GDP impact (%)", gridcolor: COLORS.grid, zerolinecolor: COLORS.grid, automargin: true } }));
}

function linearFit(points) {
  const meanX = points.reduce((sum, point) => sum + point.x, 0) / points.length;
  const meanY = points.reduce((sum, point) => sum + point.y, 0) / points.length;
  const numerator = points.reduce((sum, point) => sum + (point.x - meanX) * (point.y - meanY), 0);
  const denominator = points.reduce((sum, point) => sum + (point.x - meanX) ** 2, 0);
  const slope = denominator ? numerator / denominator : 0;
  return { slope, intercept: meanY - slope * meanX };
}

function correlation(rows, first, second) {
  if (rows.length < 2) return 0;
  const xs = rows.map((row) => number(row, first));
  const ys = rows.map((row) => number(row, second));
  const meanX = xs.reduce((sum, value) => sum + value, 0) / xs.length;
  const meanY = ys.reduce((sum, value) => sum + value, 0) / ys.length;
  const numerator = xs.reduce((sum, value, index) => sum + (value - meanX) * (ys[index] - meanY), 0);
  const denominator = Math.sqrt(xs.reduce((sum, value) => sum + (value - meanX) ** 2, 0) * ys.reduce((sum, value) => sum + (value - meanY) ** 2, 0));
  return denominator ? numerator / denominator : 0;
}

function renderRelationships(rows) {
  const points = rows.map((row) => ({ x: number(row, "Hormuz_Transit_Dependency_Pct"), y: number(row, "Estimated_GDP_Impact_Pct"), row }));
  const fit = linearFit(points);
  const range = points.map((point) => point.x);
  const min = Math.min(...range);
  const max = Math.max(...range);
  const traces = ["Exporter", "Importer"].filter((role) => points.some((point) => point.row.Role === role)).map((role) => {
    const subset = points.filter((point) => point.row.Role === role);
    return { type: "scatter", mode: "markers", name: role, x: subset.map((point) => point.x), y: subset.map((point) => point.y), text: subset.map((point) => point.row.Country), marker: { size: subset.map((point) => 8 + Math.sqrt(number(point.row, "Daily_Volume_Affected_Mbd")) * 3), color: role === "Exporter" ? COLORS.rust : COLORS.teal, opacity: 0.82, line: { color: "#fff", width: 1 } }, hovertemplate: "<b>%{text}</b><br>Dependency: %{x:.0f}%<br>GDP impact: %{y:.1f}%<extra></extra>" };
  });
  if (points.length > 1) traces.push({ type: "scatter", mode: "lines", name: "Linear trend", x: [min, max], y: [fit.slope * min + fit.intercept, fit.slope * max + fit.intercept], line: { color: COLORS.gold, dash: "dash", width: 2 }, hoverinfo: "skip" });
  const scatter = chart("scatterChart", traces, baseLayout({ margin: { l: 58, r: 18, t: 14, b: 48 }, xaxis: { title: "Transit dependency (%)", gridcolor: COLORS.grid, zerolinecolor: COLORS.grid }, yaxis: { title: "Estimated GDP impact (%)", gridcolor: COLORS.grid, zerolinecolor: COLORS.grid } }));
  const metrics = [
    ["Dependency", "Hormuz_Transit_Dependency_Pct"],
    ["Daily volume", "Daily_Volume_Affected_Mbd"],
    ["GDP impact", "Estimated_GDP_Impact_Pct"]
  ];
  const matrix = metrics.map(([, a]) => metrics.map(([, b]) => correlation(rows, a, b)));
  const heat = chart("correlationChart", [{ type: "heatmap", x: metrics.map(([label]) => label), y: metrics.map(([label]) => label), z: matrix, zmin: -1, zmax: 1, colorscale: [[0, "#437d76"], [0.5, "#f3f4ee"], [1, "#bd4f34"]], text: matrix.map((line) => line.map((value) => value.toFixed(2))), texttemplate: "%{text}", hovertemplate: "%{y} × %{x}<br>Correlation: %{z:.2f}<extra></extra>", colorbar: { thickness: 10, outlinewidth: 0, tickfont: { size: 8 } } }], baseLayout({ margin: { l: 95, r: 35, t: 15, b: 65 }, xaxis: { side: "bottom", tickangle: -18 }, yaxis: { autorange: "reversed" } }));
  return Promise.all([scatter, heat]);
}

function renderScenario(rows) {
  const days = Number(byId("daysInput").value);
  const price = Number(byId("priceInput").value);
  const simulation = rows.map((row) => ({ ...row, barrels: number(row, "Daily_Volume_Affected_Mbd") * days, value: number(row, "Daily_Volume_Affected_Mbd") * days * price / 1000 }));
  const barrels = simulation.reduce((sum, row) => sum + row.barrels, 0);
  const value = simulation.reduce((sum, row) => sum + row.value, 0);
  byId("scenarioBarrels").textContent = `${barrels.toFixed(1)} million bbl`;
  byId("scenarioValue").textContent = `$${value.toFixed(1)} billion`;
  byId("scenarioDaily").textContent = `$${(value / days * 1000).toFixed(1)} million/day`;
  const sorted = simulation.sort((a, b) => a.value - b.value);
  return chart("scenarioChart", [{ type: "bar", orientation: "h", y: sorted.map((row) => row.Country), x: sorted.map((row) => row.value), marker: { color: sorted.map((row) => row.Role === "Exporter" ? COLORS.rust : COLORS.teal) }, customdata: sorted.map((row) => row.Role), hovertemplate: "%{y}<br>Gross flow value: $%{x:.2f}B<br>%{customdata}<extra></extra>" }], baseLayout({ margin: { l: 115, r: 35, t: 10, b: 44 }, showlegend: false, xaxis: { title: `Gross flow value over ${days} days (USD billions)`, gridcolor: COLORS.grid, zerolinecolor: COLORS.grid }, yaxis: { gridcolor: "rgba(0,0,0,0)", automargin: true, tickfont: { size: 9 } }, bargap: 0.28 }));
}

function renderTable(rows) {
  const sorted = [...rows].sort((a, b) => number(b, "Hormuz_Transit_Dependency_Pct") - number(a, "Hormuz_Transit_Dependency_Pct"));
  byId("dataRows").innerHTML = sorted.map((row) => {
    const riskClass = `risk-${String(row.Economic_Impact_Risk).toLowerCase()}`;
    return `<tr><td class="country-name">${escapeHtml(row.Country)}</td><td>${escapeHtml(row.Region)}</td><td>${escapeHtml(row.Role)}</td><td>${number(row, "Hormuz_Transit_Dependency_Pct").toFixed(0)}%</td><td>${number(row, "Daily_Volume_Affected_Mbd").toFixed(1)}</td><td>${number(row, "Estimated_GDP_Impact_Pct").toFixed(1)}%</td><td><span class="risk-badge ${riskClass}">${escapeHtml(row.Economic_Impact_Risk)}</span></td><td>${escapeHtml(row.Alternative_Route_Availability)}</td></tr>`;
  }).join("");
  byId("tableCount").textContent = `Showing ${rows.length} of ${allRows.length} countries · sorted by transit dependency`;
}

function renderActiveCharts() {
  if (!window.Plotly || !currentRows.length) return;
  if (activeView === "map") renderMap(currentRows);
  if (activeView === "rankings") Promise.all([
    renderBar("dependencyChart", currentRows, "Hormuz_Transit_Dependency_Pct", COLORS.rust, "%", "Dependency (%)"),
    renderBar("volumeChart", currentRows, "Daily_Volume_Affected_Mbd", COLORS.teal, " Mbd", "Volume (Mbd)"),
    renderRoleChart(currentRows)
  ]);
  if (activeView === "correlation") renderRelationships(currentRows);
  if (activeView === "scenario") renderScenario(currentRows);
  requestAnimationFrame(() => document.querySelectorAll(`#view-${activeView} .chart`).forEach((element) => { if (element.data) Plotly.Plots.resize(element); }));
}

function clearCharts() {
  document.querySelectorAll(".chart").forEach((element) => { element.innerHTML = "<div class='empty-chart'>No countries match these filters.</div>"; });
  byId("scenarioBarrels").textContent = "—";
  byId("scenarioValue").textContent = "—";
  byId("scenarioDaily").textContent = "—";
}

function activateView(view) {
  activeView = view;
  document.querySelectorAll(".view-tab").forEach((tab) => {
    const selected = tab.dataset.view === view;
    tab.classList.toggle("active", selected);
    tab.setAttribute("aria-selected", String(selected));
  });
  document.querySelectorAll(".view-panel").forEach((panel) => {
    const selected = panel.id === `view-${view}`;
    panel.hidden = !selected;
    panel.classList.toggle("active", selected);
  });
  renderActiveCharts();
}

function downloadFilteredCsv() {
  if (!currentRows.length) return;
  const headers = Object.keys(allRows[0]);
  const quote = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;
  const csv = [headers.map(quote).join(","), ...currentRows.map((row) => headers.map((header) => quote(row[header])).join(","))].join("\r\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "strait_of_hormuz_filtered_data.csv";
  document.body.append(link);
  link.click();
  window.setTimeout(() => {
    URL.revokeObjectURL(url);
    link.remove();
  }, 1000);
}

async function start() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`Dataset request failed with status ${response.status}.`);
    allRows = parseCsv(await response.text());
    if (!allRows.length) throw new Error("The country dataset is empty.");
    initializeFilters();
    byId("loadMessage").hidden = true;
    updateDashboard();
  } catch (error) {
    byId("loadMessage").hidden = true;
    byId("errorMessage").hidden = false;
    byId("errorMessage").textContent = `Dashboard data could not be loaded. ${error.message} Check that the cleaned CSV is deployed beside index.html.`;
  }
}

start();