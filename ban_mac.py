'''
dic = {'0xac220bc6287a': 1529357571.7602956,
       '0xac220bc6287b': 1529357575.7602956,
       '0xac220bc6287c': 1529357579.7602956}
'''


def test():
    dic = {'0xac220bc6287a': 1,
           '0xac220bc6287b': 5,
           '0xac220bc6287c': 9}

    list_mac = []
    list_time = []

    for mac, time in dic.items():
        list_mac.append(mac)
        list_time.append(time)

    myvar = 4.1

    counter = 0

    for x in range(len(list_time) - 1):
        basic = list_time[x]
        for y in range(x + 1, len(list_time)):
            advanced = list_time[y]
            print('-' * 20)
            print(basic,
                  advanced,
                  advanced - myvar,
                  advanced + myvar)
            if basic > advanced - myvar and basic < advanced + myvar:
                print("hacker")
                counter += 1
    print('-' * 20)
    assert counter > 0


test()
