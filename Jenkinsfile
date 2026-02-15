pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Rapor için --junitxml parametresi şart
                sh 'venv/bin/pytest --junitxml=report.xml'
            }
        }
    }
    post {
        always {
            // Jenkins arayüzünde test sonuçlarını tablo yapar
            junit 'report.xml'
            
            // Ekran görüntülerini (fail durumunda) build sayfasında saklar
            // screenshots klasörün varsa orayı hedefler
            archiveArtifacts artifacts: '**/screenshots/*.png, report.xml', allowEmptyArchive: true

            print "Screenshots and reports archived successfully!"
        }
    }
}
