import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygame_geometry",
    version="0.1.2",
    author="Mazex",
    author_email="marc.partensky@gmail.com",
    description="Geometry environment for pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcPartensky/Pygame-Geometry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)