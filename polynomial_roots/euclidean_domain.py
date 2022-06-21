def gcd(a,b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def test_gcd():
    assert gcd(273,27) == 3
    assert gcd(2**3 * 5**2 * 7**1, 3**1 * 5**4 * 7**2) == 5**2 * 7**1
    print('OK gcd')
