"""
AdaptiveLearn AI - Verification & Test Suite
Validates all endpoints, two-student demo scenario, adaptive engine, missions, ML model, and UI views.
"""

import sys
from app import app
from database.db import db

def run_tests():
    print("=" * 70)
    print("AdaptiveLearn AI - Automated System Verification Suite")
    print("=" * 70)

    client = app.test_client()

    failures = 0
    passed = 0

    def assert_true(cond, name, details=""):
        nonlocal failures, passed
        if cond:
            print(f"  [PASS] {name}")
            passed += 1
        else:
            print(f"  [FAIL] {name} - {details}")
            failures += 1

    # 1. Test HTML Page Routes
    print("\n--- 1. Testing Core Frontend Views ---")
    routes_to_test = [
        "/",
        "/login",
        "/register",
        "/onboarding",
        "/dashboard",
        "/learning",
        "/assessment",
        "/short-feed",
        "/missions",
        "/missions/1",
        "/knowledge-graph",
        "/learning-gaps",
        "/videos",
        "/history",
        "/career",
        "/timetable",
        "/community",
        "/study-groups",
        "/projects",
        "/facilitator",
        "/chatbot",
        "/courses/1"
    ]

    for r in routes_to_test:
        resp = client.get(r)
        assert_true(resp.status_code == 200, f"GET {r} returns 200 OK", f"Status: {resp.status_code}")

    # 2. Test Two-Student Demo Logic
    print("\n--- 2. Verifying Two-Student Adaptive Demo Scenario ---")
    
    # Check Rahul (Student ID: 1, struggling)
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["student_id"] = 1
        sess["name"] = "Rahul Sharma"
        sess["role"] = "student"
    
    resp_rahul = client.get("/api/student/dashboard")
    assert_true(resp_rahul.status_code == 200, "Rahul Dashboard API returns 200")
    data_rahul = resp_rahul.get_json()
    rahul_ml = data_rahul.get("ml_state", {}).get("state")
    assert_true(rahul_ml == "NEEDS_SUPPORT", f"Rahul ML state is NEEDS_SUPPORT (Actual: {rahul_ml})")
    
    # Check Knowledge Graph for Rahul: Statistics < 70% and Probability LOCKED
    resp_kg_rahul = client.get("/api/concepts/graph?course_id=1")
    kg_rahul = resp_kg_rahul.get_json()
    stat_node_rahul = next((n for n in kg_rahul.get("nodes", []) if "STAT" in n.get("code", "")), None)
    prob_node_rahul = next((n for n in kg_rahul.get("nodes", []) if "PROB" in n.get("code", "")), None)
    
    assert_true(stat_node_rahul and stat_node_rahul.get("status") in ["STRUGGLING", "NEEDS_PRACTICE"], 
                f"Rahul Statistics status is STRUGGLING / NEEDS_PRACTICE (Score: {stat_node_rahul.get('mastery_score')}%)")
    assert_true(prob_node_rahul and prob_node_rahul.get("status") == "LOCKED", 
                "Rahul Probability concept is STRICTLY LOCKED")

    # Check Priya (Student ID: 2, mastering)
    with client.session_transaction() as sess:
        sess["user_id"] = 2
        sess["student_id"] = 2
        sess["name"] = "Priya Patel"
        sess["role"] = "student"

    resp_priya = client.get("/api/student/dashboard")
    assert_true(resp_priya.status_code == 200, "Priya Dashboard API returns 200")
    data_priya = resp_priya.get_json()
    priya_ml = data_priya.get("ml_state", {}).get("state")
    assert_true(priya_ml == "IMPROVING", f"Priya ML state is IMPROVING (Actual: {priya_ml})")

    resp_kg_priya = client.get("/api/concepts/graph?course_id=1")
    kg_priya = resp_kg_priya.get_json()
    stat_node_priya = next((n for n in kg_priya.get("nodes", []) if "STAT" in n.get("code", "")), None)
    prob_node_priya = next((n for n in kg_priya.get("nodes", []) if "PROB" in n.get("code", "")), None)
    
    assert_true(stat_node_priya and stat_node_priya.get("mastery_score", 0) >= 70, 
                f"Priya Statistics score >= 70% (Actual: {stat_node_priya.get('mastery_score')}%)")
    assert_true(prob_node_priya and prob_node_priya.get("status") != "LOCKED", 
                f"Priya Probability concept is UNLOCKED (Status: {prob_node_priya.get('status')})")

    # 3. Test Interactive Missions and Automatic Completion
    print("\n--- 3. Testing Interactive Learning Missions ---")
    resp_missions = client.get("/api/missions")
    assert_true(resp_missions.status_code == 200, "GET /api/missions returns 200")
    missions_data = resp_missions.get_json().get("missions", [])
    assert_true(len(missions_data) >= 4, f"Found at least 4 academic missions (Count: {len(missions_data)})")

    # Attempt incorrect value on Mission 1 Step 1
    resp_att_wrong = client.post("/api/missions/1/attempt", json={
        "step_number": 1,
        "submitted_value": "999",
        "time_spent_seconds": 15
    })
    att_wrong_data = resp_att_wrong.get_json()
    assert_true(not att_wrong_data.get("is_correct"), "Mission rejects incorrect parameter with pedagogical feedback")

    # Attempt correct value for step 1 (mean of 240, 260, 280 = 260)
    resp_att_correct = client.post("/api/missions/1/attempt", json={
        "step_number": 1,
        "submitted_value": "260",
        "time_spent_seconds": 25
    })
    att_correct_data = resp_att_correct.get_json()
    assert_true(att_correct_data.get("is_correct"), f"Mission accepts correct calculated parameter (Actual: {att_correct_data})")

    # 4. Test AI Contextual Re-Theming
    print("\n--- 4. Testing AI Contextual Re-Theming ---")
    original_q = {
        "question_text": "What is the median of the data set: 3, 7, 8, 12, 15?",
        "option_a": "7",
        "option_b": "8",
        "option_c": "9",
        "option_d": "12",
        "correct_answer": "8"
    }
    resp_retheme = client.post("/api/ai/retheme", json={
        "question": original_q,
        "interest_theme": "Space & Astronomy"
    })
    assert_true(resp_retheme.status_code == 200, "POST /api/ai/retheme returns 200")
    retheme_data = resp_retheme.get_json()
    rethemed_text = retheme_data.get("question_text", "")
    assert_true("probe" in rethemed_text.lower() or "telemetry" in rethemed_text.lower() or "space" in rethemed_text.lower(), 
                f"Question narrative re-themed to space context (Text: {rethemed_text})")
    assert_true(retheme_data.get("correct_answer") == "8", "Correct answer '8' strictly preserved")

    # 5. Test AI Tutor Chatbot Scaffolding
    print("\n--- 5. Testing Pedagogical AI Tutor Scaffolding ---")
    resp_chat = client.post("/api/ai/chat", json={
        "message": "Why can't I learn Probability?"
    })
    assert_true(resp_chat.status_code == 200, "POST /api/ai/chat returns 200")
    chat_data = resp_chat.get_json()
    assert_true("statistics" in chat_data.get("reply", "").lower() and "threshold" in chat_data.get("reply", "").lower(), 
                "Tutor explains Statistics prerequisite barrier without direct cheating")

    # 6. Test Facilitator Intervention Console
    print("\n--- 6. Testing Facilitator Interventions ---")
    resp_fac_students = client.get("/api/facilitator/students")
    assert_true(resp_fac_students.status_code == 200, "GET /api/facilitator/students returns 200")
    students_list = resp_fac_students.get_json().get("students", [])
    rahul_in_fac = next((s for s in students_list if "Rahul" in s["name"]), None)
    assert_true(rahul_in_fac and rahul_in_fac["ml_state"] == "NEEDS_SUPPORT", 
                "Facilitator console identifies Rahul as needing support")

    resp_interventions = client.get("/api/interventions")
    assert_true(resp_interventions.status_code == 200, "GET /api/interventions returns 200")
    interventions_list = resp_interventions.get_json().get("interventions", [])
    assert_true(len(interventions_list) > 0, f"Found active interventions needing teacher action ({len(interventions_list)})")

    # 7. Test Video Engagement Separation
    print("\n--- 7. Testing Video Engagement as Interest Signal Only ---")
    resp_video_prog = client.post("/api/youtube/video/complete", json={
        "video_id": 1,
        "watch_time_seconds": 360
    })
    assert_true(resp_video_prog.status_code == 200, "POST /api/youtube/video/complete returns 200")
    # Verify Rahul's Statistics mastery is NOT automatically 100% just from watching video
    stat_rec = db.get_one("SELECT mastery_score FROM student_mastery WHERE student_id = 1 AND concept_id = 4")
    assert_true(stat_rec["mastery_score"] < 70, 
                f"Video completion did NOT automatically grant academic mastery (Mastery: {stat_rec['mastery_score']}%)")

    print("\n" + "=" * 70)
    print(f"Summary: {passed} PASSED, {failures} FAILED")
    print("=" * 70)
    if failures == 0:
        print("🎉 ALL SYSTEMS FULLY OPERATIONAL AND VERIFIED FOR HACKATHON!")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(run_tests())
