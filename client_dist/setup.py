from setuptools import setup, find_packages

setup(name="mess_app_mrp_client",
      version="0.0.1",
      description="The Client part of the messenger in Python",
      author="Roman Mamchiy",
      author_email="mamchiy@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      )
