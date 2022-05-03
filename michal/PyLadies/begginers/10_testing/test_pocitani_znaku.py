import pytest
import funkce
#@pytest.mark.parametrize(
#  (text, znak, index, expected),
#   [])
def test_pocitam_znaky():
    assert funkce.pocitam_znaky('aaaaabbbbbcccc', 'b', 7) == 2
    #assert pocitam_znaky()


# pocitam_znaky('aaaaabbbbbcccc', 'b', 7)