from setuptools import setup, find_packages

setup(
    name='jmbo-show',
    version='0.3.2',
    description='Jmbo show app.',
    long_description=open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-show',
    packages=find_packages(),
    install_requires=[
        'jmbo-calendar>=0.2.5',
        'django-ckeditor>=4.0.2',
        'jmbo-foundry>=1.2',
    ],
    tests_require=[
        'django-setuptest>=0.1.4',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
