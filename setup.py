from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in shanti_education/__init__.py
from shanti_education import __version__ as version

setup(
	name="shanti_education",
	version=version,
	description="EDUCATION",
	author="FINBYZ TECH PVT LTD",
	author_email="info@finbyz.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
