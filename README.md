# TechTrends

Welcome to **TechTrends** – a cloud-native online news-sharing platform that I had the opportunity to build and deploy as a Platform Engineer.

## 🚀 Project Overview

TechTrends is a Python Flask-based web application designed to let users share and read articles related to the cloud-native ecosystem. Readers can view published news, access individual articles, and even submit their own content. The backend uses SQLite for lightweight and efficient local data storage.

The site includes:

- **About Page** – A brief overview of TechTrends.
- **Index Page** – Lists all available articles.
- **New Post Page** – A form to submit new articles.
- **404 Page** – Custom page rendered when a post does not exist.

The application's data is stored in a `POSTS` SQL table with the following schema:

| ID (Integer) | Created (Timestamp) | Title (Text) | Content (Text) |
|--------------|----------------------|--------------|----------------|

## 🧠 What I Learned

This project gave me hands-on experience with modern DevOps and cloud-native application delivery practices. As the Platform Engineer on the team, I was responsible for packaging, deploying, and automating the delivery pipeline of TechTrends. I enhanced my understanding of:

- **Best practices in Python application development**
- **Containerization using Docker**
- **Kubernetes declarative deployments**
- **Helm for templating Kubernetes manifests**
- **CI/CD implementation using GitHub Actions and ArgoCD**

## 🏆 My Achievements

Here's a summary of what I accomplished:

### ✅ Development Best Practices

- Developed `/healthz` and `/metrics` endpoints for monitoring application status and usage.
- Implemented structured logging to `STDOUT`/`STDERR` with timestamped logs for:
  - Article access
  - 404 pages
  - About page
  - New post creation

### 🐳 Dockerization

- Created a `Dockerfile` using **Python 2.7** as base.
- Installed dependencies from `requirements.txt`.
- Initialized the SQLite database with default posts via `init_db.py`.
- Exposed the app on **port 7111** and ran it on container start.
- Built and ran the image locally using Docker.

### ⚙️ Continuous Integration

- Set up a **GitHub Actions** pipeline to automatically build and push Docker images on each push to the main branch.
- Images were tagged as `techtrends:latest` and published to **DockerHub**.

### ☸️ Kubernetes Deployment

- Bootstrapped a **K3s cluster** using **Vagrant**.
- Created declarative manifests (`namespace.yaml`, `deploy.yaml`, `service.yaml`) to deploy TechTrends into a `sandbox` namespace.
- Configured **resource limits**, **readiness** and **liveness** probes, and service exposure.

### 📦 Helm Charting

- Built a complete Helm chart for the TechTrends app.
- Parameterized deployment configuration for flexible multi-environment support.
- Created separate values files for:
  - **Staging** (3 replicas, port 5111)
  - **Production** (5 replicas, port 7111, pull policy Always)

### 🔁 Continuous Delivery

- Installed and configured **ArgoCD**.
- Exposed ArgoCD via NodePort and synchronized Helm-based deployments.
- Created separate ArgoCD Application manifests for staging and production environments using custom values files.

## 🗂️ Project Structure

```
techtrends/
├── README.md               # This file
├── TESTING.md              # Testing guide for the application
├── app.py                  # Main application and logging logic
├── init_db.py              # DB initialization script
├── requirements.txt        # Python dependencies
├── schema.sql              # DB schema definition
├── templates/              # HTML templates (index, about, create, 404, post)
├── static/css/             # Stylesheet
├── __init__.py             # Marks the directory as a Python package
├── docker_commands         # All Docker CLI usage and output
├── kubernetes/             # YAML manifests for k8s deployment
├── helm/                   # Helm chart and values files
├── argocd/                 # ArgoCD application manifests
├── screenshots/            # Visual proof of completed tasks
└── Vagrantfile             # Vagrant box configuration for k3s cluster
```

## 🏁 Running the App Locally

To get started:

1. **Initialize the database:**
   ```bash
   python init_db.py
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Visit the app** at [http://127.0.0.1:7111](http://127.0.0.1:7111)

## 🧪 Testing the Application

For comprehensive testing instructions, please refer to the [TESTING.md](TESTING.md) guide. This guide includes:

- Instructions for testing the application locally
- Docker container testing procedures
- Kubernetes deployment testing steps
- Helm chart testing guidelines
- ArgoCD deployment testing instructions
- Troubleshooting tips for common issues
- Required screenshots for project rubric

Following this guide will ensure that all components of the TechTrends application are functioning correctly before submission.

## 📸 Reviewer Requirements

For specific instructions on how to meet the reviewer's requirements, please refer to the [INSTRUCTIONS.md](INSTRUCTIONS.md) guide. This guide includes:

- Instructions for verifying the application running on port 7111
- Steps to verify the Kubernetes deployment is in the RUNNING state
- Steps to verify the ArgoCD techtrends-prod application is in a healthy state
- Instructions for updating the required screenshots

---

I'm proud of what I achieved with TechTrends — not only in getting a cloud-native app into production but also in applying real-world DevOps principles every step of the way.