from blog.images import add_image_attributes, get_dimensions

IMG = '<img alt="Placeholder" src="/static/placeholder.png" />'


def test_get_dimensions():
    assert get_dimensions('/static/placeholder.png') is not None


def test_get_dimensions_missing_file():
    assert get_dimensions('/static/does-not-exist.png') is None


def test_get_dimensions_is_cached():
    first = get_dimensions('/static/placeholder.png')
    assert first == get_dimensions('/static/placeholder.png')


def test_add_image_attributes_adds_dimensions():
    result = add_image_attributes(IMG)
    width, height = get_dimensions('/static/placeholder.png')
    assert f'width="{width}" height="{height}"' in result


def test_add_image_attributes_lazy_by_default():
    result = add_image_attributes(IMG)
    assert 'loading="lazy"' in result
    assert 'decoding="async"' in result


def test_add_image_attributes_eager_when_not_lazy():
    result = add_image_attributes(IMG, False)
    assert 'loading="eager"' in result
    assert 'fetchpriority="high"' in result
    assert 'loading="lazy"' not in result


def test_add_image_attributes_keeps_existing_attributes():
    result = add_image_attributes('<img alt="A" src="/static/placeholder.png" loading="eager" />')
    assert result.count('loading=') == 1
    assert 'loading="eager"' in result


def test_add_image_attributes_without_dimensions():
    result = add_image_attributes('<img alt="A" src="/static/does-not-exist.png" />')
    assert 'width=' not in result
    assert 'loading="lazy"' in result


def test_add_image_attributes_ignores_img_without_src():
    original = '<img alt="A" />'
    assert original == add_image_attributes(original)


def test_add_image_attributes_handles_empty_content():
    assert add_image_attributes('') == ''
    assert add_image_attributes(None) is None


def test_add_image_attributes_leaves_other_markup_alone():
    result = add_image_attributes('<p>Text</p>' + IMG + '<p>More</p>')
    assert '<p>Text</p>' in result
    assert '<p>More</p>' in result


def test_add_image_attributes_handles_multiple_images():
    result = add_image_attributes(IMG + IMG)
    assert result.count('loading="lazy"') == 2
