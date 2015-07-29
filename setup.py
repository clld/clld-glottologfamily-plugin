from setuptools import setup, find_packages


requires = [
    'clld>=1.2.1',
    'clldclient>=0.6',
]

tests_require = [
    'mock==1.0',
]

setup(
    name='clld-glottologfamily-plugin',
    version='1.0',
    description='clld-glottologfamily-plugin',
    classifiers=[
        "Programming Language :: Python",
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
