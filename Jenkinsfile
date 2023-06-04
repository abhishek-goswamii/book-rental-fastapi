pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'docker-compose down' 
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

        stage('Build and Push Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t abhishekgoswami/book_rental .'
                sh 'docker push abhishekgoswami/abhishekgoswami/book_rental'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
             
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
