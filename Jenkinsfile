pipeline{
    agent any
    stages{
        stage("checkout"){
            steps{
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Umarsharief-07/python-new.git']])

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
                sh "docker build -t python:try ."
                sh "docker run -d -p 5656:5656 python:try"
            }
        }
    }
 }
    

