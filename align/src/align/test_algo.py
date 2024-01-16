import pytest
from algo import fill_table,traceback


def test_fill_table():
    seq1 = "AGTACGCA"
    seq2 = "TATGC"
    indel = -2
    match = 1
    mismatch = -1

    expected_result = [
        [0, -2, -4, -6, -8, -10, -12, -14, -16],
        [-2, -1, -3, -5, -7, -9, -11, -13, -15],
        [-4, -3, 0, -2, -4, -6, -8, -10, -12],
        [-6, -5, -2, 1, -1, -3, -5, -7, -9],
        [-8, -7, -4, -1, 0, -2, -4, -6, -8],
        [-10, -9, -6, -3, -2, 2, 0, -2, -4],]

    result = fill_table(seq1, seq2, indel, match, mismatch)
    assert result == expected_result

def test_traceback():
    seq1 = "AGTACGCA"
    seq2 = "TATGC"
    M = [
        [0, -2, -4, -6, -8, -10, -12, -14, -16],
        [-2, -1, -3, -5, -7, -9, -11, -13, -15],
        [-4, -3, 0, -2, -4, -6, -8, -10, -12],
        [-6, -5, -2, 1, -1, -3, -5, -7, -9],
        [-8, -7, -4, -1, 0, -2, -4, -6, -8],
        [-10, -9, -6, -3, -2, 2, 0, -2, -4],
    ]
    indel = -2
    match = 1
    mismatch = -1

    expected_alignment1 = "AGTACGCA"
    expected_alignment2 = "TAT-GC--"

    alignment1, alignment2 = traceback(seq1, seq2, M, indel, match, mismatch)
    assert alignment1 == expected_alignment1
    assert alignment2 == expected_alignment2