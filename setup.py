from setuptools import setup, find_packages

setup(
    name="algorithms",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "setuptools~=68.2.0",
        "networkx~=3.4.2",
        "numpy~=2.2.4",
        "scikit-learn~=1.6.1",
        "scipy~=1.15.2",
        "librosa~=0.11.0",
        "matplotlib~=3.10.1",
        "pandas~=2.2.3",
        "PyWavelets~=1.8.0",
        "pillow~=11.2.1"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="An interactive algorithm visualization tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/algorithm-visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
