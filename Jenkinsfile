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
                        script {
                            def sshCommand = """
                                chmod 400 awsbookrentalkey.pem
                                ssh -o StrictHostKeyChecking=no -i awsbookrentalkey.pem ubuntu@ec2-43-204-214-79.ap-south-1.compute.amazonaws.com '
                                    whoami
                                    docker ps
                                    cd book-rental-fastapi
                                    docker-compose down
                                    docker-compose up -d
                                '
                            """
                            sh sshCommand
                        }
                        echo 'Deployed successfully!'
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
