from dataclasses import dataclass

@dataclass
class DegreeMinuteSecond:
    degree: int
    minute: int
    second: int

    def __add__(self, other):
        return DegreeMinuteSecond.from_seconds(self.seconds + other.seconds)

    def __sub__(self, other):
        return DegreeMinuteSecond.from_seconds(self.seconds - other.seconds)

    def __str__(self):
        return f"{self.degree}°{self.minute}'{self.second:02d}"

    def __rmul__(self, other):
        return DegreeMinuteSecond.from_seconds(self.seconds * other)

    @property
    def normalise(self):
        return DegreeMinuteSecond.from_seconds(self.seconds)

    def __truediv__(self, other):
        return DegreeMinuteSecond.from_seconds(self.seconds / other)

    @classmethod
    def from_seconds(cls, seconds: int):
        degree = seconds // 3600
        minute = (seconds - degree * 3600) // 60
        second = seconds - degree * 3600 - minute * 60
        return cls(degree, minute, second)

    @property
    def seconds(self):
        return self.degree * 3600 + self.minute * 60 + self.second


# tests
def test_main():
    assert DegreeMinuteSecond(183, 59, 47) + DegreeMinuteSecond(-6, -59, -47) == DegreeMinuteSecond(177, 0, 0)
    assert DegreeMinuteSecond(183, 59, 47) - DegreeMinuteSecond(-6, -59, -47) == DegreeMinuteSecond(190, 59, 34)


def test_minus_given_overflow_second():
    assert DegreeMinuteSecond(0, 1, 0) - DegreeMinuteSecond(0, 0, 1) == DegreeMinuteSecond(0, 0, 59)

def test_sub_given_overflow_minute():
    assert DegreeMinuteSecond(1, 0, 0) - DegreeMinuteSecond(0, 1, 0) == DegreeMinuteSecond(0, 59, 0)


def test_add_given_overflow_second():
    assert DegreeMinuteSecond(0, 0, 59) + DegreeMinuteSecond(0, 0, 2) == DegreeMinuteSecond(0, 1, 1)


def test_add_given_overflow_minute():
    assert DegreeMinuteSecond(0, 60, 0) + DegreeMinuteSecond(0, 1, 0) == DegreeMinuteSecond(1, 1, 0)


def test_normalise():
    assert DegreeMinuteSecond(-173, -59, -47).normalise == DegreeMinuteSecond(-174, 0, 13)


def test_scalar_multiply():
    assert 2 * DegreeMinuteSecond(0, 0, 30) == DegreeMinuteSecond(0, 1, 0)
    assert 3 * DegreeMinuteSecond(0, 0, 30) == DegreeMinuteSecond(0, 1, 30)


def test_scalar_divide():
    assert DegreeMinuteSecond(0, 1, 0) / 2 == DegreeMinuteSecond(0, 0, 30)
