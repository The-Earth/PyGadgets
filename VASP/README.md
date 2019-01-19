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
outob.getcs(out='cs.csv') # write chemical shift to cs.csv
# or
outob.getcs() # just return chemical shift
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

It will read `OUTCAR` in working directory. If `OUTCAR` is renamed or moved:
```python
inob = INCAR(filename='OUTCAR1')
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

## Demos

- `cetensor.py` is a demo for getting chemical shift.
- `utest.py`: Do not use.

## Critical problem

The first line of  `POSCAR` , which represents name of this task, should be in form of:

```
li6 o2 cl3
```

Its sequence should be the same as that of atom coordinates and the number equals to number of atoms of that element. **I won't fix this problem**.