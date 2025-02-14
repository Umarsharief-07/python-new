pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SONAR_CRED')  // Jenkins credentials ID for SonarQube token
    }

    stages {
        stage("Checkout") {
            steps {
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Umarsharief-07/python-new.git']])
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run SonarQube analysis with SonarQube Scanner
                    withSonarQubeEnv('SonarQube') { // Use the SonarQube configuration name here
                        sh """
                            sonar-scanner \
                                -Dsonar.projectKey=My-Python-Project \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://15.207.18.50:9000 \
                                -Dsonar.login=${SONAR_TOKEN}  // Use the token from Jenkins credentials
                        """
                    }
                }
            }
        }

        stage("Docker Install, Image Build and Run") {
            steps {
                sh "sudo apt-get update"
                sh "sudo apt-get install -y ca-certificates curl"

                sh "sudo install -m 0755 -d /etc/apt/keyrings"
                sh "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc"
                sh "sudo chmod a+r /etc/apt/keyrings/docker.asc"

                sh '''
                    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc
                    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                    sudo apt-get update
                    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
                    sudo usermod -aG docker ubuntu
                '''
                sh "sudo chmod 777 /var/run/docker.sock"
                sh "docker build -t umarsharief07/ultimate-cicd:${BUILD_NUMBER} ."
                sh "docker stop python && docker rm python"
                sh "docker run -d --name python -p 5757:5000 umarsharief07/ultimate-cicd:${BUILD_NUMBER}"
            }
        }

        stage("Docker Push") {
            steps {
                withDockerRegistry(credentialsId: 'DOC_CRED', url: 'https://index.docker.io/v1/') {
                    sh "docker push umarsharief07/ultimate-cicd:${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        always {
            // Clean workspace inside a node block
            node {
                cleanWs()  // Clean workspace after the build completes
            }
        }
    }
}
