# Blog

My blog website - built using Flask in Python. A standalone web app that 
requires no separate database and is powered through Markdown articles.

## Development

You will require Python 3. Run the following to install required modules:

```bash
python3 setup.py develop
```

You can then launch the project using:

```bash
FLASK_APP=blog flask run
```

## Testing

Testing uses Pytest - run it as follows:

```bash
pytest --verbose
```

## Build and Release

The Jenkins pipeline handles build and release. Upon the main branch being 
updated, a new version of the blog will eb automatically released to GitHub and 
the new version will be immediately deployed to the live website. The same 
pipeline can be used to deploy other versions if required.

## Makefile

A Makefile has been added for convenience to run certain commands:

* `build` - build the Docker images (standard and test)
* `test` - run the tests after launching the test container
* `test-with-reports` - run the tests and output the required reports
* `run` - launch the blog container listening on port 5000
* `clean` - shut down and clean all running containers
