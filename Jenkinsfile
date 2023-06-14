pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        // Clonar el repositorio del proyecto
        git 'https://github.com/TheK321/URLShortener.git'
      }
    }

   stage('Build Docker Images') {
    steps {
      script {
        def buildNumber = env.BUILD_NUMBER ?: 'unknown'
        docker.build("flask-app:${buildNumber}", './app')
        docker.build("mysql-db:${buildNumber}", './database')
      }
    }
   }

    stage('Deploy') {
      steps {
        // Iniciar los contenedores usando Docker Compose
        script {
          sh 'docker-compose up -d'
        }
      }
    }
  }

  post {
    always {
      // Eliminar los contenedores y limpiar los recursos
      script {
        sh 'docker-compose down'
        sh 'docker rmi flask-app:${env.BUILD_NUMBER}'
        sh 'docker rmi mysql-db:${env.BUILD_NUMBER}'
      }
    }
  }
}
