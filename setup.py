from setuptools import setup

setup(
    name='friendly_fenced_tabs',
    version='0.0.9',
    url='https://github.com/andru255/friendly_fenced_tabs',
    packages=['friendly_fenced_tabs', 'friendly_fenced_tabs/utils'],
    install_requires=[
        'markdown>=2.6'
    ],
    include_package_data=True,
    description='Generates a html estructure for handling tabbed content',
    author='Andres Munoz',
    author_email='andru255@gmail.com',
    license='MIT',
    keywords=['fenced code blocks', 'code', 'fenced', 'tabs', 'mkdocs', 'markdown'],
    platform='Operating System :: OS Independent',
    long_description=""" Markdown extension who generates HTML tabs by fenced code block markdown syntax """,
    zip_safe=False,
    classifiers=[
        'Intented Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Text processing',
    ]
    
)