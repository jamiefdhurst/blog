#!/usr/bin/env python3
'''Fail the build if an article does not follow the expected structure.

The generator finds the title, hero image and summary by position - the
first h1, the first image, the first h2 - so an article written slightly
differently renders wrongly rather than failing loudly. This checks the
convention at pull request time instead.

Expected shape:

    # Title

    ![Alt text](/static/image.jpg)

    ## Summary sentence shown on the index and used as the meta description

    Body...

Later `##` headings are fine; only the first is treated as the summary.
'''
import os
import re
import sys

ARTICLES_DIR = 'articles'
STATIC_ROOT = 'blog'
FILENAME = re.compile(r'^\d{4}-\d{2}-\d{2}_[a-z0-9._-]+\.md$')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
MIN_SUMMARY = 40


def content_lines(text):
    '''Lines with fenced code blocks blanked out, so examples inside code
    samples are not mistaken for real headings or images'''
    lines, fenced = [], False
    for line in text.split('\n'):
        if line.strip().startswith('```'):
            fenced = not fenced
            lines.append('')
            continue
        lines.append('' if fenced else line)
    return lines


def check(name, lines):
    problems = []
    body = [line for line in lines if line.strip()]

    if not body or not body[0].startswith('# '):
        problems.append('must start with a "# Title" heading')
        return problems

    if len([line for line in lines if line.startswith('# ')]) != 1:
        problems.append('must have exactly one "# " title')

    if len(body) < 2 or not body[1].lstrip().startswith('!['):
        problems.append('needs a hero image directly after the title')
        return problems

    alt, src = IMAGE.search(body[1]).groups()
    if not alt.strip():
        problems.append('hero image needs alt text')
    if src.startswith('/static/') and not os.path.exists(STATIC_ROOT + src):
        problems.append(f'hero image {src} does not exist')

    if len(body) < 3 or not body[2].startswith('## '):
        problems.append('needs a "## " summary directly after the hero image')
        return problems

    summary = body[2][3:].strip()
    if len(summary) < MIN_SUMMARY:
        problems.append(f'summary is only {len(summary)} characters, '
                        f'expected at least {MIN_SUMMARY}')

    # The summary is rendered above the body, so repeating it anywhere in the
    # body shows the same text twice - and it is not always the opening
    # paragraph that repeats it.
    for index, line in enumerate(body[3:], start=1):
        paragraph = line.strip()
        if paragraph.startswith(('#', '!', '|', '>', '-', '*')):
            continue
        where = 'opening paragraph' if index == 1 else f'paragraph {index}'
        if paragraph == summary:
            problems.append(f'{where} repeats the summary word for word')
        elif len(paragraph) > MIN_SUMMARY and (
                summary.startswith(paragraph) or paragraph.startswith(summary)):
            problems.append(f'{where} largely repeats the summary')

    for alt, src in IMAGE.findall('\n'.join(lines)):
        if not alt.strip():
            problems.append(f'image {src} has no alt text')
        if src.startswith('/static/') and not os.path.exists(STATIC_ROOT + src):
            problems.append(f'image {src} does not exist')

    return problems


def main():
    failures = {}
    names = sorted(name for name in os.listdir(ARTICLES_DIR) if name.endswith('.md'))

    for name in names:
        problems = []
        if not FILENAME.match(name):
            problems.append('filename must be YYYY-MM-DD_slug.md')
        with open(os.path.join(ARTICLES_DIR, name), encoding='UTF-8') as handle:
            problems.extend(check(name, content_lines(handle.read())))
        if problems:
            failures[name] = problems

    print(f'Checked {len(names)} articles')

    if failures:
        print(f'\n{len(failures)} article(s) need attention:\n')
        for name, problems in failures.items():
            print(f'  {name}')
            for problem in problems:
                print(f'    ✗ {problem}')
        print('\nSee the expected structure in .github/scripts/validate-articles.py')
        return 1

    print('All articles follow the expected structure')
    return 0


if __name__ == '__main__':
    sys.exit(main())
