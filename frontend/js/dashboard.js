const farmerDashboard = {
  farms: [],
  currentFarmId: null,

  async init() {
    this.setupTabs();
    await this.loadStats();
    await this.loadFarms();
    this.setupFarmForm();
    this.checkUrlTab();
  },

  setupTabs() {
    const tabs = document.querySelectorAll('#dashboard-tabs .tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
        const content = document.getElementById(`tab-${tab.dataset.tab}`);
        if (content) content.style.display = 'block';
        if (tab.dataset.tab === 'carbon') this.loadCarbonScores();
        if (tab.dataset.tab === 'satellite') {
          if (this.farms.length > 0) {
            this.loadSatelliteData(this.farms[0].id);
          } else {
            document.querySelector('#satellite-metrics').innerHTML = '<p style="color:var(--color-text-muted)">Register a farm first</p>';
          }
        }
      });
    });
  },

  checkUrlTab() {
    const params = new URLSearchParams(window.location.search);
    const tab = params.get('tab');
    if (tab) {
      const tabEl = document.querySelector(`[data-tab="${tab}"]`);
      if (tabEl) tabEl.click();
    }
  },

  async loadStats() {
    try {
      const scores = await api.get('/carbon/my-scores');
      const totalCarbon = scores.reduce((sum, s) => sum + (s.carbon_offset_tonnes || 0), 0);
      const avgSustain = scores.length > 0
        ? scores.reduce((sum, s) => sum + (s.sustainability_score || 0), 0) / scores.length
        : 0;

      const farmsResp = document.getElementById('stat-farms');
      const carbonResp = document.getElementById('stat-carbon');
      const sustainResp = document.getElementById('stat-sustainability');
      const earnResp = document.getElementById('stat-earnings');

      const farms = await api.get('/farms');
      if (farmsResp) farmsResp.textContent = farms.total || farms.farms?.length || 0;
      if (carbonResp) carbonResp.textContent = totalCarbon.toFixed(1);
      if (sustainResp) sustainResp.textContent = avgSustain.toFixed(0);
      if (earnResp) earnResp.textContent = scores.length;
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  },

  async loadFarms() {
    try {
      const loading = document.getElementById('farms-loading');
      const empty = document.getElementById('farms-empty');
      const list = document.getElementById('farms-list');
      const grid = document.getElementById('farms-grid');

      const data = await api.get('/farms');
      this.farms = data.farms || data || [];

      loading.style.display = 'none';

      if (this.farms.length === 0) {
        empty.style.display = 'block';
        list.style.display = 'none';
        return;
      }

      empty.style.display = 'none';
      list.style.display = 'block';
      grid.innerHTML = '';

      this.farms.forEach(farm => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
            <div>
              <h3 style="font-size:18px;font-weight:600;margin-bottom:4px">${farm.name}</h3>
              <span style="font-size:13px;color:var(--color-text-muted)">${farm.country} &middot; ${farm.area_hectares} ha</span>
            </div>
            <span class="badge ${farm.is_verified ? 'badge-green' : 'badge-amber'}">${farm.is_verified ? 'Verified' : 'Pending'}</span>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:14px;color:var(--color-text-secondary);margin-bottom:12px">
            <div>Crops: ${farm.crop_types || 'N/A'}</div>
            <div>Soil: ${farm.soil_type || 'N/A'}</div>
            <div>Irrigation: ${farm.irrigation_type || 'N/A'}</div>
            <div>Status: ${farm.status}</div>
          </div>
          <div style="display:flex;gap:8px">
            <button class="btn btn-primary btn-sm estimate-btn" data-farm-id="${farm.id}">Estimate Carbon</button>
            <button class="btn btn-secondary btn-sm view-satellite-btn" data-farm-id="${farm.id}">Satellite View</button>
          </div>
          <div id="carbon-result-${farm.id}" style="margin-top:12px"></div>
        `;
        grid.appendChild(card);
      });

      document.querySelectorAll('.estimate-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const farmId = btn.dataset.farmId;
          const resultDiv = document.getElementById(`carbon-result-${farmId}`);
          resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
          try {
            const score = await api.post('/carbon/estimate', { farm_id: farmId });
            resultDiv.innerHTML = `
              <div class="alert alert-success">
                <strong>Carbon Score: ${score.carbon_offset_tonnes} tCO&#8322;e</strong> &middot;
                Sustainability: ${score.sustainability_score?.toFixed(0) || 'N/A'}/100 &middot;
                Confidence: ${(score.ai_confidence_level * 100).toFixed(0)}%
                <button class="btn btn-primary btn-sm" style="margin-left:auto" onclick="farmerDashboard.mintCredit('${score.id}')">Mint as NFT</button>
              </div>
            `;
          } catch (err) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
          }
        });
      });

      document.querySelectorAll('.view-satellite-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          this.loadSatelliteData(btn.dataset.farmId);
          const satTab = document.querySelector('[data-tab="satellite"]');
          if (satTab) satTab.click();
        });
      });
    } catch (err) {
      console.error('Failed to load farms:', err);
    }
  },

  async mintCredit(scoreId) {
    try {
      const result = await api.post(`/blockchain/mint/${scoreId}`);
      alert(`Carbon credit minted!\nTx: ${result.transaction_hash}`);
    } catch (err) {
      alert('Minting failed: ' + err.message);
    }
  },

  setupFarmForm() {
    const form = document.getElementById('farm-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = {
        name: document.getElementById('farm-name').value,
        description: document.getElementById('farm-description').value,
        country: document.getElementById('farm-country').value,
        area_hectares: parseFloat(document.getElementById('farm-area').value),
        latitude: parseFloat(document.getElementById('farm-lat').value) || 0,
        longitude: parseFloat(document.getElementById('farm-lon').value) || 0,
        crop_types: document.getElementById('farm-crops').value,
        soil_type: document.getElementById('farm-soil').value,
        irrigation_type: document.getElementById('farm-irrigation').value,
        fertilizer_usage: document.getElementById('farm-fertilizer').value,
        sustainability_practices: document.getElementById('farm-practices').value,
      };

      const errorEl = document.getElementById('farm-form-error');
      errorEl.textContent = '';

      if (!data.name || !data.area_hectares) {
        errorEl.textContent = 'Farm name and area are required';
        return;
      }

      try {
        await api.post('/farms', data);
        alert('Farm registered successfully!');
        form.reset();
        this.loadFarms();
        this.loadStats();
        document.querySelector('[data-tab="farms"]').click();
      } catch (err) {
        errorEl.textContent = err.message;
      }
    });
  },

  async loadCarbonScores() {
    const container = document.getElementById('carbon-content');
    try {
      const scores = await api.get('/carbon/my-scores');
      if (!scores || scores.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">&#9733;</div><div class="empty-state-title">No Carbon Scores Yet</div><p style="color:var(--color-text-muted)">Register a farm and generate your first carbon estimate.</p></div>';
        return;
      }
      let html = '<div class="data-table-container"><table class="data-table"><thead><tr><th>Date</th><th>Farm</th><th>CO&#8322; (tonnes)</th><th>Sustainability</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
      scores.forEach(s => {
        const date = new Date(s.created_at).toLocaleDateString();
        html += `<tr>
          <td>${date}</td>
          <td>${s.farm_id.substring(0, 8)}...</td>
          <td><strong>${s.carbon_offset_tonnes}</strong></td>
          <td>${s.sustainability_score?.toFixed(0) || 'N/A'}</td>
          <td><span class="badge ${s.status === 'approved' ? 'badge-green' : 'badge-amber'}">${s.status}</span></td>
          <td><button class="btn btn-outline btn-sm" onclick="farmerDashboard.mintCredit('${s.id}')">Mint NFT</button></td>
        </tr>`;
      });
      html += '</tbody></table></div>';
      container.innerHTML = html;
    } catch (err) {
      container.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  },

  async loadSatelliteData(farmId) {
    const metricsDiv = document.getElementById('satellite-metrics');
    metricsDiv.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
    try {
      const data = await api.get(`/satellite/analyze/${farmId}`);
      metricsDiv.innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <div style="padding:12px;background:var(--color-surface-alt);border-radius:var(--radius-sm)">
            <div style="font-size:12px;color:var(--color-text-muted)">NDVI</div>
            <div style="font-size:20px;font-weight:700">${data.ndvi_current?.toFixed(3) || 'N/A'}</div>
          </div>
          <div style="padding:12px;background:var(--color-surface-alt);border-radius:var(--radius-sm)">
            <div style="font-size:12px;color:var(--color-text-muted)">Land Health</div>
            <div style="font-size:20px;font-weight:700">${data.land_health?.toFixed(0) || 'N/A'}/100</div>
          </div>
          <div style="padding:12px;background:var(--color-surface-alt);border-radius:var(--radius-sm)">
            <div style="font-size:12px;color:var(--color-text-muted)">Vegetation Trend</div>
            <div style="font-size:20px;font-weight:700">${data.vegetation_trend || 'N/A'}</div>
          </div>
          <div style="padding:12px;background:var(--color-surface-alt);border-radius:var(--radius-sm)">
            <div style="font-size:12px;color:var(--color-text-muted)">Water Stress</div>
            <div style="font-size:20px;font-weight:700">${data.water_stress?.toFixed(3) || 'N/A'}</div>
          </div>
        </div>
        <div style="margin-top:12px;font-size:13px;color:var(--color-text-muted)">
          Analysis: ${new Date(data.analysis_date).toLocaleString()}
        </div>
      `;

      const ndviSeries = data.historical_data?.map(d => d.ndvi_value).filter(v => v != null) || [];
      this.drawNDVIChart(ndviSeries);
    } catch (err) {
      metricsDiv.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
    }
  },

  drawNDVIChart(values) {
    const canvas = document.getElementById('ndvi-chart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = rect.height;
    const pad = { top: 20, right: 20, bottom: 30, left: 40 };
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;

    ctx.clearRect(0, 0, w, h);

    if (!values || values.length === 0) {
      ctx.fillStyle = '#7a9a7a';
      ctx.font = '14px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('No NDVI data available', w / 2, h / 2);
      return;
    }

    const minVal = Math.min(...values) - 0.05;
    const maxVal = Math.max(...values) + 0.05;
    const range = maxVal - minVal || 1;

    ctx.strokeStyle = '#0d6b3e';
    ctx.lineWidth = 2;
    ctx.beginPath();

    values.forEach((v, i) => {
      const x = pad.left + (i / (values.length - 1 || 1)) * plotW;
      const y = pad.top + plotH - ((v - minVal) / range) * plotH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    ctx.fillStyle = '#0d6b3e20';
    ctx.lineTo(pad.left + plotW, pad.top + plotH);
    ctx.lineTo(pad.left, pad.top + plotH);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#4a6b4a';
    ctx.font = '11px Inter, sans-serif';
    ctx.textAlign = 'center';
    values.forEach((v, i) => {
      const x = pad.left + (i / (values.length - 1 || 1)) * plotW;
      const y = pad.top + plotH - ((v - minVal) / range) * plotH;
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#0d6b3e';
      ctx.fill();
    });

    ctx.fillStyle = '#7a9a7a';
    ctx.textAlign = 'center';
    ctx.fillText('Time →', w / 2, h - 4);
    ctx.save();
    ctx.translate(12, h / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('NDVI', 0, 0);
    ctx.restore();
  },
};
