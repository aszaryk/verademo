node {
    def mvnHome = tool 'Maven'
   
    stage ('----Pull----') {
        git 'https://github.com/aszaryk/verademo.git'
    }
    stage('----Create Veracode Dynamic Analysis Scan----'){
        withCredentials([usernamePassword(credentialsId: 'veracode-credentials',passwordVariable: 'VeraPW', usernameVariable: 'VeraID')]){
        sh 'python3 "$WORKSPACE/jenkins-create-da-scan.py"'           
             }
        }
    stage('----Veracode Dynamic Analysis Scan Now----'){
        withCredentials([usernamePassword(credentialsId: 'veracode-credentials',passwordVariable: 'VeraPW', usernameVariable: 'VeraID')]){
        sh 'python3 "$WORKSPACE/jenkins-update-da-scan.py"'           
             }
        }
}    