/**
 * MockAd — Skyscraper (160×600)
 * Drop a <div class="mock-ad-skyscraper"></div> anywhere on the page,
 * then call MockAd.init(). The component fetches from your Flask endpoint
 * and renders a styled ad with a dismiss + "Why this ad?" label.
 *
 * Usage:
 *   <div class="mock-ad-skyscraper"></div>
 *   <script src="mock_ad.js"></script>
 *   <script>MockAd.init();</script>
 *
 * Config (optional, pass to MockAd.init):
 *   MockAd.init({ endpoint: "/api/ads/skyscraper", refreshMs: 0 });
 *   refreshMs: auto-refresh interval in ms (0 = no refresh)
 */

const MockAd = (() => {
  const DEFAULTS = {
    endpoint: "/api/ads/skyscraper",
    refreshMs: 0,
  };

  const CSS = `
    .mock-ad-skyscraper {
      width: 160px;
      height: 600px;
      position: relative;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      flex-shrink: 0;
    }
    .mad-shell {
      width: 160px;
      height: 600px;
      border-radius: 8px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: 0 4px 24px rgba(0,0,0,0.18);
    }
    .mad-label {
      position: absolute;
      top: 6px;
      left: 8px;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      opacity: 0.5;
      color: #fff;
      z-index: 2;
    }
    .mad-dismiss {
      position: absolute;
      top: 4px;
      right: 6px;
      background: rgba(255,255,255,0.15);
      border: none;
      color: #fff;
      font-size: 11px;
      line-height: 1;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 3;
      transition: background 0.2s;
    }
    .mad-dismiss:hover { background: rgba(255,255,255,0.3); }
    .mad-image {
      width: 160px;
      height: 200px;
      object-fit: cover;
      display: block;
      flex-shrink: 0;
    }
    .mad-body {
      flex: 1;
      padding: 14px 12px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .mad-advertiser {
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      opacity: 0.6;
      margin-bottom: 8px;
    }
    .mad-headline {
      font-size: 17px;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 10px;
    }
    .mad-copy {
      font-size: 11px;
      line-height: 1.55;
      opacity: 0.75;
      flex: 1;
    }
    .mad-cta {
      display: block;
      margin-top: 16px;
      padding: 9px 0;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-align: center;
      text-decoration: none;
      transition: opacity 0.2s, transform 0.15s;
      cursor: pointer;
    }
    .mad-cta:hover { opacity: 0.88; transform: translateY(-1px); }
    .mad-why {
      font-size: 9px;
      text-align: center;
      opacity: 0.35;
      margin-top: 8px;
      cursor: pointer;
      text-decoration: underline;
    }
    .mad-why:hover { opacity: 0.6; }
    .mad-loading {
      width: 160px;
      height: 600px;
      background: #1a1a1a;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #555;
      font-size: 11px;
    }
  `;

  function injectStyles() {
    if (document.getElementById("mock-ad-styles")) return;
    const style = document.createElement("style");
    style.id = "mock-ad-styles";
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  function renderAd(container, data) {
    const { ad, width, height } = data;
    container.innerHTML = `
      <div class="mad-shell" style="background:${ad.bg_color}; color:#fff;">
        <span class="mad-label">Ad</span>
        <button class="mad-dismiss" title="Close ad">✕</button>
        <img class="mad-image" src="${ad.image_url}" alt="${ad.advertiser}" loading="lazy" />
        <div class="mad-body">
          <div>
            <div class="mad-advertiser" style="color:${ad.accent_color}">${ad.advertiser}</div>
            <div class="mad-headline">${ad.headline}</div>
            <div class="mad-copy">${ad.body}</div>
          </div>
          <div>
            <a class="mad-cta" href="${ad.click_url}"
               style="background:${ad.accent_color}; color:${ad.bg_color}">
              ${ad.cta}
            </a>
            <div class="mad-why">Why this ad?</div>
          </div>
        </div>
      </div>
    `;

    // Dismiss
    container.querySelector(".mad-dismiss").addEventListener("click", () => {
      container.style.display = "none";
    });

    // "Why this ad?" — just a tooltip/alert for the mockup
    container.querySelector(".mad-why").addEventListener("click", () => {
      alert("This is a simulated ad shown to free-tier users.\n\nUpgrade to remove ads.");
    });
  }

  async function fetchAndRender(container, endpoint) {
    try {
      const res = await fetch(endpoint);
      if (!res.ok) throw new Error("Non-200 response");
      const data = await res.json();
      renderAd(container, data);
    } catch (err) {
      container.innerHTML = `<div class="mad-loading">Ad unavailable</div>`;
      console.warn("[MockAd] Failed to load ad:", err);
    }
  }

  function init(options = {}) {
    const config = { ...DEFAULTS, ...options };
    injectStyles();

    const containers = document.querySelectorAll(".mock-ad-skyscraper");
    containers.forEach((el) => {
      fetchAndRender(el, config.endpoint);
      if (config.refreshMs > 0) {
        setInterval(() => fetchAndRender(el, config.endpoint), config.refreshMs);
      }
    });
  }

  return { init };
})();
