from setuptools import setup


setup(
    name='itemize',
    version=open('VERSION').read().strip(),
    author='Oakland John Peters',
    author_email='oakland.peters@gmail.com',

    description='Highly-general utility functions and interfaces for dealing with itemized collections (anything with a __getitem__). These include Mappings (~dicts), and Sequences (~tuples/lists), but are more general.',
    long_description=open('README.rst').read(),
    url='http://bitbucket.org/OPeters/itemize',
    license='MIT',

    packages=['itemize'],

    classifiers=[
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Development Status :: 2 - Pre-Alpha'
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ]
)
