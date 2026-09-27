"""
AdaptiveLearn AI - Machine Learning Feature Extraction
Extracts normalized behavioral, assessment, and engagement features for the ML Learning State Decision Tree.
"""

def extract_features(student_stats):
    """
    Transforms raw student records into an 8-dimensional feature vector:
    1. assessment_score (0 - 100)
    2. practice_score (0 - 100)
    3. attempts_count (integer >= 1)
    4. failed_attempts (integer >= 0)
    5. previous_mastery (0 - 100)
    6. performance_trend (-1 = declining, 0 = stable, 1 = improving)
    7. video_engagement_ratio (0.0 - 1.0+)
    8. time_between_attempts_hours (float >= 0.0)
    """
    assessment_score = float(student_stats.get("assessment_score", 50.0) or 50.0)
    practice_score = float(student_stats.get("practice_score", 50.0) or 50.0)
    attempts_count = int(student_stats.get("attempts_count", 1) or 1)
    failed_attempts = int(student_stats.get("failed_attempts", 0) or 0)
    previous_mastery = float(student_stats.get("previous_mastery", 50.0) or 50.0)
    
    # Calculate performance trend if not explicitly provided
    trend_val = student_stats.get("performance_trend")
    if trend_val is None:
        delta = assessment_score - previous_mastery
        if delta > 3.0:
            performance_trend = 1.0  # Improving
        elif delta < -3.0:
            performance_trend = -1.0 # Declining
        else:
            performance_trend = 0.0  # Stable
    else:
        performance_trend = float(trend_val)
        
    video_engagement_ratio = float(student_stats.get("video_engagement_ratio", 0.5) or 0.5)
    time_between_attempts_hours = float(student_stats.get("time_between_attempts_hours", 24.0) or 24.0)

    return [
        assessment_score,
        practice_score,
        attempts_count,
        failed_attempts,
        previous_mastery,
        performance_trend,
        video_engagement_ratio,
        time_between_attempts_hours
    ]
