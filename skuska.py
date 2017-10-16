#dic_moznosti = {'A':None,'B':None,'C':None,'D':None,'E':None,'F':None,'G':None,'H':None}
list_moznosti = ['A','B','C','D','E','F','G','H']
dic_akomx = {'akoma':None,'akomb':None,'akomc':None,'akomd':None,'akome':None,'akomf':None,'akomg':None,'akomh':None}
dic_zadanx = {'zadana':None,'zadanb':None,'zadanc':None,'zadand':None,'zadane':None,'zadanf':None,'zadang':None,'zadanh':None}

for x in range(8):
    zadane = request.form.get(list_moznosti[x])
    if zadane:
        moja.append(list_moznosti[x].lower())



lst = str(otazkyzdatabazy['od']).split(',')
print(lst)
maxbodovzaodpoved = len(lst)
mojbodovzaodpoved = 0

for x in range(8):
    if list_moznosti[x].lower in moja:
        dic_zadanx['zadan'+list_moznosti[x].lower] = 'zakliknute'
    else:
        dic_zadanx['zadan'+list_moznosti[x].lower] = 'nezakliknute'
    if list_moznosti[x].lower in lst and list_moznosti[x].lower in moja:
        print(list_moznosti[x] 'si zadal tak ako malo byt')
        mojbodovzaodpoved += 1
        dic_akomx['akom'+list_moznosti[x].lower] = 'spravne'
    elif list_moznosti[x].lower not in moja and list_moznosti[x].lower not in lst:
        dic_akomx['akom'+list_moznosti[x].lower] = 'neutralne'
    else:
        dic_akomx['akom'+list_moznosti[x].lower] = 'zle'

'''
    print(dic_moznosti[list_moznosti[x]])
    dic_moznosti[list_moznosti[x]] = 'nieco'
    print(dic_moznosti[list_moznosti[x]])
print(dic_moznosti)
'''
'''
    A = request.form.get('A')
    if A:
        moja.append('a')
    B = request.form.get('B')
    if B:
        moja.append('b')
    C = request.form.get('C')
    if C:
        moja.append('c')
    D = request.form.get('D')
    if D:
        moja.append('d')
    E = request.form.get('E')
    if E:
        moja.append('e')
    F = request.form.get('F')
    if F:
        moja.append('f')
    G = request.form.get('G')
    if G:
        moja.append('g')
    H = request.form.get('H')
    if H:
        moja.append('h')




lst = str(otazkyzdatabazy['od']).split(',')
print(lst)
maxbodovzaodpoved = len(lst)
mojbodovzaodpoved = 0

if 'a' in moja:
    zadana = 'zakliknute'
else:
    zadana = 'nezakliknute'
if 'a' in lst and 'a' in moja:
    print('A si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akoma = 'spravne'
elif 'a' not in moja and 'a' not in lst:
    akoma = 'neutralne'
else:
    akoma = 'zle'

if 'b' in moja:
    zadanb = 'zakliknute'
else:
    zadanb = 'nezakliknute'
if 'b' in lst and 'b' in moja:
    print('B si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomb = 'spravne'
elif 'b' not in moja and 'b' not in lst:
    akomb = 'neutralne'
else:
    akomb = 'zle'

if 'c' in moja:
    zadanc = 'zakliknute'
else:
    zadanc = 'nezakliknute'
if 'c' in lst and 'c' in moja:
    print('C si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomc = 'spravne'
elif 'c' not in moja and 'c' not in lst:
    akomc = 'neutralne'
else:
    akomc = 'zle'

if 'd' in moja:
    zadand = 'zakliknute'
else:
    zadand = 'nezakliknute'
if 'd' in lst and 'd' in moja:
    print('D si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomd = 'spravne'
elif 'd' not in moja and 'd' not in lst:
    akomd = 'neutralne'
else:
    akomd = 'zle'

if 'e' in moja:
    zadane = 'zakliknute'
else:
    zadane = 'nezakliknute'
if 'e' in lst and 'e' in moja:
    print('E si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akome = 'spravne'
elif 'e' not in moja and 'e' not in lst:
    akome = 'neutralne'
else:
    akome = 'zle'

if 'f' in moja:
    zadanf = 'zakliknute'
else:
    zadanf = 'nezakliknute'
if 'f' in lst and 'f' in moja:
    print('F si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomf = 'spravne'
elif 'f' not in moja and 'f' not in lst:
    akomf = 'neutralne'
else:
    akomf = 'zle'

if 'g' in moja:
    zadang = 'zakliknute'
else:
    zadang = 'nezakliknute'
if 'g' in lst and 'g' in moja:
    print('G si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomg = 'spravne'
elif 'g' not in moja and 'g' not in lst:
    akomg = 'neutralne'
else:
    akomg = 'zle'

if 'h' in moja:
    zadanh = 'zakliknute'
else:
    zadanh = 'nezakliknute'
if 'h' in lst and 'h' in moja:
    print('H si zadal tak ako malo byt')
    mojbodovzaodpoved += 1
    akomh = 'spravne'
elif 'h' not in moja and 'h' not in lst:
    akomh = 'neutralne'
else:
    akomh = 'zle'
'''