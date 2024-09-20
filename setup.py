from setuptools import setup
import sys

install_requires = ['ldap3']

if sys.platform.startswith('linux'):
    install_requires.append('pyasn1-modules')

setup(
    name='ldap-sync-service',
    version='4.1.0',
    py_modules=['ldap_sync_service'],
    install_requires=install_requires,
    dependency_links=[
        'https://github.com/alexsilva/django-ldap-sync.git@master'
    ],
    url='https://github.com/alexsilva/django-ldap-sync-service',
    license='MIT',
    author='alex',
    author_email='',
    description='Service used in django ldap sync command.',
)
