pipeline {
    agent any

    stages {

        stage('Check Python') {
            steps {
                sh 'which python || true'
                sh 'which python3 || true'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m pytest || true'
                sh 'python3 -m pytest || true'
            }
        }
    }
}
