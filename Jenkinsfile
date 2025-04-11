pipeline {
    agent any

     environment {
        SCANNER_HOME=tool 'sonar-scanner'
     }

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Umarsharief-07/python-new.git']])
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run SonarQube analysis with SonarQube Scanner
                    withSonarQubeEnv('sonar-server') { // Use the SonarQube configuration name here
                        sh """
                            $SCANNER_HOME/bin/sonar-scanner \
                           -Dsonar.projectKey=python-n \
                           -Dsonar.sources=. 
                           """
                    }
                }
            }
        }
        stage("Quality Gate") {
            steps {
              timeout(time: 20, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true // we need to have webhook to do in sonarqube > project settings > webhook 
                } 
            }
        }
        

        stage('Docker Install, Image Build and Run') {
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
                sh "docker build -t new:n ."
                sh "docker stop python && docker rm python"
                sh "docker run -d --name python -p 5757:5000 new:n"
            }
        }
        stage("TRIVY Image Scan") { 
            steps {
                sh 'trivy image new:n > trivyimage.txt'
                archiveArtifacts artifacts: 'trivyimage.txt', allowEmptyArchive: true     
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
          
            cleanWs()
        }
    }
}
