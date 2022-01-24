import datetime
import math
from os import listdir
from os.path import isfile, join
import re
from flask import current_app
from markdown import markdown

class Article:
    def __init__(self, directory, filename):
        self.find_image = re.compile(r'<p>(<img.+>)</p>')
        self.find_summary = re.compile(r'<h2>(.+)</h2>')
        self.find_title = re.compile(r'<h1>(.+)</h1>')

        self.filename = filename
        try:
            with open(directory + filename, encoding='UTF8') as file:
                self.contents = markdown(file.read(), extensions=['fenced_code'])
        except FileNotFoundError as fnfe:
            raise ArticleNotFoundException(f"Could not find article file {filename}") from fnfe

    def get_contents(self):
        return self.contents

    def get_content_only(self):
        title = self.find_title.search(self.contents)
        summary = self.find_summary.search(self.contents)
        contents = self.contents.replace(title.group(0), '')    
        if summary:
            return contents.replace(summary.group(0), '')
        return contents

    def get_date(self):
        '''Expects datetime to be in beginning of file name'''
        find_date = re.compile(r'^(\d{4}-\d{2}-\d{2})_')
        date = find_date.match(self.filename)
        if not date:
            raise InvalidDateForArticleException(f"Could not parse date for article {self.filename}")
        return datetime.datetime.strptime(date.group(1), '%Y-%m-%d')

    def get_image(self):
        image = self.find_image.search(self.contents)
        if not image:
            return None
        return image.group(1)

    def get_name(self):
        return self.filename[:-3]

    def get_summary(self):
        summary = self.find_summary.search(self.contents)
        if not summary:
            return None
        return summary.group(1)

    def get_title(self):
        title = self.find_title.search(self.contents)
        if not title:
            raise InvalidTitleForArticleException(f"Could not parse title for article {self.filename}")
        return title.group(1)


def __parse_articles(directory, files):
    parsed = []
    for file in files:
        article = Article(directory, file)
        parsed.append(article)
    return parsed


def get_article(directory, file):
    return Article(directory, file + '.md')


def get_paginated_articles(directory, page=1, per_page=10):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    files.sort()
    files.reverse()
    current_app.logger.debug(f"Returned {len(files)} files...")
    first_entry = (page - 1) * per_page
    last_entry = first_entry + per_page
    files = files[first_entry:last_entry]
    return __parse_articles(directory, files)


def get_pages(directory, per_page=10):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return math.ceil(len(files) / per_page)

class ArticleException(Exception):
    pass

class ArticleNotFoundException(ArticleException):
    pass

class InvalidTitleForArticleException(ArticleException):
    pass

class InvalidDateForArticleException(ArticleException):
    pass
