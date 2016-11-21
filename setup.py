
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


if sys.argv[-1] == 'prep':
    os.system('python setup.py sdist')
    sys.exit()


JAR_FILE_PATH = os.path.join('java', 'AgentUID.jar')

setup(
    name='iceburg',
    version=__import__('iceburg').__version__,
    description='Recovery tools to the Experience Upgrade Recovery project.',
    long_description=__doc__,
    author='Nathan Lucas',
    author_email='bnlucas@outlook.com',
    url='https://github.com/bnlucas/iceburg',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'requests_cache',
        'six',
    ],
    license='MIT',
    zip_safe=False,
)
