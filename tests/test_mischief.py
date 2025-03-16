from mischief import Mischief

class TestMischief:
    
    # Инициализация 
    def setup_method(self):
        self.m = Mischief()

    def test_simple1(self):
        assert self.m.compile("c+a+b") == "a b + c +"
    
    def test_simple2(self):
        assert self.m.compile("c*a*b") == "a b * c *"
    
    def test_simple3(self):
        assert self.m.compile("c-a-b") == "c a - b -"
    
    def test_simple4(self):
        assert self.m.compile("c/a/b") == "c a / b /"

    def test_simple5(self):
        assert self.m.compile("e+d/v+b+a") == "a d v / + b + e +"

    def test_simple6(self):
        assert self.m.compile("(d+e+f+b+a)+(t+c+v+m+n+p+o)") == "a b + c + d + e + f m + n + o + p + t + v + +"
    
    def test_simple7(self):
        assert self.m.compile("(d+e+f+b+a)+(t*c*v*m*n*p*o)") == "a b + d + e + f + c m * n * o * p * t * v * +"