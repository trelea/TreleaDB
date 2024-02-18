from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="treleadb",
    version="0.0.1",
    author="Trelea Marius",
    author_email="treleamarius76@gmail.com",
    description="TreleaDB object database for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["cryptography"],
    url="https://github.com/trelea/TreleaDB",
    keywords=["python", "python3", "database", "nodql", "mongodb", "treleadb", "object", "json"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System:: OS Independent",
    ]
)