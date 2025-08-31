from dataclasses import dataclass


@dataclass(slots=True)
class DegreeMinuteSecond:
    seconds: int

    def __post_init__(self):
        if not isinstance(self.seconds, int):
            raise TypeError(f"seconds must be int, got {type(self.seconds).__name__}")

    @property
    def sign(self):
        return (self.seconds > 0) - (self.seconds < 0)

    @property
    def degree(self):
        return abs(self.seconds) // 3600

    @property
    def minute(self):
        return (abs(self.seconds) // 60) % 60

    @property
    def second(self):
        return (abs(self.seconds) % 3600) % 60

    def __add__(self, other):
        return DegreeMinuteSecond(self.seconds + other.seconds)

    def __sub__(self, other):
        return DegreeMinuteSecond(self.seconds - other.seconds)

    def __str__(self):
        sign = {1: "+", 0: "", -1: "-"}[self.sign]
        return f"{sign}{self.degree}°{self.minute}'{self.second:02d}''"

    def __rmul__(self, other):
        return DegreeMinuteSecond(self.seconds * other)

    def __truediv__(self, other):
        if not isinstance(other, int):
            raise TypeError("Only integer division supported")
        return DegreeMinuteSecond(self.seconds // other)

    @classmethod
    def angle(cls, degree: int, minute: int, second: int):
        return cls(degree * 3600 + minute * 60 + second)

    def astype(self, dtype):
        if dtype == float:
            return self.seconds / 3600
        else:
            raise TypeError(f"Cannot convert {type(self)} to {dtype}")


def degree(angle: float) -> DegreeMinuteSecond:
    """Construct a DegreeMinuteSecond from a float representation of angle in degrees"""
    return DegreeMinuteSecond(int(angle * 3600))



# tests
def test_main():
    assert DegreeMinuteSecond.angle(183, 59, 47) + DegreeMinuteSecond.angle(-6, -59, -47) == DegreeMinuteSecond.angle(177, 0, 0)
    assert DegreeMinuteSecond.angle(183, 59, 47) - DegreeMinuteSecond.angle(-6, -59, -47) == DegreeMinuteSecond.angle(190, 59, 34)


def test_minus_given_overflow_second():
    assert DegreeMinuteSecond.angle(0, 1, 0) - DegreeMinuteSecond.angle(0, 0, 1) == DegreeMinuteSecond.angle(0, 0, 59)

def test_sub_given_overflow_minute():
    assert DegreeMinuteSecond.angle(1, 0, 0) - DegreeMinuteSecond.angle(0, 1, 0) == DegreeMinuteSecond.angle(0, 59, 0)


def test_add_given_overflow_second():
    assert DegreeMinuteSecond.angle(0, 0, 59) + DegreeMinuteSecond.angle(0, 0, 2) == DegreeMinuteSecond.angle(0, 1, 1)


def test_add_given_overflow_minute():
    assert DegreeMinuteSecond.angle(0, 60, 0) + DegreeMinuteSecond.angle(0, 1, 0) == DegreeMinuteSecond.angle(1, 1, 0)


def test_normalise():
    assert DegreeMinuteSecond.angle(-173, -59, -47) == DegreeMinuteSecond.angle(-174, 0, 13)


def test_scalar_multiply():
    assert 2 * DegreeMinuteSecond.angle(0, 0, 30) == DegreeMinuteSecond.angle(0, 1, 0)
    assert 3 * DegreeMinuteSecond.angle(0, 0, 30) == DegreeMinuteSecond.angle(0, 1, 30)


def test_scalar_divide():
    assert DegreeMinuteSecond.angle(0, 1, 0) / 2 == DegreeMinuteSecond.angle(0, 0, 30)


def test_astype_given_float():
    assert DegreeMinuteSecond.angle(1, 1, 1).astype(float) == 1 + (1 / 60) + (1 / 3600)


def test_constructor():
    import pytest

    assert degree(1) == DegreeMinuteSecond(3600)
    assert degree(1.5) == DegreeMinuteSecond(5400)
    assert degree(2) == DegreeMinuteSecond(7200)

    with pytest.raises(TypeError):
        DegreeMinuteSecond(1.0)


def test_sign():
    assert degree(0).sign == 0
    assert degree(-0).sign == 0


def test_str():
    assert str(degree(0)) == "0°0'00''"
    assert str(degree(61 / 3600)) == "+0°1'01''"
    assert str(degree(61 / 60)) == "+1°1'00''"
    assert str(degree(123.456)) == "+123°27'21''"
