node {
    def mvnHome = tool 'Maven'
   
    stage ('----Pull----') {
        git 'https://github.com/aszaryk/verademo.git'
    }

    stage('----Veracode Dynamic Analysis API----'){
        withCredentials([usernamePassword(credentialsId: 'veracode-credentials',passwordVariable: 'VeraPW', usernameVariable: 'VeraID')]){
        sh 'python3 "$WORKSPACE/update-da-scan.py"'           
             }
        }
}    