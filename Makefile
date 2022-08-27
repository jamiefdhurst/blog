PWD := $(shell echo `pwd`)
DOCKER_MAIN := docker run -v $(PWD):/app -e GITHUB_USERNAME=$(GITHUB_USERNAME) -e GITHUB_TOKEN=$(GITHUB_TOKEN)
DOCKER_IMAGE := --name blog -i blog
DOCKER_TEST = blog-test
DOCKER_TEST_IMAGE := --name blog-test -i $(DOCKER_TEST)

## build: build the container image for the blog
build :
	@docker build -t blog .
	@docker build -t blog-test -f Dockerfile.test .

test-background :
	@docker ps | grep blog-test || $(DOCKER_MAIN) -d $(DOCKER_TEST_IMAGE) tail -f /dev/null
	@echo "Container running in background as 'blog-test'..."

test-clean :
	@docker stop $(DOCKER_TEST) || true
	@docker rm $(DOCKER_TEST) || true

test : test-background
	@docker exec $(DOCKER_TEST) coverage run -m pytest --verbose

test-with-reports : test
	@docker exec $(DOCKER_TEST) coverage run -m pytest --verbose --junit-xml tests.xml
	@docker exec $(DOCKER_TEST) coverage xml -o coverage.xml

run :
	@$(DOCKER_MAIN) -p 5000:5000 $(DOCKER_IMAGE)

clean : test-clean
	@docker stop blog || true
	@docker rm blog || true

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command to run:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo