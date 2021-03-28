from setuptools import find_packages, setup

'''
    packages tells Python what package directories (and the Python files they contain) to include. 
    find_packages() finds these directories automatically so you don’t have to type them out. 
    To include other files, such as the static and templates directories, include_package_data is set. 
'''

setup(
    name='webapp',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
