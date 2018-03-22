# Orca Gadgets
Scripts that helps me deal with files related to ORCA 4.0 . Mainly for **NMR/EPR calculation**.

## BasisMethodTester.py

Intended for testing a variety of Basis sets and Method on a specific molecule. It should be used with a input file model with only Basis set and Method Keywords uncompleted. An additional blank line should be prepared. Example:

```
! TightSCF opt finalgrid5 NMR Grid4 RIJK
! PAL2
				#This line is blanked for the script

* xyz 0 1
Cl      -2.6710000000      0.0000000000     -0.0002000000                 
C       -0.9497000000      0.0001000000      0.0002000000                 
C       -0.2523000000      1.2080000000      0.0000000000                 
C       -0.2523000000     -1.2079000000      0.0000000000                 
C        1.1426000000      1.2079000000      0.0000000000                 
C        1.1426000000     -1.2080000000      0.0000000000                 
C        1.8401000000      0.0000000000      0.0000000000                 
H       -0.7824000000      2.1570000000      0.0000000000                 
H       -0.7825000000     -2.1569000000     -0.0001000000                 
H        1.6859000000      2.1484000000     -0.0001000000                 
H        1.6858000000     -2.1485000000     -0.0002000000                 
H        2.9262000000      0.0000000000     -0.0001000000                 
*
```

Then modify the directories in the script. Hints are provided in the script. If you understand how ORCA works and have a basic knowledge of Python3, it should not be difficult. Here I assume that the model file and final output files are stored in ./ and calculations are done in ./calc . Anyway, full paths are always recommended! 

Correct ORCA keywords are demanded for the function and basis sets list.

## OutAnalyzer.py

Collect atom coordinates from input file presented in output file and final result. Then match the **chemical shift** with the corresponding atom and save as a csv file.

These scripts are for **ORCA Windows version**. For **Linux version**, replace
```python
for i in range(len(text_array)):
        if 'xyz' in text_array[i]:
            for j in range(i+2, len(text_array), 2):
                cor = getCor(text_array[j], index)
                if cor == 'end':
                    break
                res.append(cor)
                index += 1
```
with
```python
for i in range(len(text_array)):
        if 'xyz' in text_array[i]:
            for j in range(i+2, len(text_array)):
                cor = getCor(text_array[j], index)
                if cor == 'end':
                    break
                res.append(cor)
                index += 1
```
ORCA Windows version insertes an additional line between original lines of input file in output file.

## Dependency

- Orca 4.0 for Windows