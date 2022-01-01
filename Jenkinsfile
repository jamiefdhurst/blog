/* groovylint-disable CompileStatic */
CONTAINER_NAME = 'blog'

pipeline {
    agent any

    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Build') {
        steps {
            sh "docker build -t $CONTAINER_NAME -f Dockerfile.test ."
        }
    }

    stage('Test') {
        steps {
            sh """
            docker run -d --name $CONTAINER_NAME --entrypoint='' -e GITHUB_USERNAME='jamiefdhurst' -e GITHUB_TOKEN='example' $CONTAINER_NAME tail -f /dev/null
            docker exec -it $CONTAINER_NAME -- coverage -m pytest --verbose --junit-xml tests.xml
            docker exec -it $CONTAINER_NAME -- coverage xml -o coverage.xml
            docker cp $CONTAINER_NAME:/app/tests.xml blog-tests.xml
            docker cp $CONTAINER_NAME:/app/coverage.xml blog-coverage.xml
            """
            junit 'blog-tests.xml'
            step([$class: 'CoberturaPublisher', coberturaReportFile: 'blog-coverage.xml'])
        }
    }

    post {
        always {
            sh """
            docker stop $CONTAINER_NAME
            docker rm $CONTAINER_NAME
            """
        }
    }
}
