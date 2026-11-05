# Hackathon judging checklist — 60 points

| Criterion | Max | Evidence |
|---|---:|---|
| Event Theme | 10 | Generative AI tutor, quiz generation, personalized reasoning |
| AWS Implementation / Deployment | 10 | Live Bedrock call; S3/DynamoDB if configured; explain architecture |
| Idea and Problem Statement | 15 | Clear student pain point and learn-practice-measure-adapt loop |
| UI/UX | 5 | Learning Studio, Quiz Arena, Study Planner, Progress |
| Business Model / Scale | 10 | Freemium, Pro, institutional licensing, serverless scale path |
| Codebases and README | 10 | Organized source, setup, tests, architecture, limitations |

## Pre-demo
- [ ] Verify Bedrock model access in target region
- [ ] Test a real Bedrock tutor prompt
- [ ] Test quiz and study-plan generation
- [ ] Test S3 and DynamoDB if claiming them
- [ ] Run `python -m pytest -q`
- [ ] Use non-sensitive sample notes
- [ ] Keep screenshots/video backup
- [ ] Distinguish live AWS features from demo-mode fallback
