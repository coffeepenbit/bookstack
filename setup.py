from setuptools import setup, find_packages
import os

CLASSIFIERS = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]
EXTRAS_REQUIRE = {
    'dev': [
        'bump2version',
        'pylint',
        'pytest',
        'pytest-cov',
        'pytest-vcr',
        'tox'
    ]
}
INSTALL_REQUIRES = [
    'requests>= 2.18, < 3',
    'cached_property >= 1.5, < 2',
    'inflection == 0.4'
]


def get_about(here):
    about = {}
    about_info_path = os.path.join(here, 'src', 'bookstack', '__version__.py')
    with open(about_info_path,'r', encoding='utf-8' ) as f:
        exec(f.read(), about)

    return about

def get_long_description(here):
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    return long_description


here = os.path.abspath(os.path.dirname(__file__))
about = get_about(here)

setup(
    name=about['__title__'],
    version=about['__version__'],
    url=about['__url__'],
    description=about['__description__'],
    long_description=get_long_description(here),
    author=about['__author__'],
    author_email=about['__author_email__'],
    long_description_content_type='text/markdown',
    packages=find_packages('src'),    
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=CLASSIFIERS
)