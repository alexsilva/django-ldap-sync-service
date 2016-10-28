from distutils.core import setup

setup(
    name='ldap-sync-service',
    version='1.0',
    py_modules=['ldap_sync_service'],
    install_requires=['pyad'],
    dependency_links=[
        'https://github.com/alexsilva/django-ldap-sync.git@master'
    ],
    url='https://github.com/alexsilva/django-ldap-sync-service',
    license='MIT',
    author='alex',
    author_email='',
    description='Service used in django ldap sync command.',
)
