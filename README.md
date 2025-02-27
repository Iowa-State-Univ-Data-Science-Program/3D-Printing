# Iowa State DS - 3D Printing

This repository is meant to provide a series of python scripts and utilities to assist 
in the creation of mathematically defined 3d surfaces in a printable format(STL).


## Usage
1. create a virtual environment with venv
2. install the python libs:
```
# execute from source root
pip install -r requirements.txt
```
3. Edit main.py(not required) and execute


## Notes

### Implementation order of operations
1. define bounds

2. define top surface
3. triangulate top surface
4. render top surface

5. write mesh to disk

6. define bottom surface 
7. triangulate bottom surface
8. render bottom surface

9. generate sidewalls
10. combine surfaces 
11. generate mesh

12. Unit Tests

### Libraries
- scipy
- numpy
- openstl

- pymeshlab
