import streamlit as st
from classbuild.generator import generate_course_outline, generate_lesson_content, generate_quiz

st.set_page_config(page_title="Mini ClassBuild", layout="centered")
st.title("Mini ClassBuild 🎓")
st.write("An AI-powered app to generate interactive educational courses and quizzes.")

if "outline" not in st.session_state:
    st.session_state.outline = None
if "lessons" not in st.session_state:
    st.session_state.lessons = {}
if "quizzes" not in st.session_state:
    st.session_state.quizzes = {}
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = {}

with st.form("course_form"):
    topic = st.text_input("Course Topic:")
    difficulty = st.radio("Difficulty:", ["Beginner", "Intermediate", "Advanced"])
    lesson_count = st.slider("Number of Lessons:", min_value=2, max_value=5, value=3)
    submit_button = st.form_submit_button("Generate Course Outline")

if submit_button:
    if not topic.strip():
        st.warning("⚠️ Please enter a Course Topic first.")
    else:
        with st.spinner("🤖 AI is generating your course outline..."):
            try:
                result = generate_course_outline(topic, difficulty, lesson_count)
                st.session_state.outline = result
                st.session_state.lessons = {}
                st.session_state.quizzes = {}
                st.session_state.quiz_results = {}
                st.success("✅ Course generated successfully!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

if st.session_state.outline:
    outline = st.session_state.outline
    course_title = outline.get("course_title", "Untitled Course")
    
    st.subheader(course_title)
    st.write(f"**Level:** {outline.get('difficulty_level', difficulty)}")
    
    for i, lesson in enumerate(outline.get("lessons", [])):
        lesson_num = i + 1
        lesson_title = lesson.get('title')
        
        with st.expander(f"Lesson {lesson_num}: {lesson_title}"):
            st.write(f"**Objective:** {lesson.get('objective')}")
            
            # محتوى الدرس
            if lesson_num in st.session_state.lessons:
                content = st.session_state.lessons[lesson_num]
                st.markdown("---")
                st.write(content.get('introduction', ''))
                
                for section in content.get('sections', []):
                    st.markdown(f"#### {section.get('heading')}")
                    st.write(section.get('explanation'))
                    if section.get('example'):
                        st.info(f"**Example:** {section.get('example')}")
                        
                st.markdown("#### Summary")
                st.write(content.get('summary', ''))
                
                st.markdown("#### Exercises")
                for ex in content.get('exercises', []):
                    st.success(f"**Task:** {ex.get('question')}\n\n**Hint:** {ex.get('hint')}")
                
                st.markdown("---")
                st.subheader("📝 Lesson Quiz")
                
                # قسم الاختبار (Quiz)
                if lesson_num not in st.session_state.quizzes:
                    if st.button(f"Generate Quiz for Lesson {lesson_num}", key=f"gen_quiz_{lesson_num}"):
                        with st.spinner("Generating quiz..."):
                            try:
                                # دمج محتوى الدرس كنص لإرساله للنموذج
                                lesson_text = content.get('introduction', '') + "\n" + "\n".join([s.get('explanation', '') for s in content.get('sections', [])])
                                q_data = generate_quiz(course_title, difficulty, lesson_num, lesson_title, lesson_text)
                                st.session_state.quizzes[lesson_num] = q_data
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error generating quiz: {e}")
                else:
                    quiz_data = st.session_state.quizzes[lesson_num]
                    
                    if lesson_num in st.session_state.quiz_results:
                        # عرض النتيجة إذا تم حل الاختبار مسبقاً
                        res = st.session_state.quiz_results[lesson_num]
                        st.success(f"🎯 Your Score: {res['correct_count']} / {res['total_questions']} ({res['percentage']}%)")
                        
                        for idx, qr in enumerate(res['details']):
                            st.write(f"**Q{idx+1}: {qr['question']}**")
                            if qr['is_correct']:
                                st.success(f"Your answer: {qr['selected_text']} ✅")
                            else:
                                st.error(f"Your answer: {qr['selected_text']} ❌")
                                st.info(f"Correct answer: {qr['correct_text']}")
                            st.write(f"*Explanation:* {qr['explanation']}")
                            st.markdown("---")
                            
                        if st.button("🔄 Retake Quiz", key=f"retake_{lesson_num}"):
                            del st.session_state.quiz_results[lesson_num]
                            st.rerun()
                    else:
                        # نموذج عرض الأسئلة للاختبار
                        with st.form(f"quiz_form_{lesson_num}"):
                            user_answers = {}
                            for q_idx, q in enumerate(quiz_data.get("questions", [])):
                                st.write(f"**Q{q_idx+1}: {q.get('question')}**")
                                choice = st.radio("Choose an option:", q.get("options"), key=f"q_{lesson_num}_{q_idx}", index=None)
                                user_answers[q_idx] = choice
                                st.markdown("")
                                
                            submitted = st.form_submit_button("Submit Quiz Answers")
                            if submitted:
                                if None in user_answers.values():
                                    st.warning("⚠️ Please answer all questions before submitting.")
                                else:
                                    # التصحيح المحلي (Local Grading) بدون استذكار الذكاء الاصطناعي
                                    correct_count = total = len(quiz_data.get("questions", []))
                                    details = []
                                    score = 0
                                    
                                    for q_idx, q in enumerate(quiz_data.get("questions", [])):
                                        selected_text = user_answers[q_idx]
                                        options = q.get("options")
                                        selected_idx = options.index(selected_text)
                                        correct_idx = q.get("correct_answer")
                                        is_correct = (selected_idx == correct_idx)
                                        
                                        if is_correct:
                                            score += 1
                                            
                                        details.append({
                                            "question": q.get("question"),
                                            "selected_text": selected_text,
                                            "correct_text": options[correct_idx],
                                            "is_correct": is_correct,
                                            "explanation": q.get("explanation")
                                        })
                                        
                                    percentage = int((score / total) * 100)
                                    st.session_state.quiz_results[lesson_num] = {
                                        "correct_count": score,
                                        "total_questions": total,
                                        "percentage": percentage,
                                        "details": details
                                    }
                                    st.rerun()
            else:
                if st.button(f"Generate Lesson {lesson_num} Content", key=f"btn_{lesson_num}"):
                    with st.spinner("Generating lesson content..."):
                        try:
                            lesson_content = generate_lesson_content(course_title, difficulty, lesson_num, lesson_title)
                            st.session_state.lessons[lesson_num] = lesson_content
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error generating lesson: {e}")