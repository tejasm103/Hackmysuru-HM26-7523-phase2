/**
 * AdaptiveLearn AI - Global Application Logic
 * Manages active sessions, 1-click Demo Switcher, toast alerts, and navigation.
 */

document.addEventListener("DOMContentLoaded", () => {
  initDemoSwitcher();
  highlightActiveNav();
});

function initDemoSwitcher() {
  const switcher = document.getElementById("demo-user-switcher");
  if (!switcher) return;

  switcher.addEventListener("change", async (e) => {
    const target = e.target.value;
    try {
      showToast(`Switching active demo persona to ${target.toUpperCase()}...`);
      await API.switchDemoUser(target);
      showToast(`Active session switched to ${target.toUpperCase()}! Reloading view...`);
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } catch (err) {
      showToast("Error switching demo account: " + err.message, "error");
    }
  });
}

function highlightActiveNav() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav-item a");
  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href === currentPath || (currentPath !== "/" && href.length > 1 && currentPath.startsWith(href))) {
      link.closest(".nav-item").classList.add("active");
    }
  });
}

function showToast(message, type = "info") {
  let toastContainer = document.getElementById("toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.id = "toast-container";
    toastContainer.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement("div");
  const bg = type === "error" ? "rgba(239, 68, 68, 0.95)" : "rgba(18, 28, 59, 0.95)";
  const border = type === "error" ? "rgba(239, 68, 68, 0.5)" : "rgba(99, 102, 241, 0.5)";
  
  toast.style.cssText = `
    background: ${bg};
    border: 1px solid ${border};
    color: #fff;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
  `;
  toast.innerHTML = `<span>${type === 'error' ? '⚠️' : '✨'}</span> <span>${message}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

window.showToast = showToast;
