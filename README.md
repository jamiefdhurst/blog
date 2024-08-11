# Blog

My blog website - generated from Jinja templates and markdown articles as a 
static site.

## Development

You will require Python 3. Run the following to install required modules:

```bash
python3 setup.py develop
```

You can then generate the site using:

```bash
python3 -m blog.generate
```

To run a local Docker instance of Nginx to serve a generated set of files, run:

```bash
docker run --rm --name blog -v $(pwd)/docker/nginx.conf:/etc/nginx/nginx.conf:ro -v $(pwd)/dist:/usr/share/nginx/html -p 8080:80 nginx
```

Then head to http://localhost:8080 to view the results.

## Testing

Testing uses Pytest - run it as follows:

```bash
pytest --verbose
```

## Build and Release

The GitHub Actions pipeline handles testing, building and releasing the static 
site version. Upon the main branch being updated, a new version of the blog will
be automatically released to GitHub and the new version will be immediately 
deployed to the live website. The same pipeline can be used to deploy other 
versions if required.
