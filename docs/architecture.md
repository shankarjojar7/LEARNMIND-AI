# Architecture

## Implemented MVP
```text
Student -> Streamlit UI -> services.py -> Amazon Bedrock Converse
                                   |-> optional S3 (materials)
                                   |-> optional DynamoDB (progress events)
```

## Production serverless target
```text
Browser -> CloudFront -> S3 static frontend -> API Gateway -> Lambda orchestration
                                                       |-> Bedrock
                                                       |-> S3 private materials
                                                       |-> DynamoDB progress
                                                       |-> CloudWatch
Cognito provides identity and access management.
```

The serverless target is a proposal, not a deployed stack in this MVP.

## Security controls before public launch
- Cognito authentication and per-user authorization
- Private S3 bucket, block public access, encryption, lifecycle expiry
- Upload size/type validation and presigned URLs
- Lambda throttling, quotas, and input limits
- Treat uploaded content as untrusted; defend against prompt injection
- No arbitrary code execution
- PII minimization and deletion controls
- Never log secrets or full private notes
