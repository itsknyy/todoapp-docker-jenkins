## 📘 Detailed Implementation Guide

### Step 1 – Build Frontend Docker Image

![Jenkins Build](images/image-1.png)

```
docker build -t todo-app-frontend:v0 .
```

- Docker reads the `Dockerfile`.
- Pulls the required base image `(nginx)`.
- Builds the frontend image.
- Tags it as `todo-app-frontend:v0`.

---

### Step 2 – Build Backend Docker Image

![Jenkins Build](images/image-2.png)

```
docker build -t todo-app-backend:v0 .
```

- Docker reads the backend Dockerfile.
- Pulls the base image `(python:3.11-alpine)`.
- Installs dependencies from requirements.txt.
- Builds and tags the image as `todo-app-backend:v0`.

---

### Step 3 – Tag and Push Frontend Image to Docker Hub

![Jenkins Build](images/image-3.png)

```
docker tag todo-app-frontend:v0 itsknyy/todo-app-frontend:v0
docker push itsknyy/todo-app-frontend:v0
```

- Tags the local image with your Docker Hub username.
- Pushes the image to Docker Hub.

> Note: Repeat the same steps for the backend image (todo-app-backend:v0).

---

### Step 4 – Verify Images on Docker Hub

![Jenkins Build](images/image-5.png)

- Confirm that both images are listed:
    - `itsknyy/todo-app-frontend`
    - `itsknyy/todo-app-backend`

---

### Step 5 – SSH into EC2 and Prepare docker-compose

![Jenkins Build](images/image-6.png)

```
ssh -i ec2.pem ubuntu@<EC2-PUBLIC-IP>
mkdir todo-app && cd todo-app
touch docker-compose.yaml
```

- Connects to the EC2 instance using SSH.
- Creates a project directory (todo-app).
- Creates the docker-compose.yaml file for defining deployment services.

---

### Step 6 – Create Jenkins Pipeline Job

![Jenkins Build](images/image-7.png)

- Go to Jenkins Dashboard → New Item.
- Select `Pipeline` as the project type.
- Click OK to create the pipeline job.

---

### Step 7 – Connect Jenkins to GitHub Repo

![Jenkins Build](images/image-8.png)

- Select `Pipeline script from SCM`.
- Choose Git and add your repository URL.
- Set branch to */main.
- Keep script path as Jenkinsfile.
- Click Save.

---

### Step 8 – Add Jenkins Credentials

![Jenkins Build](images/image-9.png)

- Go to Manage Jenkins → Credentials.
- Add Docker Hub credentials (username & password/token).
- Add EC2 SSH private key (for remote deployment).

---

