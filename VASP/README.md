# VASP

Tools to assist using [VASP](https://www.vasp.at/).

## vasptool.py
### OUCAR
Creat an `OUTCAR` object:

```python
from vasptool import OUTCAR
outob = OUTCAR()
```

It will read `OUTCAR` in working directory. If `OUTCAR` is renamed or moved:

```python
outob = OUTCAR(filename='OUTCAR1')
```

Get text of `OUTCAR` in list form:

```python
outob.text_list
```

Get `POSCAR` from `OUTCAR`:

```python
outob.poscar
```

`outob.poscar` is a list in form of:

```python
[['li','4'],['o','2']]
```

Get chemical shift:

```python
outob.getcs_tensor(out='cs.csv') # write chemical shift to cs.csv
# or
outob.getcs_tensor() # just return chemical shift
```

It will return a dictionary with chemical shift information and if `outfile` is not `None`, it will save that information is csv format.

Its return value is like:

```python
{1: 'li 2.345',
 2: 'li 2.346',
 3: 'o 16.321',
}
```

### INCAR
Creat an INCAR object:
 ```python
from vasptool import INCAR
inob = INCAR()
 ```

It will read `INCAR` in working directory. If `INCAR` is renamed or moved:
```python
inob = INCAR(filename='INCAR1')
```

Get text of `INCAR` in list form:
```python
inob.text_list
```

Set value for specific key in INCAR:
```python
inob.set_key(key, value)
```
Both key and value are `str`. This operation will change content of `inob.text_list` but will not modify the file.

Save changes to file on the disk:
```python
inob.save()
```
Save as other file:
```python
inob.save(target)
```
Write your target directory in `target`.

### POSCAR
Creat a POSCAR object:
```python
from vasptool import POSCAR
pos = POSCAR()
```
Attributions of POSCAR objects:
```
pos.elements # list elements in line 6 of POSCAR
pos.ele_num # list numbers of atoms in line 7
pos.cord_type # [C]artesian or [D]irect 
pos.len # number of lines of POSCAR (minus it by 8 equals number of atoms)
```

Get a dict of all elements and corresponding numbers of atoms:
```
pos.get_num_dict()
```
Its returns is like `{'Li'":2, 'O':4}`

Get positions of all atoms:
```
pos.get_full_pos(out='output.csv')
```
It returns a dictionary contains all the positions. If an output directory is given as showed in the example, it will save result in the file.

Get position of a specific atom:
```
pos.get_pos(ind=2)
```
It returns a tuple of coordinates of specified atom. In the example, it's the second atom.

Find which element it is of specific atom:
```
pos.get_element(ind=2)
```
It's similar to `get_pos()`. Will support get from position.

## Demos

- `cetensor.py` is a demo for getting chemical shift.
- `utest.py`: Do not use.

## Critical problem

The first line of  `POSCAR` , which represents name of this task, should be in form of:

```
li6 o2 cl3
```

Its sequence should be the same as that of atom coordinates and the number equals to number of atoms of that element. **I won't fix this problem**.