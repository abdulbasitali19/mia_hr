from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mia_hr/__init__.py
from mia_hr import __version__ as version

setup(
	name="mia_hr",
	version=version,
	description="hr module customization",
	author="abdul basit",
	author_email="mia.hr@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
