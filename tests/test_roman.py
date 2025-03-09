from roman import expression_to_arabic


class TestRoman:
    # Тесты на сложение
    def test_simple1(self):
        assert expression_to_arabic("10+20+30") == "10+20+30"

    def test_simple2(self):
        assert expression_to_arabic("1+2+X+3") == "1+2+10+3"

    def test_simple3(self):
        assert expression_to_arabic("1+2*IV-20") == "1+2*4-20"

    def test_simple4(self):
        assert expression_to_arabic("I/LXXX+4*VII-CD") == "1/80+4*7-400"

    def test_simple5(self):
        assert expression_to_arabic("II*VIII*(III+2)/80") == "2*8*(3+2)/80"
