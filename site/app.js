/* Brand Radar interactive marketing intelligence dashboard */
(() => {
  "use strict";

  const state = { data: null, brand: "all", time: "currently_active", tab: "overview", charts: {} };
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];

  const eur = (v) => (v == null ? "–" : "€" + Number(v).toLocaleString("de-DE", { maximumFractionDigits: 0 }));
  const num = (v, d = 0) => (v == null ? "–" : Number(v).toLocaleString("de-DE", { minimumFractionDigits: d, maximumFractionDigits: d }));
  const pct = (v, d = 1) => (v == null ? "–" : `${num(v, d)}%`);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const BRAND_COLORS = {
    ninja: "#10b981",    // Emerald
    cosori: "#f59e0b",   // Amber
    philips: "#2563eb",  // Blue
    tefal: "#ef4444",    // Red
  };
  const brandCol = (b) => BRAND_COLORS[b] || "#64748b";
  const alpha = (hex, a) => {
    const n = parseInt(hex.slice(1), 16);
    return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`;
  };

  function chart(id, config) {
    if (state.charts[id]) state.charts[id].destroy();
    const canvas = document.getElementById(id);
    if (!canvas) return null;
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    Chart.defaults.font.size = 12;
    config.options = Object.assign({ responsive: true, maintainAspectRatio: false, animation: false }, config.options || {});
    state.charts[id] = new Chart(canvas, config);
    return state.charts[id];
  }

  function table(el, headers, rows, opts = {}) {
    const t = typeof el === "string" ? $(el) : el;
    if (!t) return;
    if (!rows.length) {
      t.innerHTML = `<tbody><tr><td colspan="${headers.length}" style="text-align:center;padding:24px;color:var(--ink-3);">${opts.empty || "No data available."}</td></tr></tbody>`;
      return;
    }
    const th = headers.map((h) => `<th class="${h.num ? "num" : ""}">${esc(h.label)}</th>`).join("");
    const tb = rows.map((r) => `<tr>${headers.map((h) => `<td class="${h.num ? "num" : ""}">${h.html ? h.html(r) : esc(h.get ? h.get(r) : r[h.key])}</td>`).join("")}</tr>`).join("");
    t.innerHTML = `<thead><tr>${th}</tr></thead><tbody>${tb}</tbody>`;
  }

  function getBrands() {
    return state.brand === "all" ? Object.keys(state.data.brands_metadata) : [state.brand];
  }

  // ======================================================== 1. OVERVIEW
  function renderOverview() {
    const brands = getBrands();
    const isAct = state.time === "currently_active";
    $("#spend-hint").textContent = isAct ? "Monthly Run-Rate (EUR)" : "Trailing 12-Month Total (EUR)";

    // KPIs
    let totSpend = 0, totAds = 0, totKeywords = 0, avgHeat = 0;
    const allSpend = state.data.media_spend;
    const activeAds = state.data.meta_ads.raw_active;
    const searches = state.data.search_footprint.raw;
    const deals = state.data.affiliates.raw;

    brands.forEach((b) => {
      totSpend += allSpend[b][state.time].total_estimated_spend_eur;
      totAds += activeAds.filter((a) => a.brand === b).length;
      totKeywords += searches.filter((s) => s.brand === b).length;
      const bDeals = deals.filter((d) => d.brand === b);
      if (bDeals.length) avgHeat += bDeals.reduce((s, x) => s + x.temperature_deg, 0) / bDeals.length;
    });
    if (brands.length) avgHeat = Math.round(avgHeat / brands.length);

    $("#kpis").innerHTML = `
      <div class="kpi-card">
        <div class="brand-tag">Total Modeled Media Spend</div>
        <div class="big">${eur(totSpend)}</div>
        <div class="desc">${isAct ? "Monthly run-rate in Germany" : "Cumulative trailing 12 months"}</div>
      </div>
      <div class="kpi-card">
        <div class="brand-tag">Meta Ad Creatives</div>
        <div class="big">${num(totAds)} Active Flights</div>
        <div class="desc">Video, Reels &amp; Carousels live</div>
      </div>
      <div class="kpi-card">
        <div class="brand-tag">Search &amp; Shopping Footprint</div>
        <div class="big">${num(totKeywords)} Target Intercepts</div>
        <div class="desc">Paid SEM, PLA &amp; top organic SERPs</div>
      </div>
      <div class="kpi-card">
        <div class="brand-tag">Deal Community Engagement</div>
        <div class="big">${num(avgHeat)}° Heat</div>
        <div class="desc">Average MyDealz temperature</div>
      </div>
    `;

    // Chart 1: Spend bars
    const brandLabels = brands.map((b) => state.data.brands_metadata[b].name);
    chart("c-spend-bars", {
      type: "bar",
      data: {
        labels: brandLabels,
        datasets: [{
          label: "Estimated Spend (EUR)",
          data: brands.map((b) => allSpend[b][state.time].total_estimated_spend_eur),
          backgroundColor: brands.map((b) => brandCol(b)),
          borderRadius: 6,
        }],
      },
      options: {
        indexAxis: "y",
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (c) => {
                const b = brands[c.dataIndex];
                const d = allSpend[b][state.time];
                return [`Spend: ${eur(c.raw)}`, `Range: ${eur(d.spend_band_low_eur)} – ${eur(d.spend_band_high_eur)}`];
              },
            },
          },
        },
        scales: { x: { ticks: { callback: (v) => "€" + Number(v).toLocaleString() } } },
      },
    });

    // Chart 2: Channel mix
    const channels = ["Meta Ads", "Google Search & Shopping", "Retail Media (Amazon/MMS)", "Affiliate & Deal Payouts"];
    const channelCols = ["#8b5cf6", "#3b82f6", "#f59e0b", "#10b981"];
    chart("c-channel-mix", {
      type: "bar",
      data: {
        labels: brandLabels,
        datasets: channels.map((ch, i) => ({
          label: ch,
          data: brands.map((b) => allSpend[b][state.time].channel_breakdown_pct[ch] || 0),
          backgroundColor: channelCols[i],
          borderRadius: 2,
        })),
      },
      options: {
        scales: { x: { stacked: true }, y: { stacked: true, max: 100, ticks: { callback: (v) => v + "%" } } },
        plugins: { legend: { position: "bottom" }, tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${pct(c.raw)}` } } },
      },
    });

    // Chart 3: Seasonality curve
    const months = (allSpend.ninja.trailing_12m.monthly_trend || []).map((m) => m.month);
    chart("c-seasonality", {
      type: "line",
      data: {
        labels: months,
        datasets: brands.map((b) => ({
          label: state.data.brands_metadata[b].name,
          data: allSpend[b].trailing_12m.monthly_trend.map((m) => m.estimated_spend_eur),
          borderColor: brandCol(b),
          backgroundColor: alpha(brandCol(b), 0.1),
          tension: 0.3,
          borderWidth: 2.5,
          pointRadius: 3,
        })),
      },
      options: {
        plugins: {
          legend: { position: "bottom" },
          tooltip: {
            callbacks: {
              afterLabel: (c) => {
                const b = brands[c.datasetIndex];
                const item = allSpend[b].trailing_12m.monthly_trend[c.dataIndex];
                return `Focus: ${item.campaign_focus}`;
              },
            },
          },
        },
        scales: { y: { ticks: { callback: (v) => "€" + Number(v).toLocaleString() } } },
      },
    });
  }

  // ======================================================== 2. META AD LIBRARY
  function renderMeta() {
    const brands = getBrands();
    const isAct = state.time === "currently_active";
    const adsRaw = isAct ? state.data.meta_ads.raw_active : state.data.meta_ads.raw_12m;
    const filtered = adsRaw.filter((a) => brands.includes(a.brand));
    $("#ads-count-hint").textContent = `Showing ${filtered.length} creatives for ${brands.length === 1 ? state.data.brands_metadata[brands[0]].name : "selected brands"}`;

    // Format distribution chart
    const formats = ["video", "reel", "carousel", "static_image"];
    const formatLabels = ["Video", "Instagram Reel", "Carousel", "Static Image"];
    chart("c-meta-formats", {
      type: "bar",
      data: {
        labels: brands.map((b) => state.data.brands_metadata[b].name),
        datasets: formats.map((fmt, i) => ({
          label: formatLabels[i],
          data: brands.map((b) => filtered.filter((a) => a.brand === b && a.format === fmt).length),
          backgroundColor: ["#6366f1", "#a855f7", "#ec4899", "#94a3b8"][i],
          borderRadius: 3,
        })),
      },
      options: {
        scales: { x: { stacked: true }, y: { stacked: true, ticks: { precision: 0 } } },
        plugins: { legend: { position: "bottom" } },
      },
    });

    // Hook angles chart
    const hooks = ["space_saving", "dual_zone_sync", "energy_savings", "healthy_low_fat", "easy_cleaning", "recipe_ecosystem", "price_cut"];
    const hookLabels = ["Space-Saving", "Dual-Zone Sync", "Energy Savings", "Healthy / Low-Fat", "Easy Clean", "App & Recipes", "Price Promo"];
    chart("c-meta-hooks", {
      type: "bar",
      data: {
        labels: hookLabels,
        datasets: brands.map((b) => ({
          label: state.data.brands_metadata[b].name,
          data: hooks.map((h) => filtered.filter((a) => a.brand === b && a.hook_angle === h).length),
          backgroundColor: brandCol(b),
          borderRadius: 3,
        })),
      },
      options: {
        indexAxis: "y",
        plugins: { legend: { position: "bottom" } },
        scales: { x: { ticks: { precision: 0 } } },
      },
    });

    // Creative Cards Feed
    const cardsEl = $("#ad-cards");
    cardsEl.innerHTML = filtered.map((a) => `
      <div class="ad-card">
        <div>
          <div class="ad-header">
            <div>
              <span class="badge ${esc(a.status)}">${a.status === "active" ? "● Active Now" : "Historical Flight"}</span>
              <span class="badge ${esc(a.format)}">${esc(a.format.replace("_", " ").toUpperCase())}</span>
            </div>
            <strong style="color:${brandCol(a.brand)};font-size:12px;">${esc(state.data.brands_metadata[a.brand]?.name)}</strong>
          </div>
          <div class="ad-title">${esc(a.headline)}</div>
          <div class="ad-body">${esc(a.body_copy)}</div>
        </div>
        <div>
          <div style="font-size:11.5px;color:var(--ink-3);margin-bottom:6px;">
            Target: <strong>${esc(a.target_sku)}</strong> · Hook: <span class="badge">${esc(a.hook_angle.replace("_", " "))}</span>
          </div>
          <div class="ad-footer">
            <span>Flight: ${a.flight_days} days (${a.first_seen_date})</span>
            <a href="${esc(a.landing_page_url)}" target="_blank" rel="noopener">${esc(a.cta_text || "Link")} ↗</a>
          </div>
        </div>
      </div>
    `).join("");
  }

  // ======================================================== 3. GOOGLE SEARCH
  function renderSearch() {
    const brands = getBrands();
    const raw = state.data.search_footprint.raw.filter((s) => brands.includes(s.brand));

    // Search presence chart
    chart("c-search-presence", {
      type: "bar",
      data: {
        labels: brands.map((b) => state.data.brands_metadata[b].name),
        datasets: [
          { label: "Paid Search Ads", data: brands.map((b) => raw.filter((s) => s.brand === b && s.search_type === "paid_text_ad").length), backgroundColor: "#3b82f6", borderRadius: 3 },
          { label: "Google Shopping (PLA)", data: brands.map((b) => raw.filter((s) => s.brand === b && s.search_type === "google_shopping_pla").length), backgroundColor: "#f59e0b", borderRadius: 3 },
          { label: "Organic Top 3 SERP", data: brands.map((b) => raw.filter((s) => s.brand === b && s.search_type === "organic_serp" && s.rank <= 3).length), backgroundColor: "#10b981", borderRadius: 3 },
        ],
      },
      options: { plugins: { legend: { position: "bottom" } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
    });

    // Keyword table
    const kwRows = [];
    brands.forEach((b) => {
      const bInfo = state.data.brands_metadata[b];
      (bInfo.google_sem?.brand_terms || []).forEach((kw) => kwRows.push({ brand: bInfo.name, type: "Brand Term Defense", keyword: kw }));
      (bInfo.google_sem?.generic_intercepts || []).forEach((kw) => kwRows.push({ brand: bInfo.name, type: "Generic Category Intercept", keyword: kw }));
    });
    table("#t-search-keywords", [
      { label: "Brand", key: "brand" },
      { label: "Strategy Type", html: (r) => `<span class="badge">${esc(r.type)}</span>` },
      { label: "Target Search Keyword", html: (r) => `<code>${esc(r.keyword)}</code>` },
    ], kwRows);

    // Raw search table
    table("#t-search-raw", [
      { label: "Brand", html: (r) => `<strong style="color:${brandCol(r.brand)}">${esc(state.data.brands_metadata[r.brand]?.name)}</strong>` },
      { label: "Type", html: (r) => `<span class="badge ${esc(r.search_type)}">${esc(r.search_type.replace(/_/g, " "))}</span>` },
      { label: "Keyword", html: (r) => `<code>${esc(r.keyword)}</code>` },
      { label: "Rank", num: true, get: (r) => `#${r.rank}` },
      { label: "Ad Headline / SERP Title", html: (r) => `<a href="${esc(r.target_url)}" target="_blank" rel="noopener">${esc(r.title)}</a>` },
      { label: "Display URL", get: (r) => r.display_url },
      { label: "Price", num: true, html: (r) => r.price_shown ? eur(r.price_shown) : "–" },
    ], raw);
  }

  // ======================================================== 4. AFFILIATES
  function renderAffiliates() {
    const brands = getBrands();
    const raw = state.data.affiliates.raw.filter((d) => brands.includes(d.brand));

    // Temperature chart
    chart("c-deal-temp", {
      type: "bar",
      data: {
        labels: brands.map((b) => state.data.brands_metadata[b].name),
        datasets: [{
          label: "Avg Deal Temperature (° Heat)",
          data: brands.map((b) => {
            const bDeals = raw.filter((d) => d.brand === b);
            return bDeals.length ? Math.round(bDeals.reduce((s, x) => s + x.temperature_deg, 0) / bDeals.length) : 0;
          }),
          backgroundColor: brands.map((b) => brandCol(b)),
          borderRadius: 4,
        }],
      },
      options: { plugins: { legend: { display: false } }, scales: { y: { ticks: { callback: (v) => v + "°" } } } },
    });

    // Discounts chart
    chart("c-deal-discounts", {
      type: "bar",
      data: {
        labels: brands.map((b) => state.data.brands_metadata[b].name),
        datasets: [{
          label: "Avg Discount Depth (%)",
          data: brands.map((b) => {
            const bDeals = raw.filter((d) => d.brand === b);
            return bDeals.length ? Math.round(bDeals.reduce((s, x) => s + x.discount_pct, 0) / bDeals.length) : 0;
          }),
          backgroundColor: alpha("#ef4444", 0.75),
          borderRadius: 4,
        }],
      },
      options: { plugins: { legend: { display: false } }, scales: { y: { ticks: { callback: (v) => "-" + v + "%" } } } },
    });

    // Deals table
    table("#t-affiliates", [
      { label: "Brand", html: (r) => `<strong style="color:${brandCol(r.brand)}">${esc(state.data.brands_metadata[r.brand]?.name)}</strong>` },
      { label: "Deal Title", html: (r) => `<a href="${esc(r.deal_url)}" target="_blank" rel="noopener">${esc(r.title)}</a>` },
      { label: "Merchant", get: (r) => r.merchant },
      { label: "Price", num: true, get: (r) => eur(r.deal_price_eur) },
      { label: "Cut", num: true, html: (r) => `<span style="color:var(--good);font-weight:700;">-${pct(r.discount_pct)}</span>` },
      { label: "Heat", num: true, html: (r) => `<span class="heat-pill ${r.temperature_deg > 600 ? "heat-hot" : "heat-warm"}">${r.temperature_deg}°</span>` },
      { label: "Voucher", html: (r) => r.voucher_code ? `<code>${esc(r.voucher_code)}</code>` : "–" },
      { label: "Affiliate Network", html: (r) => `<span class="badge">${esc(r.affiliate_network)}</span>` },
      { label: "Creator / Collab", get: (r) => r.creator_collaborator || "Community" },
    ], raw);
  }

  // ======================================================== 5. PR & RETAIL
  function renderRetailPR() {
    const brands = getBrands();
    const prs = state.data.pr_coverage.raw.filter((r) => brands.includes(r.brand));
    const acts = state.data.retail_activations.raw.filter((a) => brands.includes(a.brand));

    // PR table
    table("#t-pr-releases", [
      { label: "Brand", html: (r) => `<strong style="color:${brandCol(r.brand)}">${esc(state.data.brands_metadata[r.brand]?.name)}</strong>` },
      { label: "Category", html: (r) => `<span class="badge ${esc(r.category)}">${esc(r.category.replace(/_/g, " ").toUpperCase())}</span>` },
      { label: "Headline & Release Summary", html: (r) => `<div><a href="${esc(r.url)}" target="_blank" rel="noopener"><strong>${esc(r.title)}</strong></a><div style="font-size:12px;color:var(--ink-2);margin-top:4px;">${esc(r.summary)}</div></div>` },
      { label: "Media Wire / Source", get: (r) => r.publisher_source },
      { label: "Date", get: (r) => r.date },
    ], prs);

    // Retail activations table
    table("#t-retail-activations", [
      { label: "Brand", html: (r) => `<strong style="color:${brandCol(r.brand)}">${esc(state.data.brands_metadata[r.brand]?.name)}</strong>` },
      { label: "E-Retailer", html: (r) => `<strong>${esc(r.retailer)}</strong>` },
      { label: "Format", html: (r) => `<span class="badge">${esc(r.activation_type.replace(/_/g, " "))}</span>` },
      { label: "Campaign / Store Feature", html: (r) => `<div><strong>${esc(r.title)}</strong><div style="font-size:12px;color:var(--ink-2);">${esc(r.details)}</div></div>` },
      { label: "Period", get: (r) => r.period },
    ], acts);
  }

  // ======================================================== 6. DOSSIER
  function renderDossier() {
    const md = $("#dossier-markdown");
    const brands = state.data.brands_metadata;
    const spend = state.data.media_spend;

    let html = `<h3>1. Executive Media Investment Benchmark (Germany)</h3>`;
    html += `<table><thead><tr><th>Brand</th><th>DACH Operating Entity</th><th>12-Month Est. Spend</th><th>Active Monthly Run-Rate</th><th>Lead Acquisition Motion</th></tr></thead><tbody>`;
    Object.keys(brands).forEach((b) => {
      const bInfo = brands[b];
      const s12 = spend[b].trailing_12m;
      const sAct = spend[b].currently_active;
      const lead = b === "ninja" ? "High-Velocity Meta Video + D2C Checkout" : b === "cosori" ? "Amazon Retail Media + App Ecosystem" : b === "philips" ? "Premium Stiftung Warentest TVC + MediaMarkt Co-Op" : "Grill USP + Otto/Kaufland Trade Activations";
      html += `<tr><td><strong style="color:${brandCol(b)}">${esc(bInfo.name)}</strong></td><td>${esc(bInfo.corporate_name)}</td><td><strong>${eur(s12.total_estimated_spend_eur)}</strong></td><td>${eur(sAct.total_estimated_spend_eur)}</td><td>${lead}</td></tr>`;
    });
    html += `</tbody></table>`;

    html += `<h3 style="margin-top:24px;">2. Channel Playbook Comparison</h3>`;
    html += `<ul>
      <li><strong>SharkNinja</strong>: Pure American DTC playbook adapted for DACH. Relentless creative testing on Meta (Vertical DoubleStack &amp; CRISPi), conquesting competitor search terms, and driving direct transactions via <code>ninjakitchen.de</code>.</li>
      <li><strong>Cosori (VeSync)</strong>: Digital-native e-commerce champion. Dominates Amazon Prime Day and organic TikTok/Instagram recipe communities. Moat is the VeSync smart kitchen app (over 500k German users).</li>
      <li><strong>Philips (Versuni)</strong>: Traditional Category Creator playing premium defense. Heavy reliance on <em>Stiftung Warentest</em> test awards and deep partnerships with MediaMarkt/Saturn Club programs.</li>
      <li><strong>Tefal (Groupe SEB)</strong>: Hybrid mass-market warrior. Strong POS presence in food retail (REWE loyalty stamp campaigns), differentiated by genuine die-cast grill plates (Easy Fry &amp; Grill).</li>
    </ul>`;

    md.innerHTML = html;
  }

  // ======================================================== ROUTING
  const RENDER = {
    overview: renderOverview,
    meta: renderMeta,
    search: renderSearch,
    affiliates: renderAffiliates,
    retail_pr: renderRetailPR,
    dossier: renderDossier,
  };

  function setTab(tab) {
    state.tab = tab;
    $$("#tabs button").forEach((b) => b.classList.toggle("active", b.dataset.tab === tab));
    $$("section[data-panel]").forEach((s) => (s.hidden = s.dataset.panel !== tab));
    RENDER[tab]();
  }

  function setBrand(b) {
    state.brand = b;
    $$("#brand-picker button").forEach((btn) => btn.classList.toggle("active", btn.dataset.b === b));
    RENDER[state.tab]();
  }

  function setTime(t) {
    state.time = t;
    $$("#time-picker button").forEach((btn) => btn.classList.toggle("active", btn.dataset.time === t));
    RENDER[state.tab]();
  }

  async function init() {
    try {
      const res = await fetch("data/radar.json", { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      state.data = await res.json();
    } catch (e) {
      $("#subtitle").textContent = "No data loaded. Run `brand-radar run` to execute scraper.";
      return;
    }

    $("#foot-meta").textContent = `Brand Radar · German Category Intelligence · Run ${new Date().toLocaleDateString("de-DE")}`;
    $$("#tabs button").forEach((b) => b.addEventListener("click", () => setTab(b.dataset.tab)));
    $$("#brand-picker button").forEach((b) => b.addEventListener("click", () => setBrand(b.dataset.b)));
    $$("#time-picker button").forEach((b) => b.addEventListener("click", () => setTime(b.dataset.time)));

    setTab("overview");
  }

  init();
})();
