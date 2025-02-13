Pipeline{
    agent any
    stages{
        stage("checkout"){
            steps{
                checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Umarsharief-07/python-new.git']])

            }
        }

        stage("Depencies install"){
                steps {
                script {
                    // Ensure virtualenv is used (optional)
                    sh 'python -m venv venv'  // Create a virtual environment
                    sh './venv/bin/pip install -r requirements.txt'  // Install dependencies inside virtualenv
                }
            }
        }

        stage("Docker install, image and run"){
            steps{
                
                sh "sudo apt-get update"
                sh "sudo apt-get install ca-certificates curl"
                
                sh "sudo install -m 0755 -d /etc/apt/keyrings"
                sh "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc"
                sh "sudo chmod a+r /etc/apt/keyrings/docker.asc"


                sh "echo \
  deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
                sh "sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
                sh "sudo apt-get update"
                sh "sudo chmod -aG docker ubuntu"
                sh ""
                sh "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
                sh "docker build -t python:new ."
                sh "docker run -d -p 5656:5656 python:new"
            }
        }
        }

        }
    }
}
