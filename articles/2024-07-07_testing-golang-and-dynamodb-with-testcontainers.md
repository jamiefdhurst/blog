# Testing Golang and AWS DynamoDB with TestContainers

![Walking Towards a Set of Shipping Containers with Go Logo and DynamoDB Logo Above](/static/golang-dynamodb.png)

## While trying out a refactor for my [Journal](https://github.com/jamiefdhurst/journal) and a move towards more native AWS services with Lambda and DynamoDB, trying to fully test the application without using an AWS account itself started to become challenging. This article gives an overview of how you can use DynamoDB with Golang, and how to use TestContainers, something I've used extensively with Java, in place of a docker compose setup to wrap your Go tests.

Quite a few years ago, I built a simple Journal application in Go as a means to learn the language. It started as a simple web interface with an API to interact with externally, powered by a SQLite database behind the scenes. This made it small, portable and easy for me to run anywhere I wanted while I was trying things out. I came to rely on it more and more for documenting my personal thoughts, and started to think this might be something not only useful for myself, but also for others.

Up until now, it's been hosted on a private VM, most recently on an Amazon EC2 alongside some of my other websites, including this blog. However, I wanted to move towards a more serverless experience, and given how small application is and how low its requirements are, it's the perfect candidate for running on Lambda. In order to do that, I needed to move away from SQLite and towards something that allowed me to extract the state from the local filesystem. Given it only stores posts with a title, content and date, something very straight-forward like DynamoDB would be absolutely ideal.

Rather than use the Journal application, which is a little more complex these ays with migrations and slightly more opinionated testing setup, starting fresh with something that only includes a simple JSON API might be a little easier for this article.

Let's build a very simple Scoreboard API in Go.

### REST Handlers with Go

I'm going to keep this as simple as possible - so minimal number of files and package separation only when necessary. This will mean using very simple HTTP handler functions, and keeping things as lean as we can.

First, let's start in a new folder by creating the initial application `scoreboard.go`, which will handle the main logic and allow adding new scores and retrieving them from the API:

```golang
package main

import (
	"cmp"
	"encoding/json"
	"log"
	"net/http"
	"slices"
)

type Score struct {
	Name  string `json:"name"`
	Value uint32 `json:"score"`
}

func main() {
	scores := make([]Score, 0)

	http.HandleFunc("/score", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "POST" {
			var s Score

			err := json.NewDecoder(r.Body).Decode(&s)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}
			scores = append(scores, s)
			slices.SortFunc(scores, func(a, b Score) int {
				return cmp.Compare(a.Value, b.Value) * -1
			})
			w.WriteHeader(http.StatusCreated)
			return
		}
		if r.Method == "GET" {
			w.Header().Add("Content-Type", "application/json")
			json.NewEncoder(w).Encode(scores)
			return
		}
		http.Error(w, "Not found", http.StatusNotFound)
	})

	log.Println("Listening on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

```

At this point, if we run the app it will start an HTTP server on port 8080 and allow you to call it as follows:

```bash
curl -X POST -H 'Content-type: application/json' -d '{"name":"XYZ","score":90}' http://localhost:8080/score
curl -X POST -H 'Content-type: application/json' -d '{"name":"AAA","score":50}' http://localhost:8080/score
curl http://localhost:8080/score
```

Everything is stored in memory right now, so once the app is closed it will reset and your saved scores will be lost. We need to add some state into the app to make it more useful.

### Adding DynamoDB

To add DynamoDB to the service, we'll need to make sure it can handle its dependencies correctly. This means we'll need to initialise the modules within Go to manage these for us:

```bash
go mod init example.com/scoreboard
```

Now you'll need to add the AWS SDK dependency to communicate with DynamoDB:

```bash
go get github.com/aws/aws-sdk-go-v2/aws
go get github.com/aws/aws-sdk-go-v2/config
go get github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue
go get github.com/aws/aws-sdk-go-v2/service/dynamodb
go get github.com/aws/aws-sdk-go-v2/service/dynamodb/types
```

To add the DynamoDB logic to our system, we'll keep it within its own file called `dynamodb.go`. This will be able to connect to DynamoDB either within a local Docker container or with AWS, and should be able to read and write scores into the table:

