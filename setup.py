from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

with open("README.md", "r") as f:
    long_description = f.read()

extensions = [
    #Extension('tsynth.string_z3_conversion', ['tsynth/string_z3_conversion.pyx'])
]

setup(
    name="tsynth",
    version="0.1",
    author="Thomas Steeples",
    author_email="steeps@robots.ox.ac.uk",
    description="An enumerative solver for SyGuS problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasfsteeples/tsynth/",

    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize(
        extensions, 
        annotate = True,
        language_level=3
    ),

    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)