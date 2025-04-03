# TechTrends Testing Guide

This document provides comprehensive instructions for testing the TechTrends application at various stages of deployment, from local development to Kubernetes and ArgoCD deployments.

## Table of Contents

1. [Local Application Testing](#local-application-testing)
2. [Docker Container Testing](#docker-container-testing)
3. [Kubernetes Deployment Testing](#kubernetes-deployment-testing)
4. [Helm Chart Testing](#helm-chart-testing)
5. [ArgoCD Deployment Testing](#argocd-deployment-testing)
6. [Troubleshooting](#troubleshooting)
7. [Required Screenshots for Project Rubric](#required-screenshots-for-project-rubric)

## Local Application Testing

### Prerequisites

- Python 2.7 installed
- Required Python packages installed (see `requirements.txt`)

### Steps

1. Initialize the database:
   ```bash
   cd techtrends
   python init_db.py
   ```
   Expected output: "Initialized the database."

2. Run the application:
   ```bash
   python app.py
   ```
   Expected output: "* Running on http://127.0.0.1:3111/ (Press CTRL+C to quit)"

3. Test the application by accessing the following endpoints in your browser:
   - Home page: http://127.0.0.1:3111/
   - About page: http://127.0.0.1:3111/about
   - Create new post: http://127.0.0.1:3111/create
   - Health check: http://127.0.0.1:3111/healthz
   - Metrics: http://127.0.0.1:3111/metrics

4. Test the application functionality:
   - View existing posts by clicking on their titles
   - Create a new post using the "Create" form
   - Try accessing a non-existent post (e.g., http://127.0.0.1:3111/1000) to verify the 404 page

5. Check the logs in the terminal to verify that the application is logging events correctly.

## Docker Container Testing

### Prerequisites

- Docker installed and running

### Steps

1. Build the Docker image:
   ```bash
   docker build -t techtrends:latest .
   ```
   Expected output: "Successfully built [image_id]" and "Successfully tagged techtrends:latest"

2. Run the Docker container:
   ```bash
   docker run -d -p 7111:3111 techtrends:latest
   ```
   Expected output: Container ID (a long string of characters)

3. Test the application by accessing the following endpoints in your browser:
   - Home page: http://localhost:7111/
   - About page: http://localhost:7111/about
   - Create new post: http://localhost:7111/create
   - Health check: http://localhost:7111/healthz
   - Metrics: http://localhost:7111/metrics

4. Check the container logs:
   ```bash
   docker logs [container_id]
   ```
   Expected output: Application logs showing startup and request handling

5. Take a screenshot of the application running in the browser, including the navigation bar, and save it as "docker-run-local" in the "screenshots" folder.

6. Stop the container when done:
   ```bash
   docker stop [container_id]
   ```

## Kubernetes Deployment Testing

### Prerequisites

- Kubernetes cluster running (e.g., Minikube, k3s, or a cloud provider)
- kubectl configured to connect to your cluster

### Steps

1. Verify that your Kubernetes cluster is running:
   ```bash
   kubectl get nodes
   ```
   Expected output: List of nodes with STATUS "Ready"

2. Take a screenshot of the output and save it as "k8s-nodes" in the "screenshots" folder.

3. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -f kubernetes/namespace.yaml
   kubectl apply -f kubernetes/deploy.yaml
   kubectl apply -f kubernetes/service.yaml
   ```
   Expected output: "namespace/sandbox created", "deployment.apps/techtrends created", "service/techtrends created"

4. Verify that the resources were created:
   ```bash
   kubectl get all -n sandbox
   ```
   Expected output: List of resources including pod, service, deployment, and replicaset

5. Take a screenshot of the output and save it as "kubernetes-declarative-manifests" in the "screenshots" folder.

6. Wait for the pod to be in the "Running" state:
   ```bash
   kubectl wait --for=condition=Ready pods --all -n sandbox --timeout=120s
   ```
   Expected output: "pod/techtrends-[pod_id] condition met"

7. Forward the service port to access the application:
   ```bash
   kubectl port-forward service/techtrends 4111:4111 -n sandbox
   ```
   Expected output: "Forwarding from 127.0.0.1:4111 -> 3111"

8. Test the application by accessing the following endpoints in your browser:
   - Home page: http://localhost:4111/
   - About page: http://localhost:4111/about
   - Create new post: http://localhost:4111/create
   - Health check: http://localhost:4111/healthz
   - Metrics: http://localhost:4111/metrics

9. Check the pod logs:
   ```bash
   kubectl logs -n sandbox $(kubectl get pods -n sandbox -o jsonpath="{.items[0].metadata.name}")
   ```
   Expected output: Application logs showing startup and request handling

## Helm Chart Testing

### Prerequisites

- Kubernetes cluster running
- Helm installed
- kubectl configured to connect to your cluster

### Steps

1. Install the Helm chart with default values:
   ```bash
   helm install techtrends-default ./helm
   ```
   Expected output: "NAME: techtrends-default", "NAMESPACE: default", "STATUS: deployed"

2. Verify that the resources were created:
   ```bash
   kubectl get all -n sandbox
   ```
   Expected output: List of resources including pod, service, deployment, and replicaset

3. Wait for the pod to be in the "Running" state:
   ```bash
   kubectl wait --for=condition=Ready pods --all -n sandbox --timeout=120s
   ```
   Expected output: "pod/techtrends-[pod_id] condition met"

4. Forward the service port to access the application:
   ```bash
   kubectl port-forward service/techtrends 4111:4111 -n sandbox
   ```
   Expected output: "Forwarding from 127.0.0.1:4111 -> 3111"

5. Test the application by accessing the following endpoints in your browser:
   - Home page: http://localhost:4111/
   - About page: http://localhost:4111/about
   - Create new post: http://localhost:4111/create
   - Health check: http://localhost:4111/healthz
   - Metrics: http://localhost:4111/metrics

6. Install the Helm chart with staging values:
   ```bash
   helm install techtrends-staging ./helm -f helm/values-staging.yaml
   ```
   Expected output: "NAME: techtrends-staging", "NAMESPACE: default", "STATUS: deployed"

7. Verify that the resources were created in the staging namespace:
   ```bash
   kubectl get all -n staging
   ```
   Expected output: List of resources including pods (3 replicas), service, deployment, and replicaset

8. Install the Helm chart with production values:
   ```bash
   helm install techtrends-prod ./helm -f helm/values-prod.yaml
   ```
   Expected output: "NAME: techtrends-prod", "NAMESPACE: default", "STATUS: deployed"

9. Verify that the resources were created in the prod namespace:
   ```bash
   kubectl get all -n prod
   ```
   Expected output: List of resources including pods (5 replicas), service, deployment, and replicaset

10. Uninstall the Helm charts when done:
    ```bash
    helm uninstall techtrends-default techtrends-staging techtrends-prod
    ```
    Expected output: "release "techtrends-default" uninstalled", "release "techtrends-staging" uninstalled", "release "techtrends-prod" uninstalled"

## ArgoCD Deployment Testing

### Prerequisites

- Kubernetes cluster running
- ArgoCD installed
- kubectl configured to connect to your cluster

### Steps

1. Verify that ArgoCD is running:
   ```bash
   kubectl get pods -n argocd
   ```
   Expected output: List of ArgoCD pods with STATUS "Running"

2. Access the ArgoCD UI:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
   Expected output: "Forwarding from 127.0.0.1:8080 -> 8080"

3. Open your browser and navigate to https://localhost:8080

4. Log in to ArgoCD using the default credentials (username: admin, password: can be retrieved using `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`)

5. Take a screenshot of the ArgoCD UI, including the navigation bar, and save it as "argocd-ui" in the "screenshots" folder.

6. Apply the ArgoCD application manifests:
   ```bash
   kubectl apply -f argocd/helm-techtrends-staging.yaml
   kubectl apply -f argocd/helm-techtrends-prod.yaml
   ```
   Expected output: "application.argoproj.io/techtrends-staging created", "application.argoproj.io/techtrends-prod created"

7. Verify that the applications are created in ArgoCD:
   ```bash
   kubectl get applications -n argocd
   ```
   Expected output: List of applications including "techtrends-staging" and "techtrends-prod"

8. Wait for the applications to be synchronized:
   ```bash
   kubectl wait --for=condition=Synced applications techtrends-staging techtrends-prod -n argocd --timeout=300s
   ```
   Expected output: "application.argoproj.io/techtrends-staging condition met", "application.argoproj.io/techtrends-prod condition met"

9. Verify that the resources were created in the staging and prod namespaces:
   ```bash
   kubectl get all -n staging
   kubectl get all -n prod
   ```
   Expected output: List of resources including pods, services, deployments, and replicasets

10. Take a screenshot of the "techtrends-staging" application in the ArgoCD UI, with synchronized resources (all should be up and running), and save it as "argocd-techtrends-staging" in the "screenshots" folder.

11. Take a screenshot of the "techtrends-prod" application in the ArgoCD UI, with synchronized resources (all should be up and running), and save it as "argocd-techtrends-prod" in the "screenshots" folder.

12. Delete the applications when done:
    ```bash
    kubectl delete -f argocd/helm-techtrends-staging.yaml
    kubectl delete -f argocd/helm-techtrends-prod.yaml
    ```
    Expected output: "application.argoproj.io/techtrends-staging deleted", "application.argoproj.io/techtrends-prod deleted"

## Troubleshooting

### 1. Database initialization fails

If you encounter issues with database initialization:

- Make sure you're in the correct directory (techtrends)
- Check if the database file already exists and if it's writable
- Verify that the schema.sql file exists and is readable

### 2. Application doesn't start

If the application fails to start:

- Check if the required Python packages are installed
- Verify that the port 3111 is not already in use
- Check the application logs for error messages

### 3. Docker daemon not running or connection issues

If you encounter the error "Cannot connect to the Docker daemon":

- Check if Docker is running:
  ```bash
  # For systemd-based systems (most Linux distributions)
  systemctl status docker

  # For SysVinit-based systems
  service docker status

  # For macOS
  docker info
  ```

- Start Docker if it's not running:
  ```bash
  # For systemd-based systems
  sudo systemctl start docker

  # For SysVinit-based systems
  sudo service docker start

  # For macOS, use the Docker Desktop application
  ```

- Check if you have permission to access the Docker socket:
  ```bash
  ls -l /var/run/docker.sock
  ```
  The output should show that the socket is owned by the docker group. If you're not in the docker group, add yourself:
  ```bash
  sudo usermod -aG docker $USER
  ```
  Then log out and log back in for the changes to take effect.

### 4. Docker container doesn't start

If the Docker container fails to start:

- Check if the port 7111 is already in use
- Verify that the Docker image was built successfully
- Check the container logs for error messages

### 5. Kubernetes pods are not in the "Running" state

If the Kubernetes pods are not in the "Running" state:

- Check the pod status for more details:
  ```bash
  kubectl describe pod -n sandbox $(kubectl get pods -n sandbox -o jsonpath="{.items[0].metadata.name}")
  ```
- Common issues include:
  - ImagePullBackOff: The image cannot be pulled from the registry
  - CrashLoopBackOff: The container is crashing repeatedly
  - Pending: The pod cannot be scheduled on a node
- For ImagePullBackOff issues:
  - Make sure the image exists in the registry
  - Check if authentication is required for the registry
  - For local development with Minikube, you may need to load the image into Minikube:
    ```bash
    minikube image load techtrends:latest
    ```
  - Or build the image directly inside Minikube:
    ```bash
    eval $(minikube docker-env)
    docker build -t techtrends:latest .
    ```
  - Update the deployment manifest to use `imagePullPolicy: Never` to prevent Kubernetes from trying to pull the image from a registry

### 6. Unable to connect to the Kubernetes cluster

If you encounter the error "Unable to connect to the server: dial tcp <IP>:<PORT>: connect: no route to host":

- Check if the cluster is running:
  ```bash
  minikube status
  ```
- If the cluster is stopped, start it:
  ```bash
  minikube start
  ```
- If starting fails with "Device or resource busy" errors, you may need to delete and recreate the cluster:
  ```bash
  minikube delete
  minikube start
  ```
- Verify the connection:
  ```bash
  kubectl get nodes
  ```

### 7. ArgoCD applications are not synchronizing

If the ArgoCD applications are not synchronizing:

- Check the application status:
  ```bash
  kubectl describe application -n argocd techtrends-staging
  kubectl describe application -n argocd techtrends-prod
  ```
- Common issues include:
  - Repository not accessible
  - Invalid Helm chart
  - Invalid values file
  - Missing Chart.yaml file
- If you see an error like "Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = Manifest generation error (cached): error getting helm repos: error retrieving helm dependency repos: error reading helm chart from <path to cached source>/helm/Chart.yaml: open <path to cached source>/helm/Chart.yaml: no such file or directory", it means ArgoCD cannot find the Chart.yaml file in your repository. Make sure:
  - The Chart.yaml file exists in the helm directory
  - The repository URL in the ArgoCD application manifest is correct
  - The path in the ArgoCD application manifest is correct
  - The repository is accessible from the Kubernetes cluster
- Verify that the repository is accessible and the Helm chart is valid:
  ```bash
  helm lint ./helm
  ```
- Check the ArgoCD logs for more details:
  ```bash
  kubectl logs -n argocd $(kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o jsonpath="{.items[0].metadata.name}")
  ```

## Required Screenshots for Project Rubric

To fulfill the project rubric requirements, you need to take the following screenshots:

### Docker Container Testing

- **docker-run-local**: Take a screenshot of the application running in the browser, including the navigation bar, after running the Docker container.

### Kubernetes Deployment Testing

- **k8s-nodes**: Take a screenshot of the output of the `kubectl get nodes` command.
- **kubernetes-declarative-manifests**: Take a screenshot of the output of the `kubectl get all -n sandbox` command after applying the Kubernetes manifests.

### CI/CD Screenshots

- **ci-github-actions**: Take a screenshot of a successful build of the Docker build and push GitHub action.
  1. Go to your GitHub repository
  2. Click on the "Actions" tab
  3. Click on the workflow run that built and pushed the Docker image
  4. Take a screenshot of the successful workflow run, showing all steps completed successfully

- **ci-dockerhub**: Take a screenshot of the DockerHub TechTrends image, with the tag "latest".
  1. Go to your DockerHub account
  2. Navigate to the TechTrends repository
  3. Take a screenshot showing the "latest" tag of the TechTrends image

### ArgoCD Deployment Testing

- **argocd-ui**: Take a screenshot of the ArgoCD UI, including the navigation bar, after logging in.
- **argocd-techtrends-staging**: Take a screenshot of the "techtrends-staging" application in the ArgoCD UI, with synchronized resources (all should be up and running).
- **argocd-techtrends-prod**: Take a screenshot of the "techtrends-prod" application in the ArgoCD UI, with synchronized resources (all should be up and running).
