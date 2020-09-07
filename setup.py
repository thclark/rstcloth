from setuptools import find_packages, setup


# Note:
#   The Hitchiker's guide to python provides an excellent, standard, method for creating python packages:
#       http://docs.python-guide.org/en/latest/writing/structure/
#
#   To deploy on PYPI follow the instructions at the bottom of:
#       https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi

with open("README.md") as f:
    readme_text = f.read()

with open("LICENSE") as f:
    license_text = f.read()

setup(
    name="rstcloth",
    version="0.3.0",
    py_modules=[],
    url="https://www.github.com/thclark/rstcloth",
    license="MIT",
    author="thclark",
    description="A simple Python API for generating RestructuredText.",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=["sphinx>=2,<4", "pygments", "PyYAML"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["rstable = rstcloth.table:main"]},
    python_requires=">=3.6",
    keywords=["sphinx", "rst", "restructuredtext", "documentation", "rest", "docutils"],
)
