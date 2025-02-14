pipeline{
    agent any
    stages{
        stage("checkout"){
            steps{
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Umarsharief-07/python-new.git']])

            }
        
        stage("Code analysis"){
            environment{
                SONAR_URL = http://15.207.18.50:9000/
            }
            steps{
            withCredentials([string(credentialsId: 'Sonarqube', variable: 'SONAR_AUTH_TOKEN')]) {
            sh 'cd  python-new/spring-boot-app && mvn sonar:sonar -Dsonar.login=$SONAR_AUTH_TOKEN -Dsonar.host.url=$(SONAR_URL) '
}
        }        

    
        


        stage("Docker install, image and run"){
            steps{
                
                sh "sudo apt-get update"
                sh "sudo apt-get install ca-certificates curl"
                
                sh "sudo install -m 0755 -d /etc/apt/keyrings"
                sh "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc"
                sh "sudo chmod a+r /etc/apt/keyrings/docker.asc"


                sh '''#!/bin/bash
                    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc
                    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                    sudo apt-get update
                    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
                    sudo usermod -aG docker ubuntu
                    '''
                sh ""
                sh "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
                sh "sudo chmod 777 /var/run/docker.sock"
                sh "docker build -t umarsharief07/ultimate-cicd:${BUILD_NUMBER} ."
                sh "docker stop python && docker rm python"
                sh "docker run -d --name python -p 5757:5000 umarsharief07/ultimate-cicd:${BUILD_NUMBER}"
                
            }
        }

        stage("docker push"){
            steps{
            
withDockerRegistry(credentialsId: 'DOC_CRED', url: 'https://index.docker.io/v1/') {
                sh " docker push umarsharief07/ultimate-cicd:${BUILD_NUMBER}"
    
}
    }
 }
    }
}    

