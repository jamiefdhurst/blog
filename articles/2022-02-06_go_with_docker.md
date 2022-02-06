# Go With Docker

![Docker Whale with a Gopher](/static/docker-go.png)

## I explain how to use Docker with my a simple web server in Go, how that can be integrated that into a build pipeline in Jenkins to illustrate test results and code coverage.

Building a web server or application with Go may not be everyone's first choice, but there are some significant 
advantages to think about: a strongly-typed language makes everything a little more predictable and Go still makes 
things nice and easy to get started with some built-in libraries, you can easily extend out and test what you need, and 
of course Go is extremely lightweight and fast - your application will be able to handle a lot of throughput right out 
of the box. Also, why not, it's fun!

This article will take you through an example web server (nothing complicated, a simple healthcheck) and how to build a 
full pipeline to ensure this can be tested and iterated over using Jenkins.

To get started, you'll need to have the following installed on your local machine:

* Go
* Docker

That should be all you need locally, but to take advantage of the Jenkins part of this tutorial you'll need a Jenkins 
setup somewhere.

### Go! Your HTTP Server

Create a new folder in your GOPATH (e.g. /src/github.com/{you}/http-go) and create a main.go file as follows:

```go
package main

import (
	"fmt"
	"net/http"
)

func index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi there!")
}

func main() {
	http.HandleFunc("/", index)
	http.ListenAndServe(":8080", nil)
}
```

This really is going to be a simple example! You can test this now by launching your server:

```bash
go run main.go
```

And then testing it with cURL, where you'll see "Hi there!":

```bash
curl http://localhost:8080/
```

### Testing

To prove all of this works, we need to test it. Being a very simple HTTP router at present, that will be very straight 
forward. Create a test file as main_test.go:

```go
package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestIndex(t *testing.T) {
	req, err := http.NewRequest("GET", "/", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(index)

	handler.ServeHTTP(rr, req)

	expected := "Hi there!"
	if rr.Body.String() != expected {
		t.Errorf("Method returned unexpected body: got %v want %v",
			rr.Body.String(), expected)
	}
}
```

This test will create an HTTP server, handle a request, return the response and check it against what ws expected. In 
this case, we want to see "Hi there!" so that's what we test against.

Try this with:

```bash
go test
```

### Containerising Your App

Now comes the fun part - the app is working in a basic fashion and there's a test in place, so let's containerise it!
Create a Dockerfile with the following:

```
FROM golang:1.15

WORKDIR /go/src/github.com/{you}/http-go
COPY . .

RUN go install

EXPOSE 8080

CMD ["http-go"]
```

This means you can now build and run your app using Docker instead:

```bash
docker build -t http-go:latest .
docker run --name http-go --rm -p 8080:8080 http-go:latest
```

### Integrating with Jenkins

To ready the application for Jenkins, firstly create another Dockerfile (Dockerfile.test) which will include a couple 
of different libraries to allow test report and code coverage exports to work with Jenkins' Cobertura and Xunit 
plugins:

```
FROM golang:1.15

WORKDIR /go/src/github.com/{you}/http-go
COPY . .

RUN go install
RUN go get github.com/tebeka/go2xunit
RUN go get github.com/t-yuki/gocover-cobertura

EXPOSE 8080

CMD ["http-go"]
```

Now a Jenkinsfile can be created that will be used to set up your tests remotely:

```groovy
/* groovylint-disable CompileStatic */
CONTAINER_NAME = 'http-go'

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
                docker run --name $CONTAINER_NAME $CONTAINER_NAME sh -c 'go test -coverprofile=cover.out -v ./... | go2xunit; gocover-cobertura < cover.out > coverage.xml' > tests.xml
                docker cp $CONTAINER_NAME:/go/src/github.com/{you}/http-go/coverage.xml coverage.xml
                """
                junit 'tests.xml'
                step([$class: 'CoberturaPublisher', coberturaReportFile: 'coverage.xml'])
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
```

Now - this would be a good time to push your code to git so Jenkins can fetch it. Once that's in place, create a new 
multibranch pipeline in Jenkins:

![Setting up the initial multibranch pipeline in Jenkins](/static/docker-go-jenkins-1.png)

And add in the following config (replacing the configuration as necessary):

![Adding the GitHub source](/static/docker-go-jenkins-2.png)
![Configuring the Jenkinsfile](/static/docker-go-jenkins-3.png)

Once this is complete, your build should be ready to run and should start automatically:

![Branches available in the Jenkins project](/static/docker-go-jenkins-4.png)
![Build running on the main branch](/static/docker-go-jenkins-5.png)

As an output, you can see the test reports and code coverage too:

![Final output of test results and code coverage](/static/docker-go-jenkins-6.png)

### Next Steps

Next up, there'll be a follow-up article around how you can build some infrastructure to support your new application, 
using Docker and Supervisor to have an automated deployment from Jenkins.

The full code for this article is available here: [https://github.com/jamiefdhurst/go-http-example](https://github.com/jamiefdhurst/go-http-example)
