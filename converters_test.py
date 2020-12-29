import converters
import pytest


def coordinate_to_number_test():
    assert converters.coordinate_to_number(0, 0) == 0
    assert converters.coordinate_to_number(8, 1) == 18


def number_to_coordinate_test():
    assert converters.number_to_coordinate(0) == (0, 0)
    assert converters.number_to_coordinate(18) == (8, 1)


if __name__ == "__main__":
    coordinate_to_number_test()
    number_to_coordinate_test()
