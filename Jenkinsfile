node {
    def mvnHome = tool 'Maven'
   
    stage ('----Pull----') {
        git 'https://github.com/aszaryk/verademo.git'
    }
    stage('----Create Veracode Dynamic Analysis Scan----'){
        withCredentials([usernamePassword(credentialsId: 'veracode-credentials',passwordVariable: 'VeraPW', usernameVariable: 'VeraID')]){
        sh 'python3 "$WORKSPACE/create-da-scan.py"'           
             }
        }
    stage('----Veracode Dynamic Analysis Scan Now----'){
        withCredentials([usernamePassword(credentialsId: 'veracode-credentials',passwordVariable: 'VeraPW', usernameVariable: 'VeraID')]){
        sh 'python3 "$WORKSPACE/update-da-scan.py"'           
             }
        }
}    