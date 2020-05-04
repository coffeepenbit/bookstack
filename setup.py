from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'src', 'bookstack', '__init__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'requests'
]

extras_require = {
    'dev': [
        'bump2version',
        'pylint',
        'pytest',
        'pytest-cov',
        'pytest-vcr',
        'tox'
    ]
}


setup(
    name=about['__title__'],
    version=about['__version__'],
    url=about['__url__'],
    description=about['__description__'],
    long_description=long_description,
    author=about['__author__'],
    author_email=about['__author_email__'],
    long_description_content_type='text/markdown',
    packages=find_packages('src'),    
    package_dir={'': 'src'},
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)