from distutils.core import setup

setup(
    name='ldap-sync-service',
    version='3.0',
    py_modules=['ldap_sync_service'],
    install_requires=['ldap3'],
    dependency_links=[
        'https://github.com/alexsilva/django-ldap-sync.git@master'
    ],
    url='https://github.com/alexsilva/django-ldap-sync-service',
    license='MIT',
    author='alex',
    author_email='',
    description='Service used in django ldap sync command.',
)