```golang
package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/feature/dynamodb/attributevalue"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
)

const tableName string = "scoreboard"

func createClient(endpoint string) *dynamodb.Client {
	cfg, err := config.LoadDefaultConfig(context.TODO(), func(o *config.LoadOptions) error {
		o.Region = "us-east-1"
		return nil
	})
	if err != nil {
		panic(err)
	}
	if endpoint == "" {
		endpoint = "https://dynamodb.us-east-1.amazonaws.com"
	}

	return dynamodb.NewFromConfig(cfg, func(o *dynamodb.Options) {
		o.BaseEndpoint = &endpoint
	})
}

func createTable(c *dynamodb.Client) error {
	_, err := c.CreateTable(context.TODO(), &dynamodb.CreateTableInput{
		TableName:   aws.String(tableName),
		BillingMode: types.BillingModePayPerRequest,
		AttributeDefinitions: []types.AttributeDefinition{
			{
				AttributeName: aws.String("name"),
				AttributeType: types.ScalarAttributeTypeS,
			},
		},
		KeySchema: []types.KeySchemaElement{
			{
				AttributeName: aws.String("name"),
				KeyType:       types.KeyTypeHash,
			},
		},
	})

	return err
}

func save(c *dynamodb.Client, name string, value uint32) error {
	_, err := c.PutItem(context.TODO(), &dynamodb.PutItemInput{
		TableName: aws.String(tableName),
		Item: map[string]types.AttributeValue{
			"name":  &types.AttributeValueMemberS{Value: name},
			"value": &types.AttributeValueMemberN{Value: fmt.Sprint(value)},
		},
	})

	return err
}

func get(c *dynamodb.Client) []Score {
	out, err := c.Scan(context.TODO(), &dynamodb.ScanInput{
		TableName: aws.String(tableName),
	})
	if err != nil {
		panic(err)
	}

	var result []Score
	attributevalue.UnmarshalListOfMaps(out.Items, &result)

	return result
}
```

Now that the operations are supported, there will need to be some changes in the main scoreboard file to accommodate this.

First, replace line 17:

```golang
--- scores := make([]Score, 0)
+++ dynamodb := createClient("")
```

Now update the save logic for 30:

```golang
--- scores = append(scores, s)
--- slices.SortFunc(scores, func(a, b Score) int {
---     return cmp.Compare(a.Value, b.Value) * -1
--- })
+++ err = save(dynamodb, s.Name, s.Value); if err != nil {
+++     http.Error(w, err.Error(), http.StatusInternalServerError)
+++	    return
+++ }
```

And finally, update the get logic on line 39:

```golang
--- json.NewEncoder(w).Encode(scores)
+++ scores := get(dynamodb)
+++ slices.SortFunc(scores, func(a, b Score) int {
+++     return cmp.Compare(a.Value, b.Value) * -1
+++ })
+++ json.NewEncoder(w).Encode(scores)
```

There are two ways that this will work: either using a local DynamoDB instance, or connecting to Amazon. Before we get into that, let's setup some tests to make sure this is working as expected using Test Containers first of all.

### Testing with DynamoDB

Create a new file for testing, `dynamodb_test.go` and add the following to it - this will setup the TestContainers when needed, create a new table within DynamoDB for using while testing, and check that the get and save functionality is working as expected:

```golang
package main

import (
	"context"
	"testing"

	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	containers "github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/wait"
)

// Create the test container and wait for it to be ready
func setupContainer(t *testing.T) (string, func(t *testing.T)) {
	ctx := context.Background()
	req := containers.ContainerRequest{
		Image:        "amazon/dynamodb-local:latest",
		ExposedPorts: []string{"8000/tcp"},
		WaitingFor:   wait.ForExposedPort(),
	}
	container, err := containers.GenericContainer(ctx, containers.GenericContainerRequest{
		ContainerRequest: req,
		Started:          true,
	})
	if err != nil {
		t.Fatalf("Could not start DynamoDB: %s", err)
	}
	endpoint, err := container.Endpoint(ctx, "")
	if err != nil {
		t.Fatalf("Could not get DynamoDB endpoint: %s", err)
	}

	return endpoint, func(t *testing.T) {
		if err := container.Terminate(ctx); err != nil {
			t.Fatalf("Could not stop DynamoDB: %s", err)
		}
	}
}

func connect(e string, t *testing.T) *dynamodb.Client {
	client := createClient("http://" + e)
	if err := createTable(client); err != nil {
		t.Errorf("Expected to be able to create DynamoDB table, but received: %s", err)
	}

	return client
}

func fill(c *dynamodb.Client, t *testing.T) {
	if err := save(c, "foo", 90); err != nil {
		t.Errorf("Expected to be able to put item into DynamoDB, but received: %s", err)
	}
	if err := save(c, "bar", 75); err != nil {
		t.Errorf("Expected to be able to put item into DynamoDB, but received: %s", err)
	}
	if err := save(c, "baz", 80); err != nil {
		t.Errorf("Expected to be able to put item into DynamoDB, but received: %s", err)
	}
}

func TestConnect(t *testing.T) {
	ep, tearDown := setupContainer(t)
	defer tearDown(t)

	connect(ep, t)
}

func TestSave(t *testing.T) {
	ep, tearDown := setupContainer(t)
	defer tearDown(t)
	c := connect(ep, t)

	if err := save(c, "testing", 50); err != nil {
		t.Errorf("Expected to be able to save item, but received error: %s", err)
	}
}

func TestGet(t *testing.T) {
	ep, tearDown := setupContainer(t)
	defer tearDown(t)
	c := connect(ep, t)
	fill(c, t)

	result := get(c)
	if result[0].Name != "foo" {
		t.Errorf("Expected entry 0 to be 'foo' but received: %s", result[0].Name)
	}
	if result[0].Value != 90 {
		t.Errorf("Expected entry 0 to be '90' but received: %d", result[0].Value)
	}
	if result[1].Name != "baz" {
		t.Errorf("Expected entry 1 to be 'baz' but received: %s", result[1].Name)
	}
	if result[1].Value != 80 {
		t.Errorf("Expected entry 1 to be '80' but received: %d", result[1].Value)
	}
	if result[2].Name != "bar" {
		t.Errorf("Expected entry 2 to be 'bar' but received: %s", result[2].Name)
	}
	if result[2].Value != 75 {
		t.Errorf("Expected entry 2 to be '75' but received: %d", result[2].Value)
	}
}
```

