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

Jenkins pipeline handles build and release.
