from dataclasses import dataclass

@dataclass
class DegreeMinuteSecond:
    degree: int
    minute: int
    second: int

    def __add__(self, other):
        second = (self.second + other.second) % 60
        minute = (self.minute + other.minute + int(second / 60)) % 60
        degree = self.degree + other.degree + int(minute / 60)
        return DegreeMinuteSecond(degree, minute, second)

    def __sub__(self, other):
        second = self.second - other.second
        minute = self.minute - other.minute
        degree = self.degree - other.degree
        return DegreeMinuteSecond(degree, minute, second)

    def __str__(self):
        return f"{self.degree}°{self.minute}'{self.second:02d}"

# tests
def test_main():
    assert DegreeMinuteSecond(183, 59, 47) + DegreeMinuteSecond(-6, -59, -47) == DegreeMinuteSecond(177, 0, 0)
    assert DegreeMinuteSecond(183, 59, 47) - DegreeMinuteSecond(-6, -59, -47) == DegreeMinuteSecond(189, 118, 94)


def test_minus_given_overflow_second():
    assert DegreeMinuteSecond(0, 1, 0) - DegreeMinuteSecond(0, 0, 1) == DegreeMinuteSecond(0, 0, 59)

