-- =======================================================
-- AdaptiveLearn AI - Complete Relational Seed Data
-- Evaluator Ready: Full Demo Profiles (Rahul, Priya, Arjun, Ananya, Kiran)
-- =======================================================

USE adaptivelearn_db;

-- 1. Seed Schools
INSERT INTO schools (id, name, code, city, state) VALUES
(1, 'Karnataka State Model High School', 'KSMHS-01', 'Bengaluru', 'Karnataka'),
(2, 'Government Polytechnic Institute', 'GPI-02', 'Mysuru', 'Karnataka'),
(3, 'National Science & Tech College', 'NSTC-03', 'Mangaluru', 'Karnataka');

-- 2. Seed Users
INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'Rahul Sharma', 'rahul@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'student'),
(2, 'Priya Patel', 'priya@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'student'),
(3, 'Arjun Rao', 'arjun@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'student'),
(4, 'Ananya Iyer', 'ananya@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'student'),
(5, 'Kiran Kumar', 'kiran@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'student'),
(6, 'Dr. Vikram Sharma', 'facilitator@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'facilitator'),
(7, 'Admin Lead', 'admin@adaptivelearn.ai', 'pbkdf2:sha256:600000$adaptive$8cb2237d3079b33a5cfef3b4009a6ee012f275e7a91ad34b07f8c14e1c4295e8', 'admin');

-- 3. Seed Facilitators
INSERT INTO facilitators (id, user_id, school_id, department, designation) VALUES
(1, 6, 1, 'STEM & Academic Intervention', 'Lead Academic Mentor & Facilitator');

-- 4. Seed Students
INSERT INTO students (id, user_id, school_id, study_level, grade, stream, preferred_language, learning_streak, learning_goal, career_goal) VALUES
(1, 1, 1, 'Grade 10', '10th', 'Science & Mathematics', 'English', 4, 'Overcome Statistics Gaps & Unlock Probability', 'Aerospace Engineering & Space Tech'),
(2, 2, 1, 'Grade 10', '10th', 'Science & Mathematics', 'English', 12, 'Excel in Advanced Mathematics & Olympiad Problems', 'Data Science & Applied Mathematics'),
(3, 3, 2, 'Diploma', '2nd Year', 'Computer Science', 'Kannada', 7, 'Build Full-Stack and Embedded Systems Projects', 'Robotics Software Engineer'),
(4, 4, 3, 'PUC', '1st PUC', 'Science (PCMB)', 'English', 15, 'Master Classical Mechanics and Astrophysics', 'Astrophysics & Space Research'),
(5, 5, 1, 'Professional Course', 'Final Year', 'Programming', 'English', 1, 'Complete Diagnostic Assessment & Upskill in AI', 'Machine Learning Engineer');

-- 5. Seed Courses
INSERT INTO courses (id, code, title, subject, level, stream, description, icon, color) VALUES
(1, 'MATH-10', 'Grade 10 Mathematics: Foundations to Advanced', 'Mathematics', 'Grade 10', 'Science & Mathematics', 'Comprehensive core syllabus spanning Algebra, Linear Equations, Functions, Statistics, and Probability with interactive missions.', 'calculator', '#6366f1'),
(2, 'SCI-10', 'Grade 10 Science: Biological & Ecological Systems', 'Science', 'Grade 10', 'Science', 'Cell biology, genetics, ecosystem dynamics, and sustainable resource management.', 'leaf', '#10b981'),
(3, 'CS-DIP', 'Diploma Computer Science: Algorithms & Robotics Logic', 'Computer Science', 'Diploma', 'Computer Science', 'Practical algorithm thinking, sensor control loops, and embedded logic programming.', 'cpu', '#06b6d4'),
(4, 'PHY-PUC', 'PUC Physics: Mechanics & Spacecraft Dynamics', 'Physics', 'PUC', 'Science', 'Vectors, Newton laws, kinetic energy, gravitational trajectories, and landing dynamics.', 'rocket', '#f59e0b');

-- 6. Seed Enrollments
INSERT INTO enrollments (student_id, course_id, status) VALUES
(1, 1, 'active'),
(2, 1, 'active'),
(3, 3, 'active'),
(4, 4, 'active'),
(5, 3, 'active');

-- 7. Seed Interests Catalog
INSERT INTO interests (id, name, category, icon) VALUES
(1, 'Space & Astronomy', 'STEM', 'rocket'),
(2, 'Robotics & Automation', 'Engineering', 'cpu'),
(3, 'Ecology & Environment', 'Natural Science', 'globe'),
(4, 'AI & Machine Learning', 'Computer Science', 'brain'),
(5, 'Gaming & Simulation', 'Creative Tech', 'gamepad'),
(6, 'Healthcare & Biology', 'Life Sciences', 'heart-pulse');

-- 8. Seed Student Interests (Initial profiles)
INSERT INTO student_interests (student_id, interest_id, affinity_score, source) VALUES
(1, 1, 88.00, 'onboarding'),
(1, 2, 74.00, 'video_engagement'),
(1, 3, 42.00, 'onboarding'),
(2, 4, 91.00, 'onboarding'),
(2, 1, 80.00, 'video_engagement'),
(3, 2, 94.00, 'onboarding'),
(3, 4, 78.00, 'onboarding'),
(4, 1, 95.00, 'onboarding'),
(4, 3, 65.00, 'onboarding');

-- 9. Seed Concepts for MATH-10
INSERT INTO concepts (id, course_id, code, title, sequence_order, description, difficulty_level, category) VALUES
(1, 1, 'ALG-01', 'Algebraic Expressions & Polynomials', 1, 'Fundamental algebraic manipulations, polynomial operations, and factoring.', 'EASY', 'Algebra'),
(2, 1, 'LIN-02', 'Linear Equations & Systems', 2, 'Solving pairs of linear equations, graphical representation, and substitution.', 'MEDIUM', 'Algebra'),
(3, 1, 'FUNC-03', 'Functions & Coordinate Relations', 3, 'Domain, range, function mapping, and quadratic curve characteristics.', 'MEDIUM', 'Analysis'),
(4, 1, 'STAT-04', 'Statistics: Mean, Variance & Distributions', 4, 'Measures of central tendency, grouped frequency distributions, and variance.', 'MEDIUM', 'Statistics'),
(5, 1, 'PROB-05', 'Probability: Classical, Conditional & Independent Events', 5, 'Sample spaces, compound event rules, Bayes intuition, and predictive likelihood.', 'HARD', 'Probability'),
(6, 1, 'ADV-06', 'Advanced Mathematical Modeling & Optimization', 6, 'Applying linear systems and stochastic models to real-world engineering simulations.', 'HARD', 'Applied Math');

-- Concepts for SCI-10
INSERT INTO concepts (id, course_id, code, title, sequence_order, description, difficulty_level, category) VALUES
(7, 2, 'CELL-01', 'Cell Structure & Energy Metabolism', 1, 'Organelles, cellular respiration, and ATP synthesis in living organisms.', 'EASY', 'Biology'),
(8, 2, 'GEN-02', 'Genetics, DNA & Mendelian Inheritance', 2, 'Chromosomes, alleles, punnett squares, and hereditary trait transmission.', 'MEDIUM', 'Genetics'),
(9, 2, 'ECO-03', 'Ecosystem Dynamics & Energy Flow', 3, 'Trophic cascades, nitrogen and carbon cycles, biomass pyramids, and ecological balance.', 'HARD', 'Ecology');

-- Concepts for CS-DIP
INSERT INTO concepts (id, course_id, code, title, sequence_order, description, difficulty_level, category) VALUES
(10, 3, 'PY-01', 'Python Variables, Types & Logic Flow', 1, 'Data types, conditional statements, and boolean operations.', 'EASY', 'Programming'),
(11, 3, 'CTRL-02', 'Control Loops & Algorithmic State', 2, 'For/while iterations, loop invariants, and algorithmic termination.', 'MEDIUM', 'Algorithms'),
(12, 3, 'ROB-03', 'Sensor Feedback & Closed-Loop Control', 3, 'PID concepts, sensor polling thresholds, and motor actuator logic.', 'HARD', 'Robotics');

-- Concepts for PHY-PUC
INSERT INTO concepts (id, course_id, code, title, sequence_order, description, difficulty_level, category) VALUES
(13, 4, 'KIN-01', 'Kinematics: Velocity, Acceleration & Time', 1, 'Equations of motion in 1D and 2D projectile paths.', 'EASY', 'Mechanics'),
(14, 4, 'NEWT-02', 'Newtonian Dynamics & Thrust Forces', 2, 'Newton second and third laws, momentum conservation, rocket equation fundamentals.', 'MEDIUM', 'Dynamics'),
(15, 4, 'LND-03', 'Spacecraft Trajectory & Soft Landing', 3, 'Calculating retrograde burn force, gravity deceleration, and touchdown timing.', 'HARD', 'Astrodynamics');

-- 10. Seed Concept Prerequisites
INSERT INTO concept_prerequisites (concept_id, prerequisite_id, min_mastery_required) VALUES
(2, 1, 70.00),
(3, 2, 70.00),
(4, 3, 60.00),
(5, 4, 70.00),
(6, 5, 70.00),
(8, 7, 70.00),
(9, 8, 70.00),
(11, 10, 70.00),
(12, 11, 70.00),
(14, 13, 70.00),
(15, 14, 70.00);

-- 11. Seed Student Mastery
-- RAHUL (Stats 43% STRUGGLING, Probability LOCKED)
INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score) VALUES
(1, 1, 86.00, 'MASTERED', 4, 0, 88.00),
(1, 2, 78.00, 'MASTERED', 5, 1, 76.00),
(1, 3, 61.00, 'NEEDS_PRACTICE', 6, 1, 62.00),
(1, 4, 43.00, 'STRUGGLING', 7, 3, 42.00),
(1, 5, 0.00, 'LOCKED', 0, 0, NULL),
(1, 6, 0.00, 'LOCKED', 0, 0, NULL);

-- PRIYA (Stats 82%, Functions 84%, Probability 76% UNLOCKED)
INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score) VALUES
(2, 1, 95.00, 'MASTERED', 3, 0, 96.00),
(2, 2, 92.00, 'MASTERED', 4, 0, 94.00),
(2, 3, 84.00, 'MASTERED', 4, 0, 85.00),
(2, 4, 82.00, 'MASTERED', 4, 0, 83.00),
(2, 5, 76.00, 'LEARNING', 3, 0, 78.00),
(2, 6, 0.00, 'LOCKED', 0, 0, NULL);

-- ARJUN
INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score) VALUES
(3, 10, 85.00, 'MASTERED', 4, 0, 86.00),
(3, 11, 68.00, 'NEEDS_PRACTICE', 5, 1, 66.00),
(3, 12, 45.00, 'LOCKED', 0, 0, NULL);

-- ANANYA
INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score) VALUES
(4, 13, 94.00, 'MASTERED', 3, 0, 95.00),
(4, 14, 88.00, 'MASTERED', 4, 0, 89.00),
(4, 15, 78.00, 'LEARNING', 3, 0, 77.00);

-- KIRAN
INSERT INTO student_mastery (student_id, concept_id, mastery_score, status, attempts_count, failed_attempts, last_assessment_score) VALUES
(5, 10, 0.00, 'LEARNING', 0, 0, NULL);

-- 12. Seed ML Predictions
INSERT INTO ml_predictions (student_id, concept_id, predicted_state, confidence_score, feature_snapshot) VALUES
(1, 4, 'NEEDS_SUPPORT', 0.92, '{"assessment_score": 42.0, "practice_score": 44.0, "attempts": 7, "failed_attempts": 3, "trend": -1, "video_engagement_seconds": 320}'),
(2, 5, 'IMPROVING', 0.89, '{"assessment_score": 78.0, "practice_score": 82.0, "attempts": 3, "failed_attempts": 0, "trend": 1, "video_engagement_seconds": 780}'),
(3, 11, 'STABLE', 0.78, '{"assessment_score": 66.0, "practice_score": 70.0, "attempts": 5, "failed_attempts": 1, "trend": 0, "video_engagement_seconds": 450}'),
(4, 15, 'IMPROVING', 0.94, '{"assessment_score": 77.0, "practice_score": 80.0, "attempts": 3, "failed_attempts": 0, "trend": 1, "video_engagement_seconds": 920}');

-- 13. Seed Interventions
INSERT INTO interventions (id, student_id, concept_id, trigger_reason, evidence_data, recommendation, status) VALUES
(1, 1, 4, 'Repeated struggle: Assessment score 42%, 3 failed attempts, declining trend', 
 '{"assessment": 42.0, "failed_attempts": 3, "functions_prereq_mastery": 61.0, "trend": "Declining", "common_error": "Confusing sample variance denominator (n-1) with population (n)"}',
 '1. Review Functions prerequisite (FUNC-03)\n2. Assign beginner Statistics video walkthrough\n3. Assign guided step-by-step Learning Mission\n4. Reassess after guided practice', 
 'open');

-- 14. Seed YouTube Playlists
INSERT INTO youtube_playlists (id, playlist_id, title, description, channel_name, thumbnail_url, course_id, is_user_provided) VALUES
(1, 'PLDxx7_Hz1sj8', 'Biology, Science & Career Guidance Explorations', 'User-provided educational playlist exploring biological sciences, ecosystem dynamics, and career guidance pathways.', 'Educational Pathways India', 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=600&q=80', 2, 1),
(2, 'PL_MATH_STAT', 'Grade 10 Statistics & Probability Mastery', 'High-impact breakdown of mean, variance, sample spaces, and compound probability.', 'Math Academy', 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=600&q=80', 1, 0),
(3, 'PL_ROBOTICS_CS', 'Autonomous Robotics & Sensor Logic', 'Learn closed-loop PID control, sensor polling, and embedded robotics logic in Python.', 'Robotics Lab', 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=600&q=80', 3, 0),
(4, 'PL_SPACE_PHYSICS', 'Astrophysics & Rocket Trajectory Dynamics', 'Newtonian mechanics applied to spacecraft orbital maneuvers and soft-landing burns.', 'Space Science Initiative', 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80', 4, 0),
(5, 'PL_CAREER_STREAMS', 'Secondary & Higher Secondary Career Stream Guidance', 'Curated educational guidance for Grade 10 and PUC students on stream selection (Commerce, Science, Arts), college courses, and career exploration.', 'Educational Pathways India', 'https://i.ytimg.com/vi/ueEOngDY268/hqdefault.jpg', 1, 1);

-- Seed YouTube Videos
INSERT INTO youtube_videos (id, video_id, title, description, channel_name, duration_seconds, thumbnail_url, subject, concept_id, language, difficulty, is_short_form, transcript_text) VALUES
(1, 'B57XEiiWxgY', 'Mathematics Deep Dive: Statistics & Foundations', 'Comprehensive session walking through foundational algebraic representations and statistical derivations.', 'EdTech Math Live', 600, 'https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=600&q=80', 'Mathematics', 4, 'English', 'MEDIUM', 0, 'Welcome students. Today we analyze measures of dispersion, mean deviations, and how sample variance allows us to quantify variability across datasets.'),
(2, 'O9SnhD-IpiA', '2nd PUC Maths: Matrices & Determinants PYQs', 'Important Previous Year Questions (PYQs) and core problem-solving techniques for 2nd PUC Mathematics: Matrices & Determinants.', 'College Dost Kannada', 60, 'https://i.ytimg.com/vi/O9SnhD-IpiA/hqdefault.jpg', 'Mathematics', 2, 'Kannada / English', 'MEDIUM', 1, 'Welcome PUC students. Let us solve high-frequency previous year questions on Matrices and Determinants for board and entrance exams.'),
(3, 'NlxtwjdPC78', 'Speed Math Challenge: Equation Logic', 'Rapid conceptual arithmetic and equation puzzle. Test your algebraic intuition before time runs out!', 'maths slover', 45, 'https://i.ytimg.com/vi/NlxtwjdPC78/hqdefault.jpg', 'Mathematics', 1, 'English', 'EASY', 1, 'Can you solve this algebraic challenge before time runs out? Break down the operations systematically to find the unknown value.'),
(4, 'DBQjYWs-46U', 'Pattern Logic & Mathematical Reasoning', 'Visual pattern deduction and fast numerical reasoning puzzle to train algorithmic and mathematical problem solving.', 'maths slover', 45, 'https://i.ytimg.com/vi/DBQjYWs-46U/hqdefault.jpg', 'Mathematics', 1, 'English', 'EASY', 1, 'Spot the pattern! Deduce the governing rule connecting the inputs to determine the final target number.'),
(5, '1FEPodyGeK4', 'Calculus Foundations: The Rate of Change', 'Visual introduction to calculus, understanding infinitesimal slopes, tangent derivatives, and real-time physical velocity.', 'Brain Station', 60, 'https://i.ytimg.com/vi/1FEPodyGeK4/hqdefault.jpg', 'Mathematics', 3, 'English', 'MEDIUM', 1, 'Calculus is the language of continuous change. Derivatives calculate instantaneous speed by taking the limit of average delta y over delta x as delta x approaches zero.'),
(6, '5E54PyNViZA', 'Understanding Calculus in One Minute', 'Intuitive 60-second explanation of why derivatives and integrals are inverse operations that describe change and accumulation.', 'JOCALUME', 60, 'https://i.ytimg.com/vi/5E54PyNViZA/hqdefault.jpg', 'Mathematics', 3, 'English', 'MEDIUM', 1, 'In one minute: differential calculus measures instantaneous rates of change, while integral calculus sums infinitely many tiny slices to find total area and accumulated quantities.'),
(7, 'gr57GG6Sb3Y', 'What is Commerce ? | Why to choose Commerce as stream ? | what to expect in Commerce ?', 'Essential orientation for Grade 10 & PUC students on selecting Commerce as an academic stream, covering career scope, core subjects, and expectations.', 'The Commerce Company', 480, 'https://i.ytimg.com/vi/gr57GG6Sb3Y/hqdefault.jpg', 'Commerce & Career Pathways', 9, 'English', 'EASY', 0, 'Welcome students. Today we discuss why to choose Commerce as a stream after 10th standard, core subjects like Accountancy, Business Studies, Economics, and future career opportunities in finance, analytics, and entrepreneurship.'),
(8, 'ueEOngDY268', 'Every 10th Standard Student Must Know This | Which Stream/Career To Choose In College', 'In-depth guide for 10th standard students on choosing between Science, Commerce, and Arts streams, understanding aptitude, and college pathways.', 'BeerBiceps', 720, 'https://i.ytimg.com/vi/ueEOngDY268/hqdefault.jpg', 'Career Guidance & Stream Selection', 9, 'English', 'EASY', 0, 'Deciding what stream to choose after 10th standard is a crucial milestone. Let us break down how your genuine interests, cognitive strengths, and long-term aspirations align with Science, Commerce, and Arts.'),
(9, '-_uMdKIgdHQ', 'Best Courses After 12th for Arts | High Salary Courses | Best Career Options', 'Detailed analysis of top degree courses, career paths, competitive examinations, and high-growth opportunities for students completing 12th / PUC.', 'Prabhat Exam', 600, 'https://i.ytimg.com/vi/-_uMdKIgdHQ/hqdefault.jpg', 'Higher Secondary & Career Pathways', 9, 'Hindi', 'EASY', 0, 'In this session, we analyze the top high-paying courses and career options available after completing 12th Arts, including Civil Services preparation, Law, Mass Communication, Designing, and Management.'),
(10, 'SNUKPzkiyHo', 'Mathematical Rigor: The Formal Proof That 1 + 1 = 2', 'Exploring Peano axioms and set theory: why formal mathematical proof requires rigorous foundations starting from the successor function.', 'Math Matrix', 55, 'https://i.ytimg.com/vi/SNUKPzkiyHo/hqdefault.jpg', 'Mathematics', 1, 'English', 'HARD', 1, 'Using Peano axioms, 1 is defined as S(0) and 2 is defined as S(1) = S(S(0)). By inductive addition definition, 1 + 1 equals S(1 + 0) = S(1) = 2. Rigorous proofs form the bedrock of mathematics.'),
(11, 'EHTpivfCkIU', 'Artificial Intelligence for Absolute Beginners', 'What is AI? Clear, foundational overview of machine learning, training data, and how intelligent models make decisions.', 'deepin explaining', 60, 'https://i.ytimg.com/vi/EHTpivfCkIU/hqdefault.jpg', 'Computer Science', 10, 'English', 'EASY', 1, 'Artificial intelligence allows computer algorithms to recognize patterns in data and make predictions without being explicitly programmed for every single edge case.'),
(12, 'RUxfxmV1_pI', '5 AI Technologies Transforming Industry & Daily Life', 'Breakdown of 5 revolutionary AI applications: computer vision, automated robotics, natural language processing, generative media, and autonomous vehicles.', 'AMERICA WORLDWIDE07', 60, 'https://i.ytimg.com/vi/RUxfxmV1_pI/hqdefault.jpg', 'Computer Science', 12, 'English', 'MEDIUM', 1, 'Here are 5 transformative AI technologies shaping modern engineering: advanced computer vision, sensor-guided autonomous robots, deep generative models, automated medical diagnosis, and edge compute controllers.'),
(13, 'SMC2lylFXeQ', 'What is AI? Neural Networks & Symbolic Logic Explained', 'Concise pedagogical animation explaining how artificial neural networks learn weights and biases to simulate cognitive reasoning.', 'The Educated Owl', 60, 'https://i.ytimg.com/vi/SMC2lylFXeQ/hqdefault.jpg', 'Computer Science', 12, 'English', 'EASY', 1, 'What really is Artificial Intelligence? From rule-based systems to multi-layer neural networks, AI takes input vectors, calculates weighted activations, and outputs classified probabilities.');

-- Map Playlist to Videos
INSERT INTO playlist_videos (playlist_id, video_id, sequence_order) VALUES
(2, 1, 1),
(2, 2, 2),
(2, 3, 3),
(2, 10, 4),
(1, 4, 1),
(3, 5, 1),
(3, 11, 2),
(3, 12, 3),
(3, 13, 4),
(4, 6, 1),
(5, 7, 1),
(5, 8, 2),
(5, 9, 3);
(5, 7, 1),
(5, 8, 2),
(5, 9, 3);

-- Map Playlist to Concepts
INSERT INTO playlist_concepts (playlist_id, concept_id, relevance_score) VALUES
(2, 4, 95.00),
(2, 5, 88.00),
(1, 9, 92.00),
(3, 12, 90.00),
(4, 15, 96.00),
(5, 9, 95.00);

-- 15. Seed Learning Missions
INSERT INTO learning_missions (id, concept_id, code, title, scenario_description, difficulty, theme, required_steps_count, xp_reward) VALUES
(1, 4, 'MISSION-STAT-SPACE', 'Save the Space Station: Orbital Resource Equilibrium', 
 'The orbital space station habitat modules are reporting irregular oxygen and power consumption. You must apply statistical distribution analysis and variance thresholds to restore equilibrium to the environmental life support system.', 
 'MEDIUM', 'Space', 3, 150),
(2, 9, 'MISSION-ECO-BALANCE', 'Build a Sustainable Ecosystem: Biosphere Delta', 
 'Manage a self-contained ecological dome. Balance primary producer biomass against consumer trophic levels to prevent oxygen depletion and trophic collapse.', 
 'MEDIUM', 'Ecology', 3, 150),
(3, 12, 'MISSION-ROBOT-REPAIR', 'Repair the Warehouse Robot: Closed-Loop Guidance', 
 'Warehouse delivery unit Bot-42 is oscillating erraticly between obstacles. Calculate error correction parameters and set sensor filtering bounds to guide it through the charging bay.', 
 'MEDIUM', 'Robotics', 3, 150),
(4, 15, 'MISSION-SPACE-LANDING', 'Land the Spacecraft: Mars Descent Maneuver', 
 'Descent capsule Odysseus is falling through the Martian atmosphere. Use F=ma and velocity-distance calculations to calculate retrograde thruster impulse time and achieve touchdown below 2 m/s.', 
 'HARD', 'Space', 3, 200);

-- 16. Seed Mission Steps
INSERT INTO mission_steps (id, mission_id, step_number, instruction, hint, prerequisite_ref, action_type, expected_value, tolerance) VALUES
(1, 1, 1, 'Calculate the daily mean oxygen consumption across modules Alpha, Beta, and Gamma with recorded values: 240L, 260L, and 280L.', 
 'Add the three values (240 + 260 + 280) and divide by the number of modules (3).', 'Algebraic Expressions (ALG-01)', 'calculate', '260', 0.50),
(2, 1, 2, 'Configure the life support buffer variance threshold. Given deviation from mean is 20L, compute the standard variance square (20^2).', 
 'Square the deviation: 20 * 20.', 'Linear Equations (LIN-02)', 'configure', '400', 1.00),
(3, 1, 3, 'Divert emergency auxiliary power: If Alpha requires 15kW and Beta requires 25kW, calculate total reserve percentage needed from a 100kW capacitor.', 
 'Sum of power needed divided by 100 times 100.', 'Functions & Relations (FUNC-03)', 'balance', '40', 0.50),

(4, 2, 1, 'Calculate primary producer biomass requirement: If primary consumers require 500kg of food and energy transfer efficiency is 10%, how much plant biomass is required?', 
 '10% efficiency means producer biomass = 500 / 0.10.', 'Cell Energy & Respiration', 'calculate', '5000', 5.00),
(5, 2, 2, 'Set the greenhouse CO2 absorption rate to balance 1200 ppm excess production across 4 biological scrubbers.', 
 'Divide 1200 ppm by 4 scrubbers.', 'Chemical Cycles', 'balance', '300', 1.00),
(6, 2, 3, 'Determine maximum allowable apex predator population where each predator requires 50 herbivores from a herd of 200.', 
 '200 / 50.', 'Trophic Cascades', 'configure', '4', 0.00),

(7, 3, 1, 'Set ultrasonic sensor obstacle stop distance. If braking deceleration is 2 m/s² and approach velocity is 4 m/s, calculate stopping distance d = v² / (2a).', 
 'd = (4*4) / (2*2) = 16 / 4.', 'Kinematics Equations', 'calculate', '4', 0.10),
(8, 3, 2, 'Configure the loop sample rate in milliseconds so the sensor polls at exactly 50 Hz.', 
 'Time period T in ms = 1000 / frequency.', 'Control Loops (CTRL-02)', 'configure', '20', 0.50),
(9, 3, 3, 'Calibrate wheel motor differential power offset to correct a 5-degree rightward drift.', 
 'Enter offset value 5 to compensate.', 'Feedback Loops', 'debug', '5', 0.00),

(10, 4, 1, 'Lander mass is 1500 kg. If gravity deceleration is 3.7 m/s² on Mars and upward acceleration target is 2.3 m/s², compute total thrust force in Newtons: F = m*(g+a).', 
 'F = 1500 * (3.7 + 2.3) = 1500 * 6.0.', 'Newton Laws (NEWT-02)', 'calculate', '9000', 10.00),
(11, 4, 2, 'Lander velocity must drop from 60 m/s to 0 m/s at deceleration a = 6 m/s². Calculate retrograde thruster burn duration in seconds: t = v / a.', 
 't = 60 / 6.', 'Kinematics 1D (KIN-01)', 'calculate', '10', 0.10),
(12, 4, 3, 'Set final touchdown damping gear dampening coefficient to absorb 3000 Joules over 0.5 meters: F_damping = Energy / distance.', 
 'F = 3000 / 0.5.', 'Work & Energy', 'configure', '6000', 5.00);

-- 17. Seed Questions
INSERT INTO questions (id, concept_id, difficulty, question_text, question_type, option_a, option_b, option_c, option_d, correct_answer, explanation, retheme_theme) VALUES
(1, 4, 'EASY', 'What is the median of the data set: 3, 7, 8, 12, 15?', 'multiple_choice', '7', '8', '9', '12', '8', 'When ordered, the middle value of 5 elements is the 3rd element, which is 8.', 'standard'),
(2, 4, 'MEDIUM', 'If the mean of 5 observations is 20 and one observation is removed so the new mean is 18, what was the removed value?', 'multiple_choice', '24', '26', '28', '30', '28', 'Total sum was 5*20 = 100. New sum for 4 items is 4*18 = 72. Removed value = 100 - 72 = 28.', 'standard'),
(3, 4, 'HARD', 'A sensor array records deviations with sum of squared deviations equal to 360 across 10 readings. What is the variance?', 'multiple_choice', '30', '36', '40', '6', '36', 'Variance = Sum of squared deviations / N = 360 / 10 = 36.', 'Space'),
(4, 5, 'EASY', 'A fair 6-sided die is rolled. What is the probability of rolling a prime number (2, 3, or 5)?', 'multiple_choice', '1/3', '1/2', '2/3', '5/6', '1/2', 'There are 3 prime numbers {2, 3, 5} out of 6 possible outcomes, so 3/6 = 1/2.', 'standard'),
(5, 5, 'MEDIUM', 'Two independent navigation beacons each have a 90% chance of functioning. What is the probability that at least one beacon functions?', 'multiple_choice', '0.81', '0.90', '0.99', '0.95', '0.99', 'P(at least one) = 1 - P(both fail) = 1 - (0.10 * 0.10) = 1 - 0.01 = 0.99.', 'Space'),
(6, 1, 'EASY', 'Simplify the expression: 3(x + 4) - 2x.', 'multiple_choice', 'x + 4', 'x + 12', '5x + 12', 'x - 12', 'x + 12', 'Distribute: 3x + 12 - 2x = x + 12.', 'standard'),
(7, 3, 'MEDIUM', 'If f(x) = 2x² - 3x + 1, what is the value of f(3)?', 'multiple_choice', '8', '10', '12', '14', '10', 'f(3) = 2*(9) - 3*(3) + 1 = 18 - 9 + 1 = 10.', 'standard');

-- 18. Seed Career Paths & Career Skills
INSERT INTO career_paths (id, title, field_category, education_level, description, growth_outlook) VALUES
(1, 'Aerospace Systems & Autonomous Navigation', 'Aerospace & Robotics', 'Grade 10 / PUC / Diploma', 'Designs satellite guidance algorithms, lunar landers, and telemetry analytics.', 'High Growth (+28% by 2030)'),
(2, 'Machine Learning & Applied Data Scientist', 'AI & Computing', 'PUC / Diploma / Professional', 'Builds predictive models, neural architectures, and intelligent adaptive algorithms.', 'Exceptional Growth (+36%)'),
(3, 'Ecological Resource & Sustainable Tech Specialist', 'Environmental Science', 'Grade 10 / PUC / Degree', 'Optimizes agricultural yields, manages closed-loop biosystems, and renewable microgrids.', 'Rapid Growth (+22%)'),
(4, 'Embedded Robotics & Automation Engineer', 'Mechatronics & Hardware', 'Diploma / ITI / Engineering', 'Programs microcontrollers, sensor debouncers, and factory automation pipelines.', 'High Growth (+25%)');

INSERT INTO career_skills (career_path_id, skill_name, importance_level, related_course_id) VALUES
(1, 'Orbital Mechanics & Dynamics', 'Essential', 4),
(1, 'Statistical Variance & Probability', 'Essential', 1),
(2, 'Linear Algebra & Statistics', 'Essential', 1),
(2, 'Python Algorithm Implementation', 'Essential', 3),
(3, 'Trophic Energy Balance', 'Essential', 2),
(4, 'Sensor Signal Filtering', 'Essential', 3),
(4, 'Closed-Loop Control Logic', 'Essential', 3);

-- 19. Seed Adaptive Timetable for Rahul
INSERT INTO timetables (id, student_id, day_name, available_hours) VALUES
(1, 1, 'Monday', 4.5);

INSERT INTO timetable_sessions (id, timetable_id, start_time, activity_name, activity_type, duration_minutes, concept_id, is_adaptive) VALUES
(1, 1, '09:00', 'Regular School Session', 'school', 210, NULL, 0),
(2, 1, '12:30', 'Nutritious Lunch & Rest', 'lunch', 45, NULL, 0),
(3, 1, '16:30', 'Save the Space Station Mission (Statistics)', 'mission', 25, 4, 1),
(4, 1, '17:00', 'Mindfulness Break & Hydration', 'break', 30, NULL, 0),
(5, 1, '17:30', 'Biology Video: Trophic Cascades', 'learning', 20, 9, 1),
(6, 1, '18:00', 'Sports & Outdoor Free Time', 'free_time', 60, NULL, 0),
(7, 1, '19:00', 'Guided Statistics Variance Practice', 'practice', 25, 4, 1),
(8, 1, '19:30', 'Dinner with Family', 'dinner', 60, NULL, 0),
(9, 1, '20:30', 'Prerequisite Algebra Quick Revision', 'revision', 20, 1, 1),
(10, 1, '21:00', 'Personal Wind-Down Time', 'personal', 45, NULL, 0);

-- 20. Seed Communities & Posts
INSERT INTO communities (id, name, course_id, description, icon) VALUES
(1, 'Grade 10 Mathematics Pioneers', 1, 'Collaborative peer forum for mastering algebraic concepts, statistical challenges, and probability puzzles.', 'calculator'),
(2, 'Sustainable Science Innovators', 2, 'Hands-on ecological experiments, biology discussions, and environmental project ideas.', 'leaf'),
(3, 'Robotics & Hardware Makers Club', 3, 'Sharing sensor code, PID debug techniques, and micro-controller builds.', 'cpu');

INSERT INTO community_posts (id, community_id, user_id, concept_id, title, content, post_type) VALUES
(1, 1, 2, 4, 'Intuitive way to remember Population vs Sample Variance?', 
 'Hey everyone! When calculating sample variance, we divide by (N - 1) instead of N. This is called Bessel correction. Think of it as accounting for the fact that sample mean is an estimate of true population mean, which reduces degrees of freedom by 1!', 
 'peer_hint'),
(2, 1, 1, 4, 'Struggling with deviations from mean in Mission 1 Step 2', 
 'In Step 2 of Save the Space Station, my buffer was off by 40 units. Make sure you square the difference (20^2 = 400) rather than multiplying by 2!', 
 'discussion'),
(3, 1, 6, 4, 'Facilitator Note: Live Review on Probability Foundations tomorrow at 5 PM', 
 'For students working toward unlocking Probability (PROB-05), we will review sample space diagrams and independent events during open office hours.', 
 'announcement');

INSERT INTO community_comments (id, post_id, user_id, comment_text, is_solution) VALUES
(1, 2, 2, 'Great catch Rahul! That exact square step tripped me up on my first run too.', 1);

-- 21. Seed Study Groups & Projects
INSERT INTO study_groups (id, name, course_id, concept_id, topic, description, max_members) VALUES
(1, 'Probability Beginners', 1, 5, 'Probability Rules & Independence', 'Peer group dedicated to mastering prerequisite statistics and unlocking compound probability missions.', 12);

INSERT INTO study_group_members (group_id, student_id) VALUES
(1, 1),
(1, 2);

INSERT INTO projects (id, title, subject_tags, description, status, facilitator_feedback) VALUES
(1, 'Smart Agriculture IoT & Yield Predictor', 'Science + Computer Science', 'Design an autonomous greenhouse monitoring sensor network that measures soil nitrogen and triggers irrigation pumps based on probabilistic rainfall models.', 'active', 'Excellent cross-disciplinary design. Ensure sensor noise filters are modeled in your state diagram.');

INSERT INTO project_members (project_id, student_id, role) VALUES
(1, 1, 'Data Modeler (Statistics)'),
(1, 3, 'Sensor Systems Developer');
