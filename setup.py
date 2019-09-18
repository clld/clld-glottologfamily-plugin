from setuptools import setup, find_packages

setup(
    name='clld-glottologfamily-plugin',
    version='3.1.0',
    description='clld-glottologfamily-plugin',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='https://github.com/clld/clld-glottologfamily-plugin',
    keywords='web pyramid pylons',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld>=3.3.3',
        'sqlalchemy',
        'zope.interface',
        'pyglottolog>=2.0',
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine'],
        'test': [
            'pytest>=3.6',
            'pytest-mock',
            'pytest-clld',
            'mock',
            'coverage>=4.2',
            'pytest-cov',
            'webtest',
        ],
    },
    license="Apache 2.0",
)
