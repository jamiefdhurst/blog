from setuptools import find_packages, setup

setup(
    name='blog',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'jinja2',
        'markdown',
    ],
)
