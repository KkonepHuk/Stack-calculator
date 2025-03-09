def roman_to_int(s):
        res = 0
        dictionary = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        for i in range(1, len(s)):
            if dictionary[s[i - 1]] < dictionary[s[i]]:
                res -= dictionary[s[i - 1]]
            else:
                res += dictionary[s[i - 1]]
        res += dictionary[s[-1]]
        return res


def expression_to_arabic(string):
    string+= ' '
    roman = 'IVXLCDM'
    to_int = ''
    result = ''
    for i in range(len(string)):
        if string[i] in roman and string[i + 1] in roman:
            to_int += string[i]
        elif string[i] in roman and not(string[i + 1] in roman):
            to_int += string[i]
            new_int = roman_to_int(to_int)
            result += str(new_int)
            to_int = ''
        else:
            result += string[i]

    return result[:-1]

if __name__ == '__main__':
    print(expression_to_arabic('10+20+30'))
    print(expression_to_arabic('1+2+X+3'))
    print(expression_to_arabic('1+2*IV-20'))
    print(expression_to_arabic('I/LXXX+4*VII-CD'))