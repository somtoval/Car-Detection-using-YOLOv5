# from setuptools import find_packages, setup

# setup(
#     name="Car Detector",
#     version="0.0.1",
#     author="Somto",
#     author_email="ogbesomto4@gmail.com",
#     packages=find_packages(),
#     install_requires=[],
# )


# This code specifies that src is the folder where the packages will be found
from setuptools import find_packages, setup

setup(
    name="Car_Detector",  # Name of the package
    version="0.0.1",       # Version of the package
    author="Somto Ogbe",   # Your name
    author_email="ogbesomto4@gmail.com",  # Your email
    description="A Car Detector",  # A brief description of your package
    # long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Specify the content type of the long description
    packages=find_packages(where='src'),  # Automatically find packages in the 'src' directory
    package_dir={'': 'src'},  # Set 'src' as the root for the packages
    install_requires=[],
    classifiers=[  # Optional: Add some classifiers to describe your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
)