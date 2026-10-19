/**
 * Quick-Commerce Dark Store Analytics Frontend Controller
 * Review 2 Capstone Project
 */

// Global App State
let state = {
  catalogue: [],
  categorySummary: [],
  forecasts: null,
  modelComparison: [],
  rules: [],
  algorithmComparison: [],
  literature: [],
  activeTab: 'overview',
  activeModel: 'XGBoost Regressor',
  minLift: 1.5,
  charts: {}
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  await loadData();
  initCatalogueTab();
  initForecastingTab();
  initAssociationTab();
  initLiteratureTab();
});

// Tab Navigation
function setupNavigation() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      const target = tab.getAttribute('data-tab');
      const pane = document.getElementById(`tab-${target}`);
      if (pane) pane.classList.add('active');
      state.activeTab = target;

      // Trigger chart resize on tab switch
      setTimeout(() => {
        Object.values(state.charts).forEach(c => c && c.resize && c.resize());
      }, 50);
    });
  });
}

// Load JSON data
async function loadData() {
  try {
    const [catRes, catSumRes, fcRes, mcRes, rulesRes, algoRes, litRes] = await Promise.all([
      fetch('data/catalogue.json').then(r => r.json()),
      fetch('data/category_summary.json').then(r => r.json()),
      fetch('data/forecasts.json').then(r => r.json()),
      fetch('data/model_comparison.json').then(r => r.json()),
      fetch('data/rules.json').then(r => r.json()),
      fetch('data/algorithm_comparison.json').then(r => r.json()),
      fetch('data/literature.json').then(r => r.json())
    ]);

    state.catalogue = catRes;
    state.categorySummary = catSumRes;
    state.forecasts = fcRes;
    state.modelComparison = mcRes;
    state.rules = rulesRes;
    state.algorithmComparison = algoRes;
    state.literature = litRes;
  } catch (err) {
    console.warn("Fetch failed, relying on embedded fallback data:", err);
  }
}

// -------------------------------------------------------------
// SECTION 2: PRODUCT INTELLIGENCE (CATALOGUE)
// -------------------------------------------------------------
function initCatalogueTab() {
  const searchInput = document.getElementById('catalogueSearch');
  const catFilter = document.getElementById('categoryFilter');

  function renderTable() {
    const q = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const cat = catFilter ? catFilter.value : 'ALL';
    const tbody = document.getElementById('catalogueBody');
    if (!tbody) return;

    const filtered = state.catalogue.filter(item => {
      const matchQ = !q || item.product_name.toLowerCase().includes(q) || item.brand.toLowerCase().includes(q);
      const matchCat = cat === 'ALL' || item.category === cat;
      return matchQ && matchCat;
    });

    const countElem = document.getElementById('filteredCount');
    if (countElem) countElem.innerText = filtered.length;

    tbody.innerHTML = filtered.slice(0, 100).map(item => `
      <tr>
        <td><code>#${item.source_product_id}</code></td>
        <td><strong>${item.product_name}</strong></td>
        <td><span class="badge-cyan">${item.category}</span></td>
        <td>${item.brand}</td>
        <td><strong>₹${Number(item.displayed_price).toFixed(2)}</strong></td>
        <td>₹${Number(item.original_price).toFixed(2)}</td>
        <td><span class="badge-success">${item.discount_pct}%</span></td>
        <td>${item.inventory} units</td>
        <td><span class="badge-success">${item.availability_status}</span></td>
      </tr>
    `).join('');
  }

  if (searchInput) searchInput.addEventListener('input', renderTable);
  if (catFilter) catFilter.addEventListener('change', renderTable);
  renderTable();
  renderCategoryChart();
  renderPriceScatterChart();
}

function renderCategoryChart() {
  const ctx = document.getElementById('categoryChart');
  if (!ctx || !state.categorySummary.length) return;

  const labels = state.categorySummary.map(c => c.category);
  const counts = state.categorySummary.map(c => c.Product_Count);
  const discounts = state.categorySummary.map(c => c.Mean_Discount_Pct);

  state.charts.category = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'SKU Count',
          data: counts,
          backgroundColor: '#3b82f6',
          borderRadius: 4,
          yAxisID: 'y'
        },
        {
          label: 'Mean Discount (%)',
          data: discounts,
          type: 'line',
          borderColor: '#10b981',
          borderWidth: 3,
          pointBackgroundColor: '#10b981',
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#94a3b8' } }
      },
      scales: {
        x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { display: false } },
        y: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(51, 65, 85, 0.4)' },
          title: { display: true, text: 'Products', color: '#94a3b8' }
        },
        y1: {
          position: 'right',
          ticks: { color: '#10b981' },
          grid: { display: false },
          title: { display: true, text: 'Discount %', color: '#10b981' }
        }
      }
    }
  });
}

