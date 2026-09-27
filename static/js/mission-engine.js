/**
 * AdaptiveLearn AI - Interactive Learning Mission Engine
 * Powers the "Learn By Doing" simulations (Space Station, Sustainable Ecosystem, Robot Repair, Spacecraft Landing).
 * Enforces Automatic Completion: System validates each step and automatically completes the mission.
 */

class MissionEngine {
  constructor(missionId, containerId) {
    this.missionId = missionId;
    this.container = document.getElementById(containerId);
    this.currentStepNumber = 1;
    this.missionData = null;
    this.startTime = Date.now();
  }

  async init() {
    if (!this.container) return;
    this.container.innerHTML = `<div style="text-align:center; padding:40px;">Initializing Mission Simulation...</div>`;
    try {
      this.missionData = await API.getMission(this.missionId);
      this.currentStepNumber = this.missionData.active_attempt ? this.missionData.active_attempt.current_step : 1;
      this.render();
    } catch (e) {
      this.container.innerHTML = `<div style="color:#ef4444; padding:20px;">Failed to initialize mission: ${e.message}</div>`;
    }
  }

  render() {
    const { mission, steps, active_attempt } = this.missionData;
    const isCompleted = active_attempt ? Boolean(active_attempt.is_completed) : false;

    let html = `
      <div class="mission-workspace">
        <!-- Left: Briefing & Step Cards -->
        <div class="mission-briefing">
          <div class="mission-theme-tag">🚀 Theme: ${mission.theme} • Academic Simulation</div>
          <h1 style="font-size: 28px; margin-bottom: 12px;">${mission.title}</h1>
          <p style="color: #cbd5e1; font-size: 15px; margin-bottom: 24px; line-height: 1.6;">
            ${mission.scenario_description}
          </p>

          <h3 style="font-size: 18px; margin-bottom: 16px;">Mission Execution Steps</h3>
          <div id="steps-list">
    `;

    steps.forEach(step => {
      const isPast = step.step_number < this.currentStepNumber || isCompleted;
      const isCurrent = step.step_number === this.currentStepNumber && !isCompleted;
      const cardClass = isPast ? "completed" : (isCurrent ? "active" : "");

      html += `
        <div class="step-card ${cardClass}" id="step-card-${step.step_number}">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div class="step-number-badge">${isPast ? '✓' : step.step_number}</div>
              <h4 style="font-size: 15px;">Task ${step.step_number} (${step.action_type.toUpperCase()})</h4>
            </div>
            ${isPast ? '<span class="badge badge-mastered">Verified</span>' : (isCurrent ? '<span class="badge badge-learning">In Progress</span>' : '<span class="badge badge-locked">Pending</span>')}
          </div>
          <p style="font-size: 14px; color: #e2e8f0; margin-bottom: 12px;">${step.instruction}</p>
          
          ${isCurrent ? `
            <div class="sim-input-group">
              <input type="text" id="sim-input-val" class="sim-input" placeholder="Enter calculated value or parameter..." />
              <button class="btn btn-cyan" onclick="window.activeMissionEngine.submitStep(${step.step_number})">Execute Action</button>
            </div>
            <div id="step-hint-${step.step_number}" class="hint-box">
              <strong>💡 Pedagogical Hint:</strong> <span id="hint-text-${step.step_number}"></span>
              <div id="prereq-text-${step.step_number}" style="margin-top:6px; font-size:12px; color:#93c5fd;"></div>
            </div>
          ` : ''}
        </div>
      `;
    });

    html += `
          </div>
        </div>

        <!-- Right: Real-Time Telemetry & Gauges Simulator -->
        <div class="mission-simulator">
          <div class="simulator-header">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight:700;">Operational Telemetry</div>
              <div style="font-size: 16px; font-weight:800; color:#38bdf8;">SIMULATOR ONLINE</div>
            </div>
            <span class="badge ${isCompleted ? 'badge-mastered' : 'badge-learning'}">
              ${isCompleted ? 'STATUS: NOMINAL / COMPLETED' : 'STATUS: CALIBRATING'}
            </span>
          </div>

          <div class="sim-screen" id="sim-screen">
            <div>
              <div class="telemetry-row">
                <span>SIMULATION TARGET:</span>
                <span class="telemetry-val">${mission.code}</span>
              </div>
              <div class="telemetry-row">
                <span>SYSTEM EQUILIBRIUM:</span>
                <span class="telemetry-val" id="telemetry-equilibrium">${isCompleted ? '100% STABLE' : 'CALIBRATING'}</span>
              </div>
              <div class="telemetry-row">
                <span>CURRENT STEP:</span>
                <span class="telemetry-val" id="telemetry-step">${this.currentStepNumber} of ${steps.length}</span>
              </div>
              <div class="telemetry-row">
                <span>ERRORS LOGGED:</span>
                <span class="telemetry-val" id="telemetry-errors" style="color:${active_attempt && active_attempt.mistakes_count > 0 ? '#ef4444' : '#4ade80'};">
                  ${active_attempt ? active_attempt.mistakes_count : 0}
                </span>
              </div>
            </div>
            <div style="font-size: 11px; color:#64748b; font-family: monospace;">
              [SYSTEM] Telemetry link synchronized. Enforcing continuous input verification.
            </div>
          </div>

          <div style="margin-top:20px;">
            <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
              <span>Mission Progress</span>
              <span id="mission-progress-label">${Math.round((Math.min(this.currentStepNumber - 1, steps.length) / steps.length) * 100)}%</span>
            </div>
            <div class="progress-bar-container">
              <div class="progress-bar-fill fill-emerald" id="mission-progress-bar"
                   style="width: ${Math.round((Math.min(this.currentStepNumber - 1, steps.length) / steps.length) * 100)}%;"></div>
            </div>
          </div>

          ${isCompleted ? `
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px; margin-top: 20px; text-align: center;">
              <h4 style="color: #34d399; margin-bottom: 6px;">🎉 Mission Completed!</h4>
              <p style="font-size: 13px; color: #cbd5e1;">All operational parameters verified. Concept mastery updated in database.</p>
              <a href="/learning-gaps" class="btn btn-emerald btn-sm" style="margin-top: 12px;">View Updated Knowledge Graph</a>
            </div>
          ` : ''}
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    window.activeMissionEngine = this;
  }

  async submitStep(stepNumber) {
    const inputEl = document.getElementById("sim-input-val");
    if (!inputEl) return;
    const value = inputEl.value.trim();
    if (!value) {
      showToast("Please enter a calculated parameter value.", "error");
      return;
    }

    const elapsed = Math.round((Date.now() - this.startTime) / 1000);
    this.startTime = Date.now();

    try {
      showToast("Verifying operational parameter with engine...");
      const result = await API.attemptMissionStep(this.missionId, stepNumber, value, elapsed);

      if (result.is_correct) {
        if (result.is_completed) {
          // AUTOMATIC COMPLETION
          showToast(result.message, "info");
          this.missionData.active_attempt = { is_completed: 1, mistakes_count: result.mistakes_count || 0 };
          this.currentStepNumber = this.missionData.steps.length + 1;
          this.render();
          this.showCelebrationModal(result);
        } else {
          showToast(result.message);
          this.currentStepNumber = result.next_step;
          this.render();
        }
      } else {
        // INCORRECT
        showToast(result.message, "error");
        const hintBox = document.getElementById(`step-hint-${stepNumber}`);
        const hintText = document.getElementById(`hint-text-${stepNumber}`);
        const prereqText = document.getElementById(`prereq-text-${stepNumber}`);
        
        if (hintBox) {
          hintText.textContent = result.hint || "Review your formula and check operations.";
          if (result.prerequisite_ref) {
            prereqText.textContent = `Prerequisite Concept Ref: ${result.prerequisite_ref}`;
          }
          hintBox.classList.add("show");
        }
        
        // Update error counter in telemetry
        const errEl = document.getElementById("telemetry-errors");
        if (errEl) {
          errEl.textContent = result.mistakes_count;
          errEl.style.color = "#ef4444";
        }
      }
    } catch (err) {
      showToast("Verification failed: " + err.message, "error");
    }
  }

  showCelebrationModal(result) {
    const modal = document.createElement("div");
    modal.className = "modal-overlay active";
    
    let unlockedHtml = "";
    if (result.unlocked_concepts && result.unlocked_concepts.length > 0) {
      unlockedHtml = `
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid var(--border-glow); border-radius: 12px; padding: 14px; margin-top: 16px;">
          <h5 style="color: #c7d2fe; margin-bottom: 6px;">🔓 New Concepts Unlocked!</h5>
          <ul style="list-style: none; font-size: 13px; color: #fff;">
            ${result.unlocked_concepts.map(c => `<li>✨ <strong>${c.code}</strong>: ${c.title}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    modal.innerHTML = `
      <div class="modal-card" style="text-align: center;">
        <div style="font-size: 48px; margin-bottom: 12px;">🏆</div>
        <h2 style="font-size: 26px; margin-bottom: 8px;">Mission Successfully Completed!</h2>
        <p style="color: #cbd5e1; font-size: 15px; margin-bottom: 20px;">
          All mathematical & operational parameters successfully balanced.
        </p>

        <div style="display:flex; justify-content:center; gap:24px; margin-bottom: 20px;">
          <div class="stat-pill">
            <span class="label">Demonstrated Score</span>
            <span class="value" style="color:#10b981;">${result.demonstrated_score}%</span>
          </div>
          <div class="stat-pill">
            <span class="label">XP Earned</span>
            <span class="value" style="color:#38bdf8;">+${result.xp_awarded} XP</span>
          </div>
        </div>

        ${unlockedHtml}

        <div style="display:flex; gap:12px; justify-content:center; margin-top: 24px;">
          <a href="/learning-gaps" class="btn btn-primary">View Knowledge Graph</a>
          <a href="/missions" class="btn btn-secondary">Next Mission</a>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.remove();
    });
  }
}

window.MissionEngine = MissionEngine;
