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
                docker run -d --name $CONTAINER_NAME --entrypoint='' -e GITHUB_USERNAME='jamiefdhurst' -e GITHUB_TOKEN='example' $CONTAINER_NAME-test tail -f /dev/null
                docker exec $CONTAINER_NAME coverage run -m pytest --verbose --junit-xml tests.xml
                docker exec $CONTAINER_NAME coverage xml -o coverage.xml
                docker cp $CONTAINER_NAME:/app/tests.xml blog-tests.xml
                docker cp $CONTAINER_NAME:/app/coverage.xml blog-coverage.xml
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
                library identifier: 'infrastructure@master'
                build job: '/github/blog-folder/deploy', wait: true, parameters: [
                    string(name: 'targetVersion', value: getVersion(repo: 'jamiefdhurst/blog').full)
                ]
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
