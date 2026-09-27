"""
AdaptiveLearn AI - Knowledge Graph Engine
Models concept prerequisites as a Directed Acyclic Graph (DAG) and computes visual node statuses:
- GREEN (MASTERED >= 70%)
- BLUE (LEARNING - active focus)
- YELLOW (NEEDS_PRACTICE 40-69%)
- RED (STRUGGLING < 40%)
- LOCK (LOCKED - unmet prerequisite < 70%)
"""

from database.db import db

DEFAULT_THRESHOLD = 70.0

class KnowledgeGraphEngine:
    def get_course_graph(self, course_id, student_id=None):
        """
        Retrieves all concepts for a course, their prerequisite dependencies, 
        and computes each node's status for the student.
        """
        # Fetch all concepts in sequence order
        concepts = db.query("""
            SELECT id, code, title, sequence_order, description, difficulty_level, category
            FROM concepts
            WHERE course_id = %s
            ORDER BY sequence_order ASC
        """, (course_id,))
        
        # Fetch prerequisites for all concepts in this course
        prereqs = db.query("""
            SELECT cp.concept_id, cp.prerequisite_id, cp.min_mastery_required,
                   c.title as prereq_title, c.code as prereq_code
            FROM concept_prerequisites cp
            JOIN concepts c ON cp.prerequisite_id = c.id
            JOIN concepts cur ON cp.concept_id = cur.id
            WHERE cur.course_id = %s
        """, (course_id,))
        
        prereq_map = {}
        for p in prereqs:
            cid = p["concept_id"]
            if cid not in prereq_map:
                prereq_map[cid] = []
            prereq_map[cid].append(p)
            
        # Fetch student mastery if student_id is provided
        mastery_map = {}
        if student_id:
            mastery_records = db.query("""
                SELECT concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score
                FROM student_mastery
                WHERE student_id = %s
            """, (student_id,))
            for m in mastery_records:
                mastery_map[m["concept_id"]] = m

        nodes = []
        edges = []
        
        # Build edges
        for p in prereqs:
            edges.append({
                "from": p["prerequisite_id"],
                "to": p["concept_id"],
                "min_mastery": float(p["min_mastery_required"])
            })

        # Evaluate each concept node
        for c in concepts:
            cid = c["id"]
            m_rec = mastery_map.get(cid)
            mastery_score = float(m_rec["mastery_score"]) if m_rec else 0.0
            attempts = int(m_rec["attempts_count"]) if m_rec else 0
            failed = int(m_rec["failed_attempts"]) if m_rec else 0
            
            # Check prerequisites satisfaction
            concept_prereqs = prereq_map.get(cid, [])
            all_prereqs_satisfied = True
            unmet_prereqs = []
            
            for p in concept_prereqs:
                pid = p["prerequisite_id"]
                p_mastery = float(mastery_map.get(pid, {}).get("mastery_score", 0.0))
                req_score = float(p["min_mastery_required"])
                if p_mastery < req_score:
                    all_prereqs_satisfied = False
                    unmet_prereqs.append({
                        "id": pid,
                        "title": p["prereq_title"],
                        "code": p["prereq_code"],
                        "current_mastery": p_mastery,
                        "required_mastery": req_score
                    })
            
            # Determine visual status: GREEN, BLUE, YELLOW, RED, LOCK
            rec_status = m_rec.get("status") if m_rec else None

            if not all_prereqs_satisfied:
                status = "LOCKED"
                color = "#64748b" # Slate gray / lock
                status_label = "Locked"
            elif rec_status == "STRUGGLING" or (failed >= 2 and mastery_score < DEFAULT_THRESHOLD):
                status = "STRUGGLING"
                color = "#ef4444" # Red
                status_label = "Struggling"
            elif mastery_score >= 80.0 or (mastery_score >= DEFAULT_THRESHOLD and rec_status == "MASTERED"):
                status = "MASTERED"
                color = "#10b981" # Green
                status_label = "Mastered"
            elif mastery_score >= DEFAULT_THRESHOLD:
                status = "LEARNING"
                color = "#3b82f6" # Blue
                status_label = "In Progress"
            elif mastery_score >= 40.0:
                status = "NEEDS_PRACTICE"
                color = "#f59e0b" # Yellow / Amber
                status_label = "Needs Practice"
            elif attempts > 0 or failed > 0:
                status = "STRUGGLING"
                color = "#ef4444" # Red
                status_label = "Struggling"
            else:
                status = "LEARNING"
                color = "#3b82f6" # Blue
                status_label = "Learning"
                
            nodes.append({
                "id": cid,
                "code": c["code"],
                "title": c["title"],
                "sequence_order": c["sequence_order"],
                "description": c["description"],
                "difficulty": c["difficulty_level"],
                "category": c["category"],
                "mastery_score": mastery_score,
                "status": status,
                "status_label": status_label,
                "color": color,
                "attempts": attempts,
                "failed_attempts": failed,
                "is_locked": not all_prereqs_satisfied,
                "unmet_prereqs": unmet_prereqs
            })

        return {
            "course_id": course_id,
            "nodes": nodes,
            "edges": edges,
            "default_mastery_threshold": DEFAULT_THRESHOLD
        }

knowledge_graph_engine = KnowledgeGraphEngine()
