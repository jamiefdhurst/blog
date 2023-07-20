from flask import (
    abort, Blueprint, current_app, make_response, render_template, request, send_from_directory
)

from . import articles

bp = Blueprint('blog', __name__)

@bp.route('/favicon.ico')
@bp.route('/humans.txt')
@bp.route('/robots.txt')
def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])

@bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    directory = current_app.config['ARTICLES_DIR']
    parsed_articles = articles.get_all_articles(directory)

    template = render_template(
        'sitemap.xml',
        articles=parsed_articles,
    )
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response

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
