# Iowa State DS - 3D Printing

This repository is meant to provide a series of python scripts and utilities to assist 
in the creation of mathematically defined 3d surfaces in a printable format(STL).


## math_surfaces
A package to generate 3D printable mathematical surfaces using numpy/scipy
Please see `scripts/basic_normal.py` for a simple example.

> ![NOTE]
> `scripts/basic_normal.py` uses a relative import since the 
> package is not currently published on pypi. If you copy the script to your own project,
> make sure to change the import to match the installation instructions below.

### Installation From Source

1. Clone the git repository
```bash
git clone --depth 1 https://github.com/Iowa-State-Univ-Data-Science-Program/3D-Printing.git math-surfaces
```
1. Activate your python environment(venv, conda, etc)
1. Install the Package
```
pip install .
```
1. Import in your code
```python
from math_surfaces import *
```

### Development
This project uses [uv](https://docs.astral.sh/uv/) for dependency and build management. 
If you wish to build a distributable tarball run `uv build` in the repo root:

```bash
uv build
```
All UV features including venv management and publishing to pypi(not yet implemented) should work.

> [!IMPORTANT]
> REMEMBER to increment the version number in `pyproject.toml` after making changes.
> pip uses the `project.version` parameter to decide whether or not to update a package.
