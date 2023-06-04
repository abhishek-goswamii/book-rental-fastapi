pipeline {
    agent any
    stages {
        // stage('Setup') {
        //     steps {
        //         echo 'Setting up environment...'
        //         sh 'docker-compose down' 
        //         sh 'docker-compose up -d' 
        //     }
        // }
        // stage('Test') {
        //     steps {
        //         echo 'Running tests...'
        //         sh 'pip install -r requirements.txt'  
        //         sh 'python3 venv/bin/pytest' 
        //     }
        // }

        // stage('Build and Push Image') {
        //     steps {
        //         echo 'Building Docker image...'
        //         sh 'docker build -t abhishekgoswami/book_rental .'
                
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub_id', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
        //             sh 'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD'
        //         }
                
        //         sh 'docker push abhishekgoswami/book_rental'
        //     }
        // }

        stage('Deploy') {
                steps {
                    echo 'Deploying....'
                    sh 'chmod 400 awsbookrentalkey.pem' // Set the correct permissions for the key file
                    sshagent(['ssh-credentials-id']) {
                        sh 'ssh -o StrictHostKeyChecking=no -i awsbookrentalkey.pem ubuntu@ec2-43-204-214-79.ap-south-1.compute.amazonaws.com'
                        sh 'whoami'
                        sh 'docker ps'
                        sh 'cd book-rental-fastapi'
                        sh 'docker-compose down'
                        sh 'docker-compose up -d'
                    }
                    sh 'echo "Deployed successfully!"'
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
