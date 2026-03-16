from setuptools import setup, find_packages

setup(
    name="bacon_distance",
    version="0.1",
    author="Ori",
    packages=find_packages(),
    install_requires=["pytest", "pandas", "fastapi[standard]"],
)
