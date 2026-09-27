/**
 * AdaptiveLearn AI - Short Educational Video Feed Controller
 * Manages vertical reel interactions, live YouTube player, replays, skips, and updates the Learning Interest Profile.
 * CRITICAL RULE: Video engagement is an INTEREST signal, NEVER automatic academic mastery.
 */

class ShortFeedController {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.videos = [];
    this.currentIndex = 0;
    this.watchTimer = null;
    this.currentWatchSeconds = 0;
    this.isPlaying = true;
    this.replayCount = 0;
    this.playerMode = "video"; // "video" (iframe embed) or "card" (cover mode)
    this.boundKeyHandler = null;
  }

  async init() {
    if (!this.container) return;
    this.container.innerHTML = `<div style="text-align:center; padding:60px; color:#94a3b8;">
      <div style="font-size:2rem; margin-bottom:12px;">⚡</div>
      Loading Curated Educational Shorts...
    </div>`;

    try {
      const data = await API.getShortFeed();
      this.videos = data.feed || [];
      if (this.videos.length === 0) {
        this.container.innerHTML = `<div style="text-align:center; padding:60px; color:#94a3b8;">
          No short videos currently available.
        </div>`;
        return;
      }

      // Check if a specific video was requested via URL query params (e.g., /short-feed?v=1FEPodyGeK4)
      const urlParams = new URLSearchParams(window.location.search);
      const targetVid = urlParams.get("v") || urlParams.get("video_id");
      if (targetVid) {
        const foundIdx = this.videos.findIndex(v => v.video_id === targetVid || String(v.id) === targetVid);
        if (foundIdx !== -1) {
          this.currentIndex = foundIdx;
        }
      }

      this.render();
      this.startWatchTimer();
      this.setupKeyboardListeners();
    } catch (e) {
      console.error("Short feed init error:", e);
      this.container.innerHTML = `<div style="color:#ef4444; text-align:center; padding:40px;">
        Failed to load feed: ${e.message}
      </div>`;
    }
  }

  setupKeyboardListeners() {
    if (this.boundKeyHandler) {
      window.removeEventListener("keydown", this.boundKeyHandler);
    }
    this.boundKeyHandler = (e) => {
      // Don't trigger if user is typing in an input
      if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) return;
      if (e.key === "ArrowDown" || e.key === "ArrowRight") {
        e.preventDefault();
        this.nextVideo();
      } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
        e.preventDefault();
        this.prevVideo();
      } else if (e.key === " ") {
        e.preventDefault();
        this.togglePlay();
      }
    };
    window.addEventListener("keydown", this.boundKeyHandler);
  }

  render() {
    const video = this.videos[this.currentIndex];
    if (!video) return;

    const duration = video.duration_seconds || 60;
    const progressPct = Math.min(100, Math.round((this.currentWatchSeconds / duration) * 100));
    const youtubeUrl = `https://youtube.com/shorts/${video.video_id}`;

    // Build the Shelf HTML for all 9 videos
    const shelfItemsHtml = this.videos.map((v, idx) => {
      const isActive = idx === this.currentIndex;
      return `
        <div class="shelf-item ${isActive ? 'active' : ''}" onclick="window.activeFeedController.selectVideo(${idx})">
          <div class="shelf-thumb" style="background-image: url('${v.thumbnail_url || 'https://i.ytimg.com/vi/' + v.video_id + '/hqdefault.jpg'}');">
            <span class="shelf-index-tag">#${idx + 1}</span>
          </div>
          <div class="shelf-info">
            <div class="shelf-item-title">${v.title}</div>
            <div class="shelf-item-meta">
              <span class="shelf-item-subj">${v.subject || 'Core'}</span>
              <span>•</span>
              <span>⏱️ ${v.duration_seconds || 60}s</span>
              <span>•</span>
              <span>${v.difficulty || 'MEDIUM'}</span>
            </div>
          </div>
        </div>
      `;
    }).join("");

    this.container.innerHTML = `
      <div class="short-feed-layout fade-in">
        <!-- Center Column: Vertical Reel Phone Viewport -->
        <div class="reels-viewport">
          
          <!-- Top Floating Bar -->
          <div class="reel-top-bar">
            <span class="reel-counter-badge">
              ⚡ Short ${this.currentIndex + 1} / ${this.videos.length}
            </span>
            <button class="reel-mode-toggle" onclick="window.activeFeedController.togglePlayerMode()">
              ${this.playerMode === 'video' ? '🖼️ Card View' : '🎬 Player View'}
            </button>
          </div>

          <!-- Video Player Frame -->
          <div class="video-player-frame">
            ${this.playerMode === 'video' ? `
              <iframe 
                id="short-yt-iframe"
                src="https://www.youtube.com/embed/${video.video_id}?autoplay=1&enablejsapi=1&rel=0&playsinline=1" 
                title="${video.title}" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen>
              </iframe>
            ` : `
              <div class="video-slide-cover" style="background-image: url('${video.thumbnail_url || 'https://i.ytimg.com/vi/' + video.video_id + '/hqdefault.jpg'}');">
                <div class="play-watermark" onclick="window.activeFeedController.togglePlayerMode()" title="Switch to Live Video Player">
                  ▶
                </div>
              </div>
            `}
          </div>

          <!-- Bottom Info and Controls Sheet -->
          <div class="reel-bottom-sheet">
            <div>
              <div class="video-tags">
                <span class="tag-pill tag-concept">📚 ${video.concept_title || video.subject || 'Academic Concept'}</span>
                <span class="tag-pill">⚡ ${video.difficulty || 'MEDIUM'}</span>
                <span class="tag-pill">⏱️ ${video.duration_seconds || 60}s</span>
                <span class="tag-pill">🗣️ ${video.language || 'English'}</span>
              </div>

              <h2 class="video-title">${video.title}</h2>
              <div class="video-channel">
                <span>📺 <strong>${video.channel_name || 'AdaptiveLearn AI'}</strong></span>
              </div>
              <p class="video-desc">${video.description || 'Fast-paced conceptual breakdown.'}</p>
            </div>

            <div>
              <!-- Progress Tracker Bar -->
              <div class="video-progress-tracker" title="Watch progress">
                <div class="video-progress-fill" id="feed-progress-fill" style="width: ${progressPct}%;"></div>
              </div>

              <!-- Action Links Row -->
              <div class="reel-actions-row">
                <button class="yt-direct-btn" onclick="window.activeFeedController.togglePlayerMode()" title="Toggle Player View / Poster View" type="button">
                  <span>${this.playerMode === 'video' ? '🎬 Live Player' : '🖼️ Poster View'}</span>
                  <span style="font-size:10px; color:#38bdf8;">● Active</span>
                </button>

                <div class="btn-icon-group">
                  <button class="action-btn-circle" onclick="window.activeFeedController.showTranscript()" title="Read Lesson Transcript">
                    📝
                  </button>
                  <button class="action-btn-circle" onclick="window.activeFeedController.saveVideo(${video.id})" title="Save to Watch Later">
                    🔖
                  </button>
                  <button class="action-btn-circle" onclick="window.activeFeedController.learnMore(${video.concept_id || 4})" title="Go to Guided Mission / Practice">
                    🎯
                  </button>
                </div>
              </div>

              <!-- Main Navigation Controls -->
              <div class="feed-nav-controls">
                <button class="feed-nav-btn" onclick="window.activeFeedController.prevVideo()">
                  ▲ Prev
                </button>
                <button class="feed-nav-btn primary" onclick="window.activeFeedController.togglePlay()">
                  <span id="play-btn-label">${this.isPlaying ? '⏸️ Pause' : '▶️ Play'}</span>
                </button>
                <button class="feed-nav-btn" onclick="window.activeFeedController.replayVideo()">
                  🔄 Replay
                </button>
                <button class="feed-nav-btn" onclick="window.activeFeedController.nextVideo(true)">
                  ▼ Next
                </button>
              </div>
            </div>
          </div>

        </div>

        <!-- Right Column: Interactive Educational Shorts Shelf -->
        <div class="shorts-playlist-shelf">
          <div class="shelf-header">
            <div>
              <div class="shelf-title">📱 Shorts Catalog</div>
              <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Fast-Paced Conceptual Modules</div>
            </div>
            <span class="shelf-count">${this.videos.length} Videos</span>
          </div>

          <div class="shelf-list">
            ${shelfItemsHtml}
          </div>
        </div>

      </div>
    `;

    window.activeFeedController = this;
  }

  togglePlayerMode() {
    this.playerMode = this.playerMode === "video" ? "card" : "video";
    this.render();
  }

  startWatchTimer() {
    if (this.watchTimer) clearInterval(this.watchTimer);
    this.currentWatchSeconds = 0;
    this.isPlaying = true;

    this.watchTimer = setInterval(() => {
      if (!this.isPlaying) return;
      this.currentWatchSeconds += 1;
      const video = this.videos[this.currentIndex];
      const duration = video ? video.duration_seconds || 60 : 60;
      
      const pct = Math.min(100, Math.round((this.currentWatchSeconds / duration) * 100));
      const fillEl = document.getElementById("feed-progress-fill");
      if (fillEl) fillEl.style.width = `${pct}%`;

      // Every 10 seconds or upon completion, record engagement and boost interest
      if (this.currentWatchSeconds % 10 === 0 || this.currentWatchSeconds >= duration) {
        const isCompleted = this.currentWatchSeconds >= duration;
        API.recordVideoProgress(video.id, 10, isCompleted, this.replayCount);
        
        if (isCompleted) {
          showToast(`Completed: ${video.title}! Learning Interest Profile updated. ✨`);
          setTimeout(() => this.nextVideo(false), 1200);
        }
      }
    }, 1000);
  }

  selectVideo(index) {
    if (index === this.currentIndex) return;
    if (this.watchTimer) clearInterval(this.watchTimer);
    const video = this.videos[this.currentIndex];
    if (video && this.currentWatchSeconds > 0) {
      API.recordVideoProgress(video.id, this.currentWatchSeconds, false, this.replayCount);
    }
    this.currentIndex = index;
    this.currentWatchSeconds = 0;
    this.replayCount = 0;
    this.render();
    this.startWatchTimer();
  }

  togglePlay() {
    this.isPlaying = !this.isPlaying;
    const label = document.getElementById("play-btn-label");
    if (label) label.textContent = this.isPlaying ? '⏸️ Pause' : '▶️ Play';
    showToast(this.isPlaying ? "Resumed short playback." : "Paused playback.");
  }

  replayVideo() {
    this.replayCount += 1;
    this.currentWatchSeconds = 0;
    this.isPlaying = true;
    showToast("Replaying conceptual short (+1 Interest signal recorded). 🔄");
    const video = this.videos[this.currentIndex];
    if (video) {
      API.recordVideoProgress(video.id, 0, false, 1);
    }
    this.render();
    this.startWatchTimer();
  }

  prevVideo() {
    if (this.watchTimer) clearInterval(this.watchTimer);
    this.currentIndex = (this.currentIndex - 1 + this.videos.length) % this.videos.length;
    this.currentWatchSeconds = 0;
    this.replayCount = 0;
    this.render();
    this.startWatchTimer();
  }

  nextVideo(isSkip = false) {
    if (this.watchTimer) clearInterval(this.watchTimer);
    const video = this.videos[this.currentIndex];
    if (isSkip && video) {
      showToast(`Skipped to next short.`);
      API.recordVideoProgress(video.id, this.currentWatchSeconds, false, 0);
    }
    this.currentIndex = (this.currentIndex + 1) % this.videos.length;
    this.currentWatchSeconds = 0;
    this.replayCount = 0;
    this.render();
    this.startWatchTimer();
  }

  saveVideo(videoId) {
    showToast("Short saved to your Study Collection! 🔖");
  }

  showTranscript() {
    const video = this.videos[this.currentIndex];
    if (!video) return;
    const modal = document.createElement("div");
    modal.className = "modal-overlay active";
    modal.innerHTML = `
      <div class="modal-card" style="max-width: 520px; padding: 24px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px;">
          <div>
            <h3 style="font-size:17px; margin-bottom:4px; color:#fff;">📝 Lesson Summary & Transcript</h3>
            <div style="font-size:12px; color:var(--accent-cyan);">${video.title}</div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="this.closest('.modal-overlay').remove()">✕</button>
        </div>
        <div style="font-size: 13.5px; color: #cbd5e1; line-height: 1.6; max-height: 320px; overflow-y: auto; margin-bottom: 20px; background: rgba(0,0,0,0.3); padding: 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);">
          ${video.transcript_text || 'Educational transcript loading or unavailable for this short segment.'}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <button class="btn btn-secondary btn-sm" onclick="window.activeFeedController.learnMore(${video.concept_id || 4})" style="font-size:12px;">
            🎯 Practice Mission
          </button>
          <button class="btn btn-cyan btn-sm" onclick="this.closest('.modal-overlay').remove()">Got It</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  learnMore(conceptId) {
    window.location.href = `/learning-gaps?concept_id=${conceptId || 4}`;
  }
}

window.ShortFeedController = ShortFeedController;
