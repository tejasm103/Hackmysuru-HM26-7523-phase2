/**
 * AdaptiveLearn AI - Analytics & Chart.js Visualizer
 * Renders multi-signal Interest Graph, Weekly Learning Activity, and Before-vs-After Mastery correlation.
 * Enforces Section 29 disclaimer.
 */

class AnalyticsVisualizer {
  static async renderDashboardCharts() {
    try {
      const data = await API.getVideoAnalytics();
      const interestRes = await API.getDashboard();
      const interestGraph = interestRes.interest_graph;

      // 1. Learning Interest Profile Chart (Radar or Bar)
      const interestCanvas = document.getElementById("interest-chart");
      if (interestCanvas && interestGraph && interestGraph.chart_data) {
        new Chart(interestCanvas, {
          type: "radar",
          data: {
            labels: interestGraph.chart_data.labels,
            datasets: [{
              label: "Affinity Score (%)",
              data: interestGraph.chart_data.scores,
              backgroundColor: "rgba(99, 102, 241, 0.25)",
              borderColor: "#6366f1",
              borderWidth: 2,
              pointBackgroundColor: "#06b6d4",
              pointBorderColor: "#fff",
              pointHoverRadius: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              r: {
                angleLines: { color: "rgba(255, 255, 255, 0.08)" },
                grid: { color: "rgba(255, 255, 255, 0.08)" },
                pointLabels: { color: "#94a3b8", font: { family: "'Outfit', sans-serif", size: 12, weight: "600" } },
                ticks: { display: false, min: 0, max: 100 }
              }
            },
            plugins: {
              legend: { display: false }
            }
          }
        });
      }

      // 2. Weekly Learning Time Chart
      const weeklyCanvas = document.getElementById("weekly-activity-chart");
      if (weeklyCanvas && data.weekly_activity) {
        new Chart(weeklyCanvas, {
          type: "bar",
          data: {
            labels: data.weekly_activity.labels,
            datasets: [
              {
                label: "Missions & Practice (min)",
                data: data.weekly_activity.mission_minutes,
                backgroundColor: "#10b981",
                borderRadius: 6
              },
              {
                label: "Video Engagement (min)",
                data: data.weekly_activity.video_minutes,
                backgroundColor: "#6366f1",
                borderRadius: 6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
              y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } }
            },
            plugins: {
              legend: { labels: { color: "#cbd5e1", font: { family: "'Plus Jakarta Sans', sans-serif" } } }
            }
          }
        });
      }

      // 3. Before vs After Mastery Correlation Chart
      const masteryCanvas = document.getElementById("mastery-comparison-chart");
      if (masteryCanvas && data.mastery_comparison) {
        new Chart(masteryCanvas, {
          type: "line",
          data: {
            labels: data.mastery_comparison.labels,
            datasets: [
              {
                label: "Initial Diagnostic Score (%)",
                data: data.mastery_comparison.before_activity,
                borderColor: "#64748b",
                backgroundColor: "transparent",
                borderDash: [5, 5],
                pointRadius: 4,
                pointBackgroundColor: "#94a3b8"
              },
              {
                label: "Mastery After Missions & Practice (%)",
                data: data.mastery_comparison.after_activity,
                borderColor: "#10b981",
                backgroundColor: "rgba(16, 185, 129, 0.12)",
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointBackgroundColor: "#10b981"
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
              y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" }, min: 0, max: 100 }
            },
            plugins: {
              legend: { labels: { color: "#cbd5e1" } }
            }
          }
        });
      }

    } catch (err) {
      console.error("Failed to render analytics charts:", err);
    }
  }
}

window.AnalyticsVisualizer = AnalyticsVisualizer;
