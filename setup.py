import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="usdm",
  version="0.18.2",
  author="D Iberson-Hurst",
  author_email="demo@email.com",
  description="A python package for using the CDISC TransCelerate USDM",
  long_description=long_description,
  long_description_content_type="text/markdown",
  dependencies = ['pandas', 'openpyxl', 'pydantic', 'stringcase'],
  packages=setuptools.find_packages(where="src"),
  package_dir={"": "src"},
  package_data={"usdm_excel.data": ["*.yaml, *.json"]},
  classifiers=[
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Operating System :: OS Independent"
  ],
)