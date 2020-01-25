import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imported",
    version="0.0.1",
    author="Brian Larsen",
    author_email="bmelarsen+imported@gmail.com",
    description="Simple function to list imported modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brl0/imported",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
