from setuptools import setup, find_packages


requires = [
    'html5lib == 0.999999',
    'clld>=1.4.1',
    'clldclient>=1.0.1',
]

tests_require = [
    'mock==1.0',
]

setup(
    name='clld-glottologfamily-plugin',
    version='1.2',
    description='clld-glottologfamily-plugin',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Robert Forkel',
    author_email='xrotwang@googlemail.com',
    url='https://github.com/clld/clld-glottologfamily-plugin',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    test_suite="clld_glottologfamily_plugin",
    entry_points="""\
    """)