You'll also need to run:

```bash
go get github.com/testcontainers/testcontainers-go
```

What does this file do?

- The first function creates the test container - it loads an Amazon DynamoDB image and waits for it to be ready, then returns the endpoint so it can be connected to further down. It also creates a teardown function so we can safely close the container after we've finished our tests.
- The second function connects to the container and creates a table ready for us to use.
- The third function fills in some test data within the container, using our DynamoDB library file so we can test the get functionality.

From then on, the tests are pretty straight-forward.

Now, to initiate the tests you can run:

```bash
go test -v
```

This will show the containers spinning up and down, and the result of each test as it completes. You'll find that the connect and save tests are successful, but there seems to be something wrong with the get test:

```
--- FAIL: TestGet (3.72s)
    dynamodb_test.go:85: Expected entry 0 to be 'foo' but received: baz
    dynamodb_test.go:88: Expected entry 0 to be '90' but received: 80
    dynamodb_test.go:91: Expected entry 1 to be 'baz' but received: bar
    dynamodb_test.go:94: Expected entry 1 to be '80' but received: 75
    dynamodb_test.go:97: Expected entry 2 to be 'bar' but received: foo
    dynamodb_test.go:100: Expected entry 2 to be '75' but received: 90
```

The entries aren't appearing in the order they're inserted - DynamoDB doesn't guarantee sort order on a scan, and we're running into that. We have the sorting within our main scoreboard.go file, so maybe we should move it to be part of the DynamoDB logic instead.

First, add the following to `dynamodb.go` around line 77, before the function returns:

```golang
	slices.SortFunc(result, func(a, b Score) int {
		return cmp.Compare(a.Value, b.Value) * -1
	})
```

Now we can remove the same lines (41-43) from `scoreboard.go`.

Now, try the tests again - they should pass!

### Running Locally

To run the whole app locally, you'll need to run the docker image for DynamoDB in the background, and then pass the endpoint into the application to load it. For that, we need to make one more change to the DynamoDB file to accept an environment variable as configuration.

In `scoreboard.go`, change line 17 as follows:

```golang
--- dynamodb := createClient("")
+++ dynamodb := createClient(os.Getenv("DYNAMODB_ENDPOINT"))
```

Now, starting the DynamoDB container, creating the table and launching the scoreboard is possible by running the following:

```bash
docker run --rm -d --name dynamodb -p 8000:8000 amazon/dynamodb-local:latest
aws dynamodb --endpoint http://localhost:8000 create-table --table-name scoreboard --attribute-definitions 'AttributeName=name,AttributeType=S' --key-schema 'AttributeName=name,KeyType=HASH' --billing-mode PAY_PER_REQUEST
DYNAMODB_ENDPOINT=http://localhost:8000 go run dynamodb.go scoreboard.go
```

Now the cURL requests you made previously should work again:

```bash
curl -X POST -H 'Content-type: application/json' -d '{"name":"XYZ","score":90}' http://localhost:8080/score
curl -X POST -H 'Content-type: application/json' -d '{"name":"AAA","score":50}' http://localhost:8080/score
curl http://localhost:8080/score
```

Tip: if you run into any `ResourceNotFound` exceptions, you may need to change the region in your `dynamodb.go` file to match your default configuration if you're not using us-east-1.

### Deploying with AWS

Deploying this with AWS goes a little beyond the scope of the current article, maybe that's something for another time?

There are some things you could think about if you wanted to try this yourself, however:

- You could create all this in the console, but using Terraform or AWS CDK would be better
- The scoreboard code could be very easily packaged as a Lambda and run without much cost
- Deploying a DynamoDB table manually would be very similar to what we've done here locally
- You'd need to make the table name an environment variable in the same way the endpoint is, as "scoreboard" will have already been used by someone else

For reference, all the code used today is available in GitHub at the following gist: [https://gist.github.com/jamiefdhurst/6fc5990c588f89520f136ffc1c3ccbe5](https://gist.github.com/jamiefdhurst/6fc5990c588f89520f136ffc1c3ccbe5).

Any questions or comments, reach me on [Mastodon](https://howdee.social/@jamiefdhurst) or find me through my [GitHub profile](https://github.com/jamiefdhurst).
