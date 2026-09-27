# AI Text Summarizer

A simple, responsive web application that uses Generative AI (Google Gemini API) to summarize text. This project demonstrates core DevOps principles including Containerization (Docker), Orchestration (Kubernetes), and CI (GitHub Actions).

## Project Overview
This project provides a clean user interface to paste long text and receive a concise summary. It acts as a complete end-to-end college DevOps demo, showing how to build, test, containerize, and deploy a modern AI application locally.

## Architecture
- **Frontend**: HTML5, Vanilla CSS (Custom design), Vanilla JavaScript.
- **Backend**: Python 3.11 with FastAPI.
- **AI/LLM**: Google Gemini API (`gemini-3.8-flash`).
- **Containerization**: Docker.
- **Orchestration**: Kubernetes (Local using Docker Desktop).
- **CI/CD**: GitHub Actions.

## Technologies Used
- Python 3.11+, FastAPI, Uvicorn, pytest
- Docker
- Kubernetes (`kubectl`)
- Git & GitHub Actions

## Project Structure
```text
genai-text-summarizer/
├── app/                  # Main application code
│   ├── main.py           # FastAPI backend
│   ├── templates/        # HTML templates
│   │   └── index.html
│   └── static/           # CSS and JS
│       ├── style.css
│       └── script.js
├── tests/                # Pytest tests
│   └── test_app.py
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
├── .github/workflows/    # CI Pipeline
│   └── ci.yml
├── Dockerfile            # Docker image definition
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # Documentation
```

## Local Setup

### Environment Variables
1. Create a `.env` file in the root directory based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your actual Gemini API key (DO NOT commit this file to Git):
   ```env
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-3.8-flash
   ```

### Running Locally (Without Docker)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Access the application in your browser at `http://localhost:8000`.

### Running Tests
Tests use `pytest` and mock the Gemini API so they do not consume credits.
```bash
pytest tests/
```

## Docker Setup
Build and run the application using Docker.

1. Build the Docker image:
   ```bash
   docker build -t genai-summarizer .
   ```
2. Run the Docker container (passing the `.env` file for the API key):
   ```bash
   docker run --env-file .env -p 8000:8000 genai-summarizer
   ```
3. Access the application at `http://localhost:8000`.

## Kubernetes Setup

Ensure you have Kubernetes enabled in Docker Desktop.

1. **Create the Kubernetes Secret**
   We use a Secret so we don't hardcode the API key in the deployment YAML.
   ```bash
   # Replace YOUR_API_KEY with your actual Gemini API key
   kubectl create secret generic gemini-secret --from-literal=api-key=YOUR_API_KEY
   ```

2. **Apply the Manifests**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Check the Status**
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. **Access the Application**
   Open your browser and navigate to `http://localhost:30080`.
   *(Note: The service uses NodePort 30080)*

### Kubernetes Scaling Demo
To demonstrate horizontal scaling:

1. Check current replicas (should be 2):
   ```bash
   kubectl get pods
   ```
2. Scale up to 4 replicas:
   ```bash
   kubectl scale deployment genai-summarizer --replicas=4
   ```
3. Verify the new pods are running:
   ```bash
   kubectl get pods
   ```

## GitHub Actions
The project includes a Continuous Integration (CI) pipeline located at `.github/workflows/ci.yml`.
On every push or pull request to the `main` branch, the pipeline will:
1. Set up a Python environment.
2. Install all dependencies.
3. Run the automated tests (`pytest`).
4. Build the Docker image to verify it builds successfully.

## DevOps Concepts Demonstrated
- **Version control**: Tracking code changes safely.
- **CI**: Automatically running tests and builds in GitHub Actions.
- **Automated testing**: Preventing regressions without consuming external API credits.
- **Containerization**: Packaging the app securely with Docker.
- **Kubernetes Pods & Deployments**: Managing container lifecycle and desired state.
- **Kubernetes Services**: Exposing the application to the network.
- **Horizontal scaling**: Adding more replicas dynamically.
- **Secrets management**: Injecting API keys safely via Kubernetes Secrets and environment variables.

## Future Improvements
- Add persistent storage to keep a history of summaries (e.g., PostgreSQL).
- Implement user authentication.
- Deploy to a managed cloud Kubernetes service (AKS, EKS, GKE).
- Push images to a container registry (Docker Hub/GHCR) during CI/CD.
