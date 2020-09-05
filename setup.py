import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcrawl",
    version="0.0.2",
    author="Dongsheng Deng",
    author_email="ddswhu@outlook.com",
    description="dcrawl package to crawl data from web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dd-datascience/dcrawl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
