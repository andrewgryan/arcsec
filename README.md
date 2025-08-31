# Degree, minutes and seconds

A convenient module to make working with coordinates easier.

```python
from dms import degree

angle = degree(90.5)

print(str(angle))  # 90°30'00''
print(angle.degree)  # 90
print(angle.minute)  # 30
print(angle.second)  # 0
```

## Arithmetic

Simple arithmetic to make angle calculations easier.

```python
half = angle / 2  # 45° 15'
double = 2 * angle  # 181° 0' 
double + half + degree(1 / 3600)  # 226° 15' 01'
```

## Coordinate syntax

If degrees, minutes and seconds are available as integers.

```python
from dms import coord

lat = coord(51, 13, 27)
print(str(lat + degree(1)))  # 52° 13' 27''
```

## Constructors

Convenient functions for combining units of angle together using addition/subtraction.

```python
from dms import degree, minute, second
print(degree(10) + minute(5) + second(1))  # +10°5'01''

assert degree(10) + minute(5) + second(1) == coord(10, 5, 1)
```
