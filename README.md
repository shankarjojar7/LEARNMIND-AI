# LEARNMIND AI — Your Personal AI Teacher

**Hackathon track:** Generative AI & Intelligent Applications  
**Tagline:** Upload. Understand. Practice. Master.

LearnMind turns student notes into a personalized learning workspace: upload PDF/TXT/Markdown, ask questions, generate quizzes, create study plans, and review learning insights.

## Implemented MVP
- Streamlit web interface with Learning Studio, Quiz Arena, Study Planner, and Progress
- PDF/TXT/Markdown text extraction
- Learner level, language, and teaching-style personalization
- Amazon Bedrock Converse API integration
- Quiz generation with JSON validation and demo fallback
- Study plan generation and basic learning analytics
- Optional S3 upload and DynamoDB progress-event persistence
- Automated tests

**Important:** If `AWS_REGION` is blank, the app runs in demo mode. Demo mode is not live generative AI. Clearly distinguish it during judging.

## Windows PowerShell setup
```powershell
cd path\to\LEARNMIND_AI_Hackathon
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```
Open `http://localhost:8501`.

## Tests
```powershell
python -m pytest -q
```

## Enable Amazon Bedrock
1. Select an AWS region that supports your chosen foundation model.
2. Enable/request model access in Amazon Bedrock if your account requires it.
3. Configure credentials via AWS CLI profile, environment credentials, or IAM role. Never hardcode or share secret keys.
4. Set `AWS_REGION` and `BEDROCK_MODEL_ID` in `.env`.
5. Grant the identity `bedrock:InvokeModel` for the selected model.
6. Restart Streamlit and test a real tutor prompt.

The default model ID is an example and may not be available in every region/account. Verify availability in your AWS console.

## Optional AWS persistence
Create an S3 bucket and a DynamoDB table with string partition key `id`. Set `S3_BUCKET` and `DYNAMODB_TABLE`. Uploaded files use the `learning-materials/` prefix and AES256 server-side encryption. Use least-privilege IAM, private buckets, and retention policies.

## AWS architecture
**Runnable MVP:** Streamlit + Bedrock Converse + optional S3 and DynamoDB.

**Production/serverless target:** CloudFront + S3 static frontend; API Gateway; Lambda orchestration; Bedrock; S3 private materials; DynamoDB progress; Cognito authentication; CloudWatch logs/metrics. This target architecture is documented, not pre-deployed. Do not claim it is deployed unless you deploy and verify it.

## 3-minute demo
1. Explain the problem: students have notes but lack personalized explanations and practice.
2. Upload a small text-based PDF or paste a short chapter.
3. Choose Beginner and Hindi/Marathi.
4. Ask for a simple explanation and example.
5. Generate a 5-question quiz and submit answers.
6. Generate a 7-day study plan.
7. Show quiz accuracy and weak-topic insight.
8. Explain Bedrock, and demonstrate S3/DynamoDB only if configured.

## Responsible AI and privacy
- Do not upload sensitive student records for a public demo.
- Treat AI output as assistance; verify important facts with course materials.
- Keep credentials out of source control.
- Add authentication, user isolation, retention, and deletion controls before public launch.

## Limitations
- Scanned PDFs need OCR (not included).
- Analytics are session-scoped unless DynamoDB is configured.
- No login/multi-user isolation in this MVP.
- Bedrock model access varies by region/account.
- Generated educational content is not guaranteed correct.

## Windows PowerShell quick start

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and configure AWS_REGION, BEDROCK_MODEL_ID and AWS credentials for live AI.
streamlit run app.py
```

Run tests with `python -m pytest -q`.

### Important implementation notes

- Without AWS configuration, the app clearly labels its tutor/quiz/planner as demo or template behavior; it does not claim to generate live AI answers.
- Live AI requires an AWS account, Bedrock model access in the selected region, and credentials with least-privilege Bedrock permissions.
- Optional S3 and DynamoDB persistence require their resources and IAM permissions to be configured. Persistence failures are surfaced in the UI.
- Uploaded documents are limited to 10 MB and 50,000 extracted characters. Scanned/image-only PDFs need OCR, which is not included.
- This starter app has no user authentication or multi-user data isolation. Do not deploy it publicly with real student data until authentication, authorization, retention controls, and per-user isolation are implemented.
- The serverless AWS architecture in `docs/architecture.md` is a proposed deployment design, not a deployed environment.
