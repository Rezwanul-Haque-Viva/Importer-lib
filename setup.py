from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="importer-libs-campuscom",
    version="1.0.0",
    author="Rezwanul Haque",
    author_email="rezwanul.haque@vivacomsolutions.com",
    description="common libraries used in importer for Campus.com project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rezwanul-Haque-Viva/Importer-lib.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mongoengine==0.19.1",
        "requests==2.22.0",
    ],
    dependency_links=[
        'git+ssh://git@bitbucket.org/vivacomsolution/campus-shared-models.git@v1.45.0#egg=shared-models-campuscom',
        'git+ssh://git@bitbucket.org/vivacomsolution/campus-libs.git@v1.4.0#egg=campus-libs'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
