from setuptools import setup
import rstcloth

setup(
    name='rstcloth',
    description='A simple Python API for generating RestructuredText.',
    version=rstcloth.__version__,
    author='Sam Kleinman',
    author_email='sam@tychoish.com',
    license='Apache',
    url='http://cyborginstitute.org/projects/rstcloth',
    packages=['rstcloth'],
    setup_requires=['nose'],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        ],
    entry_points={
        'console_scripts': [
            'rstable = rstcloth.table:main',
            ],
        }
    )
