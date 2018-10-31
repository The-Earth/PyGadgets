# VASP

Tools to assist using [VASP](https://www.vasp.at/).

## vasptool.py

Creat an `vasptool.OUTCAR` object:

```python
from vasptool.py import OUTCAR
outob = OUTCAR()
```

It will read `OUTCAR` in working directory. If `OUTCAR` is renamed or moved:

```python
outob = OUTCAR(filename='OUTCAR1')
```

Get text of `OUTCAR` in list form:

```python
outob.text
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

## Demos

`cetensor.py` is a demo for getting chemical shift.

## Critical problem

The first line of  `POSCAR` , which represents name of this task, should be in form of:

```
li6 o2 cl3
```

Its sequence should be the same as that of atom coordinates and the number equals to number of atoms of that element. **I won't fix this problem**.