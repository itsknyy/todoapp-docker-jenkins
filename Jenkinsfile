pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub')
        IMAGE_BACKEND = "itsknyy/todoapp-backend"
        IMAGE_FRONTEND = "itsknyy/todoapp-frontend"
        EC2_IP = "52.206.53.110"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Images') {
            steps {
                sh """
                docker build -t $IMAGE_BACKEND:${BUILD_NUMBER} ./backend
                docker build -t $IMAGE_FRONTEND:${BUILD_NUMBER} ./frontend
                """
            }
        }

        stage('Docker Login') {
            steps {
                sh """
                echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                """
            }
        }

        stage('Push Images') {
            steps {
                sh """
                docker push $IMAGE_BACKEND:${BUILD_NUMBER}
                docker push $IMAGE_FRONTEND:${BUILD_NUMBER}
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                withCredentials([string(credentialsId: 'ec2-key-base64', variable: 'SSH_KEY')]) {
                    sh '''
                    echo "$SSH_KEY" | base64 -d > ec2.pem
                    chmod 600 ec2.pem

                    ssh -o StrictHostKeyChecking=no -i ec2.pem ubuntu@52.206.53.110 "
                    cd ~/todo-app &&
                    export APP_VERSION=${BUILD_NUMBER} &&
                    docker compose pull &&
                    docker compose up -d --force-recreate
                    "
                    '''
                }
            }
        }
    }
}