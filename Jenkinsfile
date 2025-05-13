// Jenkins Pipeline Definition
pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "kahoot-gradio-frontend"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = "okii225" 
        FULL_IMAGE_NAME = "${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
    }

    stage('Debug Env') {
        steps {
            sh '''
            echo "Running on OS:"
            uname -a
            echo "Docker version:"
            docker --version
            echo "kubectl version:"
            kubectl version --client
            '''
        }
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${env.FULL_IMAGE_NAME} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh """
                    echo ${env.DOCKER_PASSWORD} | docker login -u ${env.DOCKER_USERNAME} --password-stdin
                    """
                    sh "docker push ${env.FULL_IMAGE_NAME}"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                    kubectl set image deployment/frontend-deployment frontend=${env.FULL_IMAGE_NAME} --record
                    """
                }
            }
        }
    }

    post {
        always {
            echo '清理 Docker 映像...'
            sh "docker rmi ${env.FULL_IMAGE_NAME} || true"
        }
        success {
            echo '部署成功！'
        }
        failure {
            echo '部署失敗！'
        }
    }
}