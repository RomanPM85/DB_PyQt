from setuptools import setup, find_packages

setup(name="mess_app_mrp_server",
      version="0.0.1",
      description="The Server part of the messenger in Python",
      author="Roman Mamchiy",
      author_email="mamchiy@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )
