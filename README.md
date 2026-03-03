# IBU NBA/E Operations — Executive Summary Dashboard

## Overview
Streamlit dashboard replicating the Overview_1 Excel layout with Azure OpenAI GPT-4.1 integration for AI-powered insights and Q&A.

## Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure secrets
# Edit .streamlit/secrets.toml with your Azure OpenAI credentials and Lilly logo URL

# 3. Run
streamlit run app.py
```

## SageMaker Deployment

### Option A: SageMaker Studio / Notebook Instance

```bash
# SSH into SageMaker or open a terminal in Studio

# 1. Upload the streamlit_dashboard folder to your SageMaker instance
# 2. Navigate to the directory
cd streamlit_dashboard

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
mkdir -p .streamlit
# Edit .streamlit/secrets.toml with your credentials

# 5. Run Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# 6. Access via:
# - SageMaker Studio: Use the proxy URL provided
# - Notebook Instance: https://<instance-name>.notebook.<region>.sagemaker.aws/proxy/8501/
```

### Option B: SageMaker with Docker

Create a Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Configuration

### .streamlit/secrets.toml
```toml
[azure_openai]
endpoint = "https://your-instance.cognitiveservices.azure.com/"
model_name = "gpt-4.1"
deployment = "gpt-4.1"
api_key = "YOUR_KEY_HERE"
api_version = "2024-12-01-preview"

[branding]
logo_url = "https://your-sharepoint-url/lilly-logo.png"
```

### Environment Variables (Alternative)
If you prefer environment variables over secrets.toml:
```bash
export AZURE_OPENAI_ENDPOINT="https://..."
export AZURE_OPENAI_KEY="..."
```

## Security Notes
- **NEVER** commit secrets.toml to version control
- Add `.streamlit/secrets.toml` to `.gitignore`
- Rotate API keys regularly
- Use Azure Key Vault for production deployments

## Architecture
```
app.py                    # Main Streamlit application
requirements.txt          # Python dependencies
.streamlit/
  secrets.toml           # Credentials (git-ignored)
README.md                # This file
```

## Features
- Executive summary layout matching Overview_1 Excel tab
- Lilly Red branding with configurable logo
- GPT-4.1 banner insight (auto-generated, cached 1hr)
- GPT-4.1 market insights (auto-generated, cached 1hr)
- Interactive Q&A search bar for leadership questions
- Plotly charts (incident trends, resource utilisation, category breakdown)
- Static business health metrics (manually updatable)
- APAC market expansion risk card
- Print-friendly layout
# IBU-Leadership-Dashboard
# IBU-Leadership-Dashboard
# IBU-Leadership-Dashboard
# IBU-Leadership-Dashboard
