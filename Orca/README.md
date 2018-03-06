# Orca Gadgets
Scripts that helps me deal with files related to ORCA and molecules.

## OutAnalyzer.py
Collect atom coordinates from input file presented in output file and final result. Then match the result with the correct atom and save as csv file.

These scripts are for **ORCA Windows version**. For Linux version, replace
```
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
```
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
