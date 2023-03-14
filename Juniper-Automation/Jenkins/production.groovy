pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], 
                          userRemoteConfigs: [[url: 'https://github.com/IPvZero/JenkinsPipeline.git']]])
            }
        }
        stage('Pull Docker Image') {
            steps {
                sh 'docker pull ipvzero/nornir_demo:latest'
            }
        }
        stage('Run Container and Execute Script') {
            steps {
                sh 'docker run -t --entrypoint /bin/bash ipvzero/nornir_demo:latest -c "cd automation && git pull && git checkout main && pylint script1.py --fail-under=7 && python3 script1.py prod_config.yaml"'
            }
        }
    }
    post {
        success {
            slackSend(channel: "#automation", token: "bIciXaK9JByxOFC0FEEfPsfn", color: "good", message: "The production pipeline execution was successful. :white_check_mark:")
        }
        failure {
            slackSend(channel: "#automation", token: "bIciXaK9JByxOFC0FEEfPsfn", color: "danger", message: "The production pipeline execution failed. :x:")
        }
    }
}
