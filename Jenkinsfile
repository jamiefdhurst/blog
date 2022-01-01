/* groovylint-disable CompileStatic */
CONTAINER_NAME = 'blog'

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "docker build -t $CONTAINER_NAME -f Dockerfile.test ."
            }
        }

        stage('Test') {
            steps {
                sh """
                docker run -d --name $CONTAINER_NAME --entrypoint='' -e GITHUB_USERNAME='jamiefdhurst' -e GITHUB_TOKEN='example' $CONTAINER_NAME tail -f /dev/null
                docker exec $CONTAINER_NAME coverage run -m pytest --verbose --junit-xml tests.xml
                docker exec $CONTAINER_NAME coverage xml -o coverage.xml
                docker cp $CONTAINER_NAME:/app/tests.xml blog-tests.xml
                docker cp $CONTAINER_NAME:/app/coverage.xml blog-coverage.xml
                """
                junit 'blog-tests.xml'
                step([$class: 'CoberturaPublisher', coberturaReportFile: 'blog-coverage.xml'])
            }
        }

        stage('Package') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-personal-access-token', usernameVariable: 'GITHUB_USERNAME', passwordVariable: 'GITHUB_PASSWORD')]) {
                    sh "docker login -u $GITHUB_USERNAME -p $GITHUB_PASSWORD docker.pkg.github.com"
                    sh """
                    docker tag $CONTAINER_NAME docker.pkg.github.com/jamiefdhurst/blog/blog:latest
                    docker push docker.pkg.github.com/jamiefdhurst/blog/blog:latest
                    """
                }
            }
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
