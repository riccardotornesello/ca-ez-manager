import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ca_manager",
    version="0.0.1",
    author="Riccardo Tornesello",
    description="CLI tool to simply manage Certification Authorities using the shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    py_modules=["ca_manager"],
    install_requires=[
        "cryptography==42.0.5",
        "inquirerpy==0.3.4",
        "rich==13.7.1",
        "typer==0.12.1",
    ],
    entry_points={"console_scripts": ["ca-manager = ca_manager.__main__:main"]},
)
