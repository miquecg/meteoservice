from setuptools import setup


setup(
    name='meteoservice',
    version='0.1.0',
    author='Miguel Casal',
    url='https://github.com/miquecg/meteoservice',
    packages=['meteoservice'],
    package_dir={'': 'src'},
    extras_require={
        'test': [
            'coverage',
            'flexmock',
            'py',
            'pytest',
            'pytest-cov',
            'wsgi-intercept'
        ]
    })
