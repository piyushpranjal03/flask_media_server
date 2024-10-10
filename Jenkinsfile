pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-media-server'
        GAMMA_PORT = '5000'
        PROD_PORT = '5001'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }
        
        stage('Gamma') {
            steps {
                script {
                    sh "docker stop gamma-${DOCKER_IMAGE} || true"
                    sh "docker rm gamma-${DOCKER_IMAGE} || true"
                    sh "docker run -d --name gamma-${DOCKER_IMAGE} -p ${GAMMA_PORT}:5000 ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Gamma Health Check') {
            steps {
                script {
                    sh "sleep 20" // Wait for the application to start
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${PROD_PORT}/videos/1.webm", returnStdout: true).trim()
                    if (response != "200") {
                        error "Gamma health check failed with status ${response}"
                    }
                }
            }
        }
        
        stage('Prod') {
            steps {
                input "Deploy to Production?"
                script {
                    sh "docker stop prod-${DOCKER_IMAGE} || true"
                    sh "docker rm prod-${DOCKER_IMAGE} || true"
                    sh "docker run -d --name prod-${DOCKER_IMAGE} -p ${PROD_PORT}:5000 ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Prod Health Check') {
            steps {
                script {
                    sh "sleep 10" // Wait for the application to start
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:${PROD_PORT}/videos/1.webm", returnStdout: true).trim()
                    if (response != "200") {
                        error "Production health check failed with status ${response}"
                    }
                }
            }
        }
    }
    
    post {
        failure {
            echo 'The Pipeline failed :('
        }
    }
}
