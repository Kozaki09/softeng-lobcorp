document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================
  // 1. INITIALIZE ADS (If applicable)
  // ==========================================
  // This safely checks if the MockAd script was loaded by the HTML template
  if (typeof MockAd !== "undefined") {
    MockAd.init({ endpoint: "/api/ads/banner" });
    MockAd.init({ endpoint: "/api/ads/rectangle" });
  }

  // ==========================================
  // 2. DOM ELEMENTS
  // ==========================================
  const form            = document.getElementById("predictForm");
  const submitBtn       = document.getElementById("submitBtn");
  const modeSelect      = document.getElementById("form-type");
  const disclaimerModal = document.getElementById("disclaimerModal");
  const agreeBtn        = document.getElementById("agreeBtn");

  // ==========================================
  // 3. THE PREDICTION LOGIC
  // ==========================================
  async function runPrediction() {
    submitBtn.disabled = true;
    submitBtn.textContent = "Analyzing…";

    const formData = new FormData(form);
    formData.append("mode", modeSelect.value);

    try {
      const res  = await fetch("/predict", { method: "POST", body: formData, credentials: "same-origin" });
      const data = await res.json();

      document.getElementById("resultArea").style.display = "block";
      document.getElementById("errorMsg").style.display   = "none";

      if (!res.ok) {
        throw new Error(data.error || "Prediction failed.");
      }

      const pct      = Math.round(data.risk_probability * 100);
      const highRisk = data.prediction === 1;

      // Update Status Pill
      const pill = document.getElementById("statusPill");
      pill.textContent = highRisk ? "High Risk" : "Low Risk";
      pill.style.background = highRisk ? "rgba(192,57,43,0.15)" : "rgba(31,122,140,0.15)";
      pill.style.color      = highRisk ? "#c0392b" : "var(--accent-1)";

      // Update Summary Text
      document.getElementById("resultSummary").innerHTML = `
        <p style="font-size:1rem;font-weight:600;color:${highRisk ? "#c0392b" : "var(--accent-1)"};">
          ${highRisk ? "⚠️ Elevated risk of heart disease detected." : "✓ Low risk of heart disease detected."}
        </p>
        <p class="muted" style="font-size:0.85rem;margin-top:4px;">
          ${highRisk
            ? "Consider consulting a healthcare professional for further evaluation."
            : "Maintain a healthy lifestyle and schedule regular check-ups."}
        </p>`;

      // Update Risk Bar
      document.getElementById("riskPct").textContent  = pct + "%";
      document.getElementById("riskPct").style.color  = highRisk ? "#c0392b" : "var(--accent-1)";
      document.getElementById("riskFill").style.width = pct + "%";
      document.getElementById("riskFill").style.background = highRisk
        ? "linear-gradient(90deg,#e67e22,#c0392b)"
        : "linear-gradient(90deg,var(--accent-2),var(--accent-1))";

    } catch (err) {
      document.getElementById("resultArea").style.display = "block";
      document.getElementById("errorMsg").style.display   = "block";
      document.getElementById("errorMsg").textContent     = err.message;
      document.getElementById("statusPill").textContent   = "Error";
    } finally {
      submitBtn.disabled    = false;
      submitBtn.textContent = "Analyze Risk";
    }
  }

  // ==========================================
  // 4. FORM SUBMISSION INTERCEPT
  // ==========================================
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // Check if user already agreed before
    if (localStorage.getItem("disclaimerAccepted")) {
      runPrediction();
    } else {
      disclaimerModal.style.display = "flex"; 
    }
  });

  // ==========================================
  // 5. MODAL BUTTON LOGIC
  // ==========================================
  agreeBtn.addEventListener("click", () => {
    localStorage.setItem("disclaimerAccepted", "true");
    disclaimerModal.style.display = "none";
    runPrediction();
  });

});