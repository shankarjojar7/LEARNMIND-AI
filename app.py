import os
import streamlit as st
from dotenv import load_dotenv
from services import extract_text, tutor_response, make_quiz, make_study_plan, analyze_weak_topics, save_to_s3, save_progress

load_dotenv()
st.set_page_config(page_title="LearnMind AI", page_icon="🧠", layout="wide")
st.markdown("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">", unsafe_allow_html=True)
st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 80% 0%,#20204b 0,#0b1020 42%,#080b14 100%);color:#f4f5ff}
[data-testid="stSidebar"]{background:#101629}
.hero{padding:26px 30px;border:1px solid #393b70;border-radius:22px;background:linear-gradient(120deg,#171e3a,#24204d);margin-bottom:22px}
.hero h1{font-size:42px;color:#fff;margin:0}.hero p{color:#c2c8e8}
.pill{display:inline-block;padding:5px 11px;border-radius:20px;background:#342b68;color:#c9baff;font-size:12px}
</style>""", unsafe_allow_html=True)

for key, default in {"notes":"","history":[],"quiz":None,"scores":[]}.items():
    if key not in st.session_state: st.session_state[key]=default

with st.sidebar:
    st.markdown("## 🧠 LEARNMIND AI")
    st.caption("Your Personal AI Teacher")
    page=st.radio("Workspace",["Learning Studio","Quiz Arena","Study Planner","My Progress","About"])
    st.divider()
    st.caption("AI ENGINE")
    st.write("Amazon Bedrock" if os.getenv("AWS_REGION") else "Demo mode — configure AWS")
    st.caption("Privacy-first learning workspace")

if page=="Learning Studio":
    st.markdown('<div class="hero"><span class="pill">GENERATIVE AI • PERSONALIZED LEARNING</span><h1>Learn anything. Your way.</h1><p>Upload notes, ask questions, and get explanations designed around your level.</p></div>',unsafe_allow_html=True)
    a,b=st.columns([1.15,.85])
    with a:
        st.subheader("📚 Your learning material")
        up=st.file_uploader("Upload PDF, TXT or Markdown notes (max 10 MB)",type=["pdf","txt","md"])
        if up:
            try:
                st.session_state.notes=extract_text(up)
                st.success(f"Loaded {up.name} — {len(st.session_state.notes):,} characters")
                if os.getenv("S3_BUCKET"):
                    try: save_to_s3(up.getvalue(),up.name); st.caption("Encrypted copy saved to configured S3 bucket.")
                    except Exception: st.warning("Notes loaded for this session, but the optional S3 backup failed. Check AWS configuration.")
            except Exception as e: st.error(str(e))
        pasted=st.text_area("Or paste your notes here",height=150)
        if st.button("Use pasted notes"): st.session_state.notes=pasted; st.success("Notes added.")
    with b:
        st.subheader("🎯 Personalize your lesson")
        st.session_state.profile={"level":st.selectbox("Your level",["Beginner","Intermediate","Advanced"]),
          "language":st.selectbox("Preferred language",["English","Hindi","Marathi","Hinglish"]),
          "style":st.selectbox("Teaching style",["Simple examples","Step-by-step","Analogy-based","Exam-focused"])}
        st.info("Add notes first for answers grounded in your material.")
    st.divider(); st.subheader("💬 Ask your AI teacher")
    q=st.chat_input("Ask about your notes or any topic...")
    for m in st.session_state.history[-8:]:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    if q:
        st.session_state.history.append({"role":"user","content":q})
        with st.chat_message("user"): st.markdown(q)
        with st.chat_message("assistant"):
            with st.spinner("Your tutor is thinking..."):
                ans=tutor_response(q,st.session_state.notes,st.session_state.get("profile",{}))
                st.markdown(ans)
        st.session_state.history.append({"role":"assistant","content":ans})
        try: save_progress("question",{"question":q,"answer":ans[:400]})
        except Exception: st.warning("Answer generated, but optional progress persistence failed.")

elif page=="Quiz Arena":
    st.markdown('<div class="hero"><span class="pill">ACTIVE RECALL</span><h1>Quiz Arena</h1><p>Turn your notes into a personalized challenge.</p></div>',unsafe_allow_html=True)
    topic=st.text_input("Quiz topic",placeholder="e.g. Photosynthesis, Python loops")
    difficulty=st.select_slider("Difficulty",["Easy","Medium","Hard"])
    count=st.slider("Number of questions",3,10,5)
    if st.button("Generate quiz",type="primary"):
        with st.spinner("Creating quiz..."): st.session_state.quiz=make_quiz(topic,st.session_state.notes,difficulty,count)
    quiz=st.session_state.quiz
    if quiz:
        st.subheader(quiz.get("title","Your quiz")); answers={}
        if quiz.get("warning"): st.warning(quiz["warning"])
        if quiz.get("demo"): st.info("Demo questions — connect Amazon Bedrock for topic-specific AI questions.")
        for i,item in enumerate(quiz["questions"]):
            st.markdown(f"**Q{i+1}. {item['question']}**")
            answers[str(i)]=st.radio("Choose one",item["options"],key=f"answer_{i}",index=None,label_visibility="collapsed")
        if st.button("Submit answers",type="primary"):
            score=sum(answers.get(str(i))==item["answer"] for i,item in enumerate(quiz["questions"]))
            result={"topic":topic or "General","score":score,"total":len(quiz["questions"])}
            st.session_state.scores.append(result)
            try: save_progress("quiz",result)
            except Exception: st.warning("Score saved in this session, but optional database persistence failed.")
            st.success(f"Score: {score}/{len(quiz['questions'])}")
            with st.expander("Review answers",expanded=True):
                for i,item in enumerate(quiz["questions"]):
                    st.write(f"Q{i+1}: **{item['answer']}** — {item.get('explanation','')}")
    else: st.caption("Generate a quiz to begin.")

elif page=="Study Planner":
    st.markdown('<div class="hero"><span class="pill">PERSONALIZED ROADMAP</span><h1>Your study plan</h1><p>Turn a big goal into achievable daily sessions.</p></div>',unsafe_allow_html=True)
    goal=st.text_input("What do you want to learn?")
    days=st.slider("Days available",1,30,7); hours=st.slider("Hours per day",.5,8.0,2.0,.5)
    if st.button("Create my plan",type="primary"):
        try:
            with st.spinner("Building your roadmap..."): st.markdown(make_study_plan(goal,days,hours,st.session_state.notes))
            try: save_progress("study_plan",{"goal":goal,"days":days,"hours":hours})
            except Exception: st.warning("Plan created, but optional progress persistence failed.")
        except ValueError as e: st.error(str(e))

elif page=="My Progress":
    st.markdown('<div class="hero"><span class="pill">LEARNING ANALYTICS</span><h1>Your progress</h1><p>See what you practiced and where to focus next.</p></div>',unsafe_allow_html=True)
    scores=st.session_state.scores; total=sum(x["total"] for x in scores); correct=sum(x["score"] for x in scores)
    c1,c2,c3=st.columns(3); c1.metric("Quizzes",len(scores)); c2.metric("Questions",total); c3.metric("Accuracy",f"{round(correct/total*100) if total else 0}%")
    if scores:
        st.dataframe(scores,use_container_width=True)
        if st.button("Analyze weak topics"): st.markdown(analyze_weak_topics(scores))
    else: st.info("Complete a quiz to start tracking progress.")

else:
    st.markdown('<div class="hero"><span class="pill">ABOUT THE PROJECT</span><h1>LearnMind AI</h1><p>An adaptive AI tutor for accessible, measurable learning.</p></div>',unsafe_allow_html=True)
    st.markdown("""
**Features:** source-grounded explanations, multilingual teaching styles, automatic quizzes, study plans, and progress insights.

**AWS:** Amazon Bedrock for generation, S3 for optional uploaded-material storage, DynamoDB for optional learning-event persistence. A production serverless path is documented in `docs/architecture.md`.

**Responsible AI:** Model outputs can be wrong. Verify important facts against course materials. Do not upload sensitive student data.
""")