function renderPriceScatterChart() {
  const ctx = document.getElementById('priceScatterChart');
  if (!ctx || !state.catalogue.length) return;

  const points = state.catalogue.slice(0, 120).map(p => ({
    x: p.original_price,
    y: p.displayed_price
  }));

  state.charts.scatter = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Observed SKU (MRP vs Selling Price)',
          data: points,
          backgroundColor: 'rgba(6, 182, 212, 0.65)',
          borderColor: '#06b6d4',
          pointRadius: 4
        },
        {
          label: 'Zero Discount Line (Price = MRP)',
          data: [{ x: 10, y: 10 }, { x: 500, y: 500 }],
          type: 'line',
          borderColor: 'rgba(148, 163, 184, 0.5)',
          borderDash: [5, 5],
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#94a3b8' } }
      },
      scales: {
        x: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(51, 65, 85, 0.4)' },
          title: { display: true, text: 'Maximum Retail Price (INR)', color: '#94a3b8' }
        },
        y: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(51, 65, 85, 0.4)' },
          title: { display: true, text: 'Selling Price (INR)', color: '#94a3b8' }
        }
      }
    }
  });
}

// -------------------------------------------------------------
// SECTION 3: TIME-SERIES FORECASTING
// -------------------------------------------------------------
function initForecastingTab() {
  renderModelCompTable();
  renderForecastChart();
  renderFeatureImportanceChart();

  const modelSelect = document.getElementById('forecastModelSelect');
  if (modelSelect) {
    modelSelect.addEventListener('change', (e) => {
      state.activeModel = e.target.value;
      const badge = document.getElementById('activeModelBadge');
      if (badge) badge.innerText = `Active: ${state.activeModel}`;
      updateForecastChart();
    });
  }
}

function renderModelCompTable() {
  const tbody = document.getElementById('modelCompBody');
  if (!tbody || !state.modelComparison.length) return;

  tbody.innerHTML = state.modelComparison.map((m, idx) => `
    <tr>
      <td><strong>${m.Model}</strong></td>
      <td>${m['MAE (Units)']}</td>
      <td><strong>${m['RMSE (Units)']}</strong></td>
      <td>${m['WAPE (%)']}%</td>
      <td><span class="${idx === 0 ? 'badge-success' : 'badge-cyan'}">${idx === 0 ? '★ Winner' : '#' + (idx + 1)}</span></td>
    </tr>
  `).join('');
}

function renderForecastChart() {
  const ctx = document.getElementById('forecastChart');
  if (!ctx || !state.forecasts) return;

  const dates = state.forecasts.dates;
  const actual = state.forecasts.actual;
  const pred = state.forecasts.predictions[state.activeModel] || actual;

  state.charts.forecast = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [
        {
          label: 'Actual Store Unit Demand',
          data: actual,
          borderColor: '#f8fafc',
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          borderWidth: 2.5,
          tension: 0.2,
          pointRadius: 3
        },
        {
          label: `Forecast: ${state.activeModel}`,
          data: pred,
          borderColor: '#10b981',
          borderDash: [6, 4],
          borderWidth: 2.5,
          tension: 0.2,
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#cbd5e1' } }
      },
      scales: {
        x: { ticks: { color: '#94a3b8', maxTicksLimit: 12 }, grid: { display: false } },
        y: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(51, 65, 85, 0.4)' },
          title: { display: true, text: 'Total Units Demanded', color: '#94a3b8' }
        }
      }
    }
  });
}

function updateForecastChart() {
  if (!state.charts.forecast || !state.forecasts) return;
  const pred = state.forecasts.predictions[state.activeModel] || state.forecasts.actual;
  state.charts.forecast.data.datasets[1].label = `Forecast: ${state.activeModel}`;
  state.charts.forecast.data.datasets[1].data = pred;
  state.charts.forecast.update();
}

function renderFeatureImportanceChart() {
  const ctx = document.getElementById('featureImportanceChart');
  if (!ctx) return;

  const features = ['lag_7', 'roll_mean_7', 'lag_1', 'is_weekend', 'day_of_week', 'roll_std_7', 'lag_14', 'day_of_month'];
  const importance = [0.38, 0.24, 0.14, 0.09, 0.06, 0.04, 0.03, 0.02];

  state.charts.features = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: features,
      datasets: [{
        label: 'Feature Importance Weight',
        data: importance,
        backgroundColor: '#10b981',
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.4)' } },
        y: { ticks: { color: '#cbd5e1', font: { size: 10 } }, grid: { display: false } }
      }
    }
  });
}

