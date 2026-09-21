# ICAO Doc 9303 Machine Readable Travel Documents Reference

## 1. Character Weighting & Values
Characters permitted in an ICAO Doc 9303 MRZ are restricted to uppercase Latin `A-Z`, digits `0-9`, and the filler character `<`.

```
0: 0    A: 10   K: 20   U: 30
1: 1    B: 11   L: 21   V: 31
2: 2    C: 12   M: 22   W: 32
3: 3    D: 13   N: 23   X: 33
4: 4    E: 14   O: 24   Y: 34
5: 5    F: 15   P: 25   Z: 35
6: 6    G: 16   Q: 26   <: 0
7: 7    H: 17   R: 27
8: 8    I: 18   S: 28
9: 9    J: 19   T: 29
```

Weights repeat in cycles of 3: `7, 3, 1, 7, 3, 1, ...`.

---

## 2. TD3 Format (Standard Passport, 2 lines x 44 characters)

### Line 1 (Positions 1-44):
- `1-2`: Document Code (e.g. `P<`)
- `3-5`: Issuing State or Organization (3-letter ISO 3166-1 alpha-3 code)
- `6-44`: Name (Surname followed by `<<`, then Given Names separated by `<`)

### Line 2 (Positions 1-44):
- `1-9`: Document Number (9 chars)
- `10`: Document Number Check Digit (1 char)
- `11-13`: Nationality of Holder (3-letter code)
- `14-19`: Date of Birth (`YYMMDD`)
- `20`: Date of Birth Check Digit (1 char)
- `21`: Sex (`M`, `F`, or `<`)
- `22-27`: Expiry Date (`YYMMDD`)
- `28`: Expiry Date Check Digit (1 char)
- `29-42`: Personal Number or Optional Data (14 chars)
- `43`: Optional Data Check Digit (or `<` if unused)
- `44`: **Composite Check Digit** over positions 1-10, 14-20, 22-43.

---

## 3. TD1 Format (ID Card, 3 lines x 30 characters)

### Line 1 (Positions 1-30):
- `1-2`: Document Code (e.g. `I<`, `ID`)
- `3-5`: Issuing State (3-letter code)
- `6-14`: Document Number (9 chars)
- `15`: Document Number Check Digit (1 char)
- `16-30`: Optional Data Elements (15 chars)

### Line 2 (Positions 1-30):
- `1-6`: Date of Birth (`YYMMDD`)
- `7`: Date of Birth Check Digit (1 char)
- `8`: Sex (`M`, `F`, or `<`)
- `9-14`: Expiry Date (`YYMMDD`)
- `15`: Expiry Date Check Digit (1 char)
- `16-18`: Nationality (3-letter code)
- `19-29`: Optional Data Elements (11 chars)
- `30`: **Composite Check Digit** over Line 1 (6-30), Line 2 (1-7), Line 2 (9-15), Line 2 (19-29).

### Line 3 (Positions 1-30):
- `1-30`: Primary Identifier (Surname) followed by `<<`, then Secondary Identifier (Given Names).
