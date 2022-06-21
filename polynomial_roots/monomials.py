from rationals import Rational
from functools import total_ordering

@total_ordering
class Monomial(object):
    """
    This class represents a monomial: coef * x^degree
    * coef will be a rational number
    * degree>=0 an integer
    * if coef==0, then degree==0
    """
    def __init__(self, coef=Rational(num=0), degree=0):
        self.coef=coef
        self.degree=degree
        if self.coef == 0:
            self.degree = 0

    def __add__(self,other):
        if self.coef == 0:
            return Monomial(other.coef, other.degree)
        if other.degree!=self.degree:
            raise Exception("I can only sum monomials with the same degree")
        return Monomial(self.coef + other.coef, self.degree)

    def __mul__(self,other):
        return Monomial(self.coef * other.coef, self.degree+other.degree)

    def __lt__(self, other):
        return (self.degree < other.degree) or \
            (self.degree == other.degree and self.coef < other.coef)

    def __eq__(self, other):
        return self.degree == other.degree and self.coef == other.coef


    def __repr__(self):
        s=str(self.coef)
        if self.degree>0:
            s+=f"·x^{self.degree}"
        return s

    def __truediv__(self,other):
        if other.coef==Rational(0):
            raise Exception("The divisor monomial cannot be zero")
        if other.degree>self.degree:
            raise Exception("The degree of the divisor monomial cannot be greater than the dividend monomial")
        return Monomial(self.coef/other.coef, self.degree-other.degree)

    @staticmethod
    def parse(s):
        """
        This static method parses a string that should contain a monomial
        of one of the following forms:
          - <rational> * x^<integer>
          - <rational>
        @type s: string
        @rtype: Monomial
        @raise Exception: if the string is not as described above
        """
        l = s.strip().split("·")
        coef = Rational.parse(l[0].strip())
        if len(l)==1:
            exp=0
        else:
            l[1] = l[1].strip()
            if len(l[1]) == 1:
                exp = 1
            else:
                exp = int(l[1].strip()[2:])
        return Monomial(coef,exp)

def test_parse():
    m = Monomial.parse("1·x")
    assert m.coef == Rational(1,1) and m.degree == 1
    m = Monomial.parse("1/2·x")
    assert m.coef == Rational(1,2) and m.degree == 1
    m = Monomial.parse("2·x")
    assert m.coef == Rational(2) and m.degree == 1
    m = Monomial.parse("1/2·x^2")
    assert m.coef == Rational(1, 2) and m.degree == 2
    print('OK. parse')

def test_equal():
    m1 = Monomial.parse("0·x^5")
    m2 = Monomial.parse("0·x^3")
    assert m1 == m2 and m2 == m1

    m1 = Monomial.parse("2·x^5")
    m2 = Monomial.parse("4/2·x^5")
    assert m1 == m2 and m2 == m1

    m1 = Monomial.parse("2·x^5")
    m2 = Monomial.parse("1/4·x^5")
    assert not m1 == m2  and not m2 == m1
    print('OK')

def test_sum_monomial():
    m1 = Monomial.parse("3/13·x^5")
    m2 = Monomial.parse("12/13·x^5")
    m3 = m1 + m2
    assert m3 == Monomial.parse("15/13·x^5")


    m1 = Monomial.parse("3/13·x^5")
    m2 = Monomial.parse("12/13·x^2")
    try:
        m3 = m1 + m2
        assert False, "You are adding {m1} and {m2}, which is not possible"
    except AssertionError as e:
        raise(e)
    except Exception as e:
        print(f'He capturado la excepcion {e}')


def test_prod_monomial():
    m1 = Monomial.parse("2/3·x^5")
    m2 = Monomial.parse("3/5·x^3")
    m3 = m1 * m2
    assert m3 == Monomial.parse("2/5·x^8")

    m1 = Monomial.parse("0·x^5")
    m2 = Monomial.parse("12/13·x^2")
    m3 = m1 * m2
    assert m3 == Monomial.parse("0·x^0")

    print('OK')


def test_div():
    m1 = Monomial(Rational(1,2), 2)
    m2 = Monomial.parse("3/13·x^5")
    m3 = m2 / m1
    print(m3)
    assert m3 == Monomial.parse("6/13·x^3")

def pr_set_mon():
    m1 = Monomial(Rational(1,2), 2)
    m2 = Monomial.parse("3/13·x^5")
    m3 = m2 / m1
    a = {m1, m2, m3}