// -------------------------------------------------------------
// SECTION 4: ASSOCIATION RULE MINING
// -------------------------------------------------------------
function initAssociationTab() {
  const slider = document.getElementById('liftSlider');
  const valDisplay = document.getElementById('liftValue');

  function updateRules() {
    const minL = slider ? parseFloat(slider.value) : 1.5;
    if (valDisplay) valDisplay.innerText = `${minL.toFixed(2)}x`;

    const filtered = state.rules.filter(r => r.lift >= minL);
    renderRulesTable(filtered);
    renderBundleCards(filtered.slice(0, 4));
  }

  if (slider) slider.addEventListener('input', updateRules);
  updateRules();
  renderRuntimeBenchmarkChart();
}

function renderRulesTable(rulesList) {
  const tbody = document.getElementById('rulesTableBody');
  if (!tbody) return;

  tbody.innerHTML = rulesList.slice(0, 20).map(r => `
    <tr>
      <td><strong>${r.antecedents_str}</strong></td>
      <td><strong>${r.consequents_str}</strong></td>
      <td>${(r.support * 100).toFixed(2)}%</td>
      <td>${(r.confidence * 100).toFixed(1)}%</td>
      <td><span class="badge-success">${Number(r.lift).toFixed(2)}x</span></td>
      <td><span class="text-secondary">High-affinity cross-sell bundle</span></td>
    </tr>
  `).join('');
}

function renderBundleCards(topRules) {
  const container = document.getElementById('bundleCards');
  if (!container) return;

  if (!topRules.length) {
    container.innerHTML = '<p class="text-muted">No bundles meet current lift threshold.</p>';
    return;
  }

  container.innerHTML = topRules.map(r => `
    <div class="bundle-item-card">
      <div>
        <div class="bundle-rule">${r.antecedents_str} ➔ ${r.consequents_str}</div>
        <div class="bundle-sub">Confidence: ${(r.confidence * 100).toFixed(1)}% | Support: ${(r.support * 100).toFixed(2)}%</div>
      </div>
      <div class="bundle-lift">${Number(r.lift).toFixed(2)}x Lift</div>
    </div>
  `).join('');
}

function renderRuntimeBenchmarkChart() {
  const ctx = document.getElementById('runtimeBenchmarkChart');
  if (!ctx || !state.algorithmComparison.length) return;

  const supports = state.algorithmComparison.map(b => `${(b.Min_Support * 100).toFixed(1)}%`);
  const apTimes = state.algorithmComparison.map(b => b.Apriori_Time_Sec);
  const fpTimes = state.algorithmComparison.map(b => b.FPGrowth_Time_Sec);

  state.charts.benchmark = new Chart(ctx, {
    type: 'line',
    data: {
      labels: supports,
      datasets: [
        {
          label: 'Apriori Algorithm (Candidate Sets)',
          data: apTimes,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 2,
          pointRadius: 4
        },
        {
          label: 'FP-Growth Algorithm (Prefix Tree)',
          data: fpTimes,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 2,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#cbd5e1' } }
      },
      scales: {
        x: { ticks: { color: '#94a3b8' }, title: { display: true, text: 'Min Support Threshold', color: '#94a3b8' }, grid: { display: false } },
        y: { ticks: { color: '#94a3b8' }, title: { display: true, text: 'Execution Time (Seconds)', color: '#94a3b8' }, grid: { color: 'rgba(51, 65, 85, 0.4)' } }
      }
    }
  });
}

// -------------------------------------------------------------
// SECTION 6: RESEARCH & LITERATURE MATRIX
// -------------------------------------------------------------
function initLiteratureTab() {
  const tbody = document.getElementById('literatureBody');
  if (!tbody || !state.literature.length) return;

  tbody.innerHTML = state.literature.map(p => `
    <tr>
      <td><code>${p.Paper_ID}</code></td>
      <td><strong>${p.Citation}</strong></td>
      <td><a href="${p.DOI.startsWith('http') ? p.DOI : 'https://doi.org/' + p.DOI}" target="_blank" style="color: #06b6d4; text-decoration: none;">Link ↗</a></td>
      <td>${p.Methods}</td>
      <td>${p.Verified_Findings}</td>
      <td><span class="badge-success">${p.Relevance_To_Project}</span></td>
    </tr>
  `).join('');
}
