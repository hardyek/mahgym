from setuptools import setup, find_packages

setup(
    name="mahgym",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "mahgym": ["tiles/*.png"],
    },
    install_requires=[
        "pygame",
        # other dependencies
    ],
)