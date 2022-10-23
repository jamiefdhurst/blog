from flask import (
    abort, Blueprint, current_app, render_template, request
)

from . import articles

bp = Blueprint('blog', __name__)

@bp.route('/', methods=['GET'])
def index():
    directory = current_app.config['ARTICLES_DIR']
    current_page = int(request.args.get('page') or 1)
    parsed_articles = articles.get_paginated_articles(directory, current_page)
    pages = articles.get_pages(directory)

    return render_template(
        'index.html',
        articles=parsed_articles,
        current_page=current_page,
        pages=[None] * pages,
    )

@bp.route('/now', methods=['GET'])
def now():
    return render_template(
        'now.html',
    )

@bp.route('/<slug>', methods=['GET'])
def view(slug):
    directory = current_app.config['ARTICLES_DIR']
    try:
        article = articles.get_article(directory, slug)
    except articles.ArticleException:
        abort(404)
    return render_template(
        'view.html',
        article=article,
    )
