import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DummyRDM",
    version="0.0.1",
    author="Dave McCulloch",
    author_email="dave@d5systems.co.uk",
    description="A Dummy RDM Test suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfivesystems/DummyRDM/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)