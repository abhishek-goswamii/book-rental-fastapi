pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'docker-compose up -d' 
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pip install -r requirements.txt'  
                sh 'python3 venv/bin/pytest' 
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                // Add your deployment steps here
            }
        }
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                sh 'docker-compose down'  // Stop and remove the containers
            }
        }
    }
}
