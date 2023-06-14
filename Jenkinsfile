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
        // Construir la imagen de Docker para la aplicación Flask
        script {
          docker.build("flask-app:${env.BUILD_NUMBER}", './app')
        }
        
        // Construir la imagen de Docker para el contenedor de la base de datos
        script {
          docker.build("mysql-db:${env.BUILD_NUMBER}", './database')
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
