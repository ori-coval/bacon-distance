from setuptools import setup, find_packages

setup(
    name="bacon_distance_frontend",
    version="0.1",
    author="Ori",
    packages=find_packages(),
    install_requires=["pytest", "fastapi[standard]"],
)
