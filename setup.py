from setuptools import setup, find_packages

setup(
    name='EasySaveService',  
    version='0.2.0', 
    packages=find_packages(), 
    install_requires=[ 
        'requests',
        'enum',
        'os'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='David Comor',
    author_email='david.comor@gmail.com',
    description='EasySave service python library',
    url='https://github.com/DavComo/EasySaveModule',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
