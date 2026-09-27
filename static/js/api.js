/**
 * AdaptiveLearn AI - Frontend API Client
 * Wraps REST endpoints with error handling and JSON parsing.
 */

const API = {
  async get(url) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }));
        throw new Error(err.error || `HTTP error ${res.status}`);
      }
      return await res.json();
    } catch (e) {
      console.error(`API GET [${url}] Error:`, e);
      throw e;
    }
  },

  async post(url, data = {}) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }));
        throw new Error(err.error || `HTTP error ${res.status}`);
      }
      return await res.json();
    } catch (e) {
      console.error(`API POST [${url}] Error:`, e);
      throw e;
    }
  },

  // Auth & Session
  switchDemoUser: (target) => API.post("/api/auth/switch-demo", { target }),
  getCurrentUser: () => API.get("/api/auth/me"),
  logout: () => API.post("/api/auth/logout"),

  // Student & Adaptive Flow
  getDashboard: () => API.get("/api/student/dashboard"),
  getNextActivity: (courseId) => API.get(`/api/learning/next${courseId ? '?course_id=' + courseId : ''}`),
  getAdaptivePath: (courseId) => API.get(`/api/learning/path${courseId ? '?course_id=' + courseId : ''}`),
  getKnowledgeGraph: (courseId) => API.get(`/api/concepts/graph${courseId ? '?course_id=' + courseId : ''}`),
  getMasteryOverview: (courseId) => API.get(`/api/mastery${courseId ? '?course_id=' + courseId : ''}`),

  // Assessments
  getAssessment: (conceptId, retheme = true) => API.get(`/api/assessment?concept_id=${conceptId}&retheme=${retheme}`),
  submitAssessment: (conceptId, answers) => API.post("/api/assessment/submit", { concept_id: conceptId, answers }),

  // Missions
  getMissions: () => API.get("/api/missions"),
  getMission: (missionId) => API.get(`/api/missions/${missionId}`),
  attemptMissionStep: (missionId, stepNumber, value, timeTaken = 30) => 
    API.post(`/api/missions/${missionId}/attempt`, {
      step_number: stepNumber,
      submitted_value: value,
      time_spent_seconds: timeTaken
    }),

  // Videos & Short Feed
  getShortFeed: () => API.get("/api/short-feed"),
  getPlaylists: () => API.get("/api/youtube/playlists"),
  getCuratedVideos: () => API.get("/api/youtube/curated-videos"),
  getPlaylist: (id) => API.get(`/api/youtube/playlists/${id}`),
  getVideoAnalytics: () => API.get("/api/youtube/analytics"),
  recordVideoProgress: (videoId, seconds, isCompleted = false, replayCount = 0) =>
    API.post("/api/youtube/video/progress", {
      video_id: videoId,
      watched_seconds: seconds,
      is_completed: isCompleted,
      replay_count: replayCount
    }),

  // Career & Timetable
  getCareerPathways: () => API.get("/api/career/pathways"),
  getTimetable: () => API.get("/api/timetable"),
  generateTimetable: (hours) => API.post("/api/timetable/generate", { available_hours: hours }),

  // AI Assistant & Community
  sendChatMessage: (msg, conceptId) => API.post("/api/ai/chat", { message: msg, concept_id: conceptId }),
  translateText: (text, lang) => API.post("/api/ai/translate", { text, target_language: lang }),
  getCommunityPosts: (cid) => API.get(`/api/community${cid ? '?community_id=' + cid : ''}`),
  createCommunityPost: (data) => API.post("/api/community/posts", data),

  // Facilitator
  getFacilitatorStudents: () => API.get("/api/facilitator/students"),
  getInterventions: (status) => API.get(`/api/interventions${status ? '?status=' + status : ''}`),
  assignIntervention: (interventionId, actionType, details) => 
    API.post("/api/interventions/assign", { intervention_id: interventionId, action_type: actionType, details })
};

window.API = API;
