from database.db import db

print("Testing db methods:")
users = db.query("SELECT id, name, email, role FROM users")
print(f"Total Users: {len(users)}")
for u in users:
    print(" ", u)

courses = db.query("SELECT id, code, title FROM courses")
print(f"\nTotal Courses: {len(courses)}")
for c in courses:
    print(" ", c)

missions = db.query("SELECT id, code, title FROM learning_missions")
print(f"\nTotal Missions: {len(missions)}")
for m in missions:
    print(" ", m)

rahul_m = db.query("""
    SELECT c.title, sm.mastery_score, sm.status 
    FROM student_mastery sm 
    JOIN concepts c ON sm.concept_id = c.id 
    WHERE sm.student_id = 1
""")
print(f"\nRahul's Concepts (Student 1):")
for rm in rahul_m:
    print(" ", rm)

interventions = db.query("SELECT * FROM interventions")
print(f"\nActive Interventions: {len(interventions)}")
for iv in interventions:
    print(" ", iv['trigger_reason'], "->", iv['status'])
