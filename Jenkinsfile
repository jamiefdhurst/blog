/* groovylint-disable CompileStatic */
CONTAINER_NAME = 'blog'

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "docker build -t $CONTAINER_NAME-test -f Dockerfile.test ."
            }
        }

        stage('Test') {
            steps {
                sh """
                docker run -d --name $CONTAINER_NAME-test --entrypoint='' -e GITHUB_USERNAME='jamiefdhurst' -e GITHUB_TOKEN='example' $CONTAINER_NAME-test tail -f /dev/null
                docker exec $CONTAINER_NAME-test coverage run -m pytest --verbose --junit-xml tests.xml
                docker exec $CONTAINER_NAME-test coverage xml -o coverage.xml
                docker cp $CONTAINER_NAME-test:/app/tests.xml blog-tests.xml
                docker cp $CONTAINER_NAME-test:/app/coverage.xml blog-coverage.xml
                """
                junit 'blog-tests.xml'
                step([$class: 'CoberturaPublisher', coberturaReportFile: 'blog-coverage.xml'])
            }
        }

        stage('Package and Release') {
            when {
                branch 'main'
            }
            steps {
                sh "docker build -t $CONTAINER_NAME -f Dockerfile ."
                build job: '/github/blog-folder/release', wait: true
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                library identifier: 'jenkins@main'
                build job: '/github/blog-folder/deploy', wait: true, parameters: [
                    string(name: 'targetVersion', value: getVersion(repo: 'jamiefdhurst/blog').full)
                ]
            }
        }
    }

    post {
        always {
            sh """
            docker stop $CONTAINER_NAME-test
            docker rm $CONTAINER_NAME-test
            """
        }
    }
}
