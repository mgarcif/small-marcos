#$Id$

from euclidean_domain import gcd
import functools

@functools.total_ordering
class Rational(object):
    """
    Class to represent rationals: numerator/denominator.
    * denominator > 0
    * numerator and denominator do not have common divisors.
    * if numerator is 0, then denominator is 1
    """
    def __init__(self, num=0, den=1):
        """
        Builds a rational
        @type num: integer
        @type den: integer
        @raise Exception: if den==0
        """
        self.numerator = num
        self.denominator = den
        self.reduce()

    def reduce(self):
        """
        This function reduce this rational into a equivalent simplified one.
        @raise Exception: if self.denominator==0
        """
        if self.denominator==0:
            raise Exception('The denominator of a rational cannot be zero')

        if self.denominator<0:
            self.denominator=-self.denominator
            self.numerator=-self.numerator

        if self.numerator!=0:
            d = gcd(abs(self.numerator), abs(self.denominator))
            self.numerator = self.numerator // d
            self.denominator = self.denominator // d
        else:
            self.denominator=1

    def __repr__(self):
        """
        Function to transform the rational into a string.
        See the special mehtods in python:
        http://docs.python.org/reference/datamodel.html#special-method-names
        """
        if self.denominator==1:
            return str(self.numerator)
        else:
            return str(self.numerator)+"/"+str(self.denominator)

    def __add__(self, other):
        """
        Sum this rational to other
        @type other: Rational
        @rtype: Rational
        """
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            return NotImplemented


        d = gcd(abs(self.denominator), abs(other.denominator))
        lcm = (abs(self.denominator) * abs(other.denominator)) // d
        s = Rational(self.numerator*lcm // self.denominator+
                     other.numerator*lcm // other.denominator
                     ,lcm)

        return s

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        """
        This function computes the opposite rational.
        @rtype: Rational
        """
        return Rational(-self.numerator, self.denominator)

    def __sub__(self,other):
        """
        This function performs the substraction between rationals.
        @tpye other: Rational
        @rtype: Rational
        """
        return self + (-other)

    def __mul__(self,other):
        """
        This function performs the mutltiplicationa between rationals
        @type other: Rational
        @rtype: Rational
        """
        if isinstance(other, int):
            other = Rational(other, 1)
        elif not isinstance(other, Rational):
            return NotImplemented

        return Rational(self.numerator*other.numerator,
                        self.denominator*other.denominator)

    def __rmul__(self, other):
        return self.__mul__(other)

    def inv(self):
        """
        This function computes the inverse (if exists) if the rational
        @rtype: Rational
        @raise Exception: if this rational is zero.
        """
        return Rational(self.denominator,self.numerator)

    def __truediv__(self, other):
        """
        This function performs the divistion between rationals
        @type other: Rational
        @rtype: Rational
        @raise Exception: if the other rational is zero
        """
        return self * other.inv()

    def __pow__(self, other):
        """Computes the integer power
        @type other:int
        """
        if isinstance(other, int):
            return Rational(self.numerator**other, self.denominator**other)
        else:
            return NotImplemented

    def cmp_rational(self,other):
        d = self - other
        return d.numerator
    def cmp_integer(self,other):
        d = self - Rational(other)
        return d.numerator
    def cmp_float(self,other):
        f = float(self.numerator) - other * self.denominator
        return f

    def __lt__(self, other):
        if isinstance(other,Rational):
            return self.cmp_rational(other)<0
        elif isinstance(other,int):
            return self.cmp_integer(other)<0
        elif isinstance(other,float):
            return self.cmp_float(other)<0
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other,Rational):
            return self.cmp_rational(other)==0
        elif isinstance(other,int):
            return self.cmp_integer(other)==0
        elif isinstance(other,float):
            return self.cmp_float(other)==0
        else:
            return NotImplemented

    def to_float(self):
        return self.numerator / self.denominator


    @staticmethod
    def parse(s):
        """
        This static function builds a rational from a string. The
        rational can have the folowing forms:
          - <integer>
          - <integer>/<integer>
        @raise Exception: This function can raise an exception
           - There is no number at all
           - if the second integer is zero
        @type s: string
        @rtype rational
        """
        l=s.strip().split("/")
        num=int(l[0].strip())
        if len(l)>1:
            den=int(l[1].strip())
        else:
            den=1
        return Rational(num,den)


ZERO = Rational(0)
ONE = Rational(1,1)

def test_init():
    a = Rational(2, 4)
    assert a.numerator == 1 and a.denominator==2

    a = Rational(30,60)
    assert a.numerator == 1 and a.denominator==2

    a = Rational(31,-23)
    assert a.numerator == -31 and a.denominator == 23

    a = Rational(-31, 23)
    assert a.numerator == -31 and a.denominator == 23

    print('OK init')

def test_parse():
    a = Rational.parse("2/4")
    assert a.numerator == 1 and a.denominator==2

    a = Rational.parse("30/60")
    assert a.numerator == 1 and a.denominator==2

    a = Rational.parse("31/-23")
    assert a.numerator == -31 and a.denominator == 23

    a = Rational.parse("-31/23")
    assert a.numerator == -31 and a.denominator == 23

    print('OK parse')

def test_eq():
    a = Rational.parse("2/4")
    assert a == Rational(1,2)

    a = Rational.parse("30/60")
    assert a == Rational(1,2)

    a = Rational.parse("31/-23")
    assert a == Rational(-31,23)

    a = Rational.parse("-31/23")
    assert a == Rational(-31,23)

    print('OK eq')


def test_add():
    a = Rational.parse("2/4")
    b = Rational.parse("30/60")
    assert a + b == Rational(1,1)
    assert a + 2 == Rational(5,2)
    assert 2 + a == Rational(5,2)

    print('ok add')

def test_mul():
    a = Rational.parse("2/4")
    b = Rational.parse("30/60")
    assert a * b == Rational(1,4)
    assert a * 2 == Rational(1,1)
    assert 2 * a == Rational(1,1)

    print('ok mul')

def test_lt():
    a = Rational.parse("2/4")
    b = Rational.parse("30/61")
    assert b<a

    print('ok lt')
