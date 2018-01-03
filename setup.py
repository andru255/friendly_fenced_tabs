from setuptools import setup, find_packages

setup(
    name='friendly_fenced_tabs',
    version='0.0.9',
    url='https://github.com/andru255/friendly_fenced_tabs',
    py_modules=['friendly_fenced_tabs'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_dir= {'friendly_fenced_tabs.lib': 'lib'},
    install_requires=[
        'markdown>=2.6'
    ],
    description='Generates a html estructure for handling tabbed content',
    author='Andres Munoz',
    author_email='andru255@gmail.com',
    license='MIT',
    keywords=['fenced code blocks', 'code', 'fenced', 'tabs', 'mkdocs', 'markdown'],
    platform='Operating System :: OS Independent',
    long_description=""" Markdown extension who generates HTML tabs by fenced code block markdown syntax """,
    classifiers=[
        'Intented Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Text processing',
    ]
    
)