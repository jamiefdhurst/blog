# Blog

My blog website - generated from Jinja templates and markdown articles as a 
static site.

## Development

You will require Python 3. Run the following to install required modules:

```bash
python3 -m pip install -r requirements.txt
```

You can then generate the site using:

```bash
python3 -m blog.generate
```

To run a local Docker instance of Nginx to serve a generated set of files, run:

```bash
docker run --rm -d --name blog -v $(pwd)/docker/nginx.conf:/etc/nginx/nginx.conf:ro -v $(pwd)/dist:/usr/share/nginx/html -p 8080:80 nginx
```

You can then run the when-changed package to automatically generate the blog files anytime a change is made:

```bash
when-changed -r -1 articles blog -c python3 -m blog.generate
```

*(You must be using a virtual environment or your
Python bin files must be on your path for this to work.)*

Then head to http://localhost:8080 to view the results.

You can stop the docker container with `docker stop blog`.

## Testing

Testing uses Pytest - run it as follows (installing the required modules too):

```bash
pytest --verbose
```

## Build and Release

The GitHub Actions pipeline handles testing, building and releasing the static 
site version. Upon the main branch being updated, a new version of the blog will
be automatically released to GitHub and the new version will be immediately 
deployed to the live website. The same pipeline can be used to deploy other 
versions if required.
