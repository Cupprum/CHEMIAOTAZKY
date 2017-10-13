moja = ['a','b','c']
lst = ['a','b','c']
dic = {'a':0}

def __init__(pismeno):
        if pismeno in moja:
            zadan+pismeno = 'zakliknute'
        else:
            'zadan'+pismeno = 'nezakliknute'
        if pismeno in lst and pismeno in moja:
            print('A si zadal tak ako malo byt')
            mojbodovzaodpoved += 1
            str('akom'+pismeno) = 'spravne'
        elif pismeno not in moja and pismeno not in lst:
            str('akom'+pismeno) = 'neutralne'
        else:
            str('akom'+pismeno) = 'zle'

print(__init___('a'))