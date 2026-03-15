from setuptools import setup, find_packages

setup(
    name="rpyc_client",
    version="0.1",
    author="Ori",
    packages=find_packages(),
    install_requires=["pytest", "pandas"],
)
