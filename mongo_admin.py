from pymongo import MongoClient
import xml.etree.ElementTree as ET


client = MongoClient('mongodb://atrumoram:atrumoram1@ds159489.mlab.com:59489/heroku_847wntjv')
db = client.chemia
qtable = db.table_questions
utable = db.table_users
ltable = db.table_lists

tree = ET.parse('chemia.xml')
root = tree.getroot()


def insert_all_func():
    list_of_possibilities = ["ot",
                             "od",
                             "ma",
                             "mb",
                             "mc",
                             "md",
                             "me",
                             "mf",
                             "mg",
                             "mh"]

    counter = 1
    for x in root.findall('otazka'):
        number = x.attrib.get('number')
        if str(counter) == number:
            dic_otazka = {"possition": counter,
                          "ot": None,
                          "od": None,
                          "ma": None,
                          "mb": None,
                          "mc": None,
                          "md": None,
                          "me": None,
                          "mf": None,
                          "mg": None,
                          "mh": None}

            for y in list_of_possibilities:
                actual_possibilitie = str(x.find(y).text)
                dic_otazka[str(y)] = actual_possibilitie.strip()

            print(dic_otazka)

            qtable.insert_one(dic_otazka)
            counter += 1


def insert_list_of_categories():
    list_of_categories = ['Atóm',
                          'Sústava látok',
                          'Látky',
                          'Periodická sústava prvkov',
                          'Chemická väzba', 'Názvoslovie',
                          'Chemické veličiny',
                          'Kyseliny a zásady',
                          'Chemické reakcie',
                          'Chemická rovnováha',
                          'Komplexné zlúčeniny',
                          'Príklady']

    dic = {}
    dic.update({"name_of_list": "list_of_categories"})
    dic.update({"lst": list_of_categories})

    ltable.insert_one(dic)


def insert_categories():
    list_of_categories = ['Atóm',
                          'Sústava látok',
                          'Látky',
                          'Periodická sústava prvkov',
                          'Chemická väzba', 'Názvoslovie',
                          'Chemické veličiny',
                          'Kyseliny a zásady',
                          'Chemické reakcie',
                          'Chemická rovnováha',
                          'Komplexné zlúčeniny',
                          'Príklady']

    list_names = ['atom',
                  'sustavalatok',
                  'latky',
                  'psustava',
                  'chvazba',
                  'nazvoslovie',
                  'veliciny',
                  'kyszas',
                  'reakcie',
                  'rovnovaha',
                  'komplexy',
                  'priklady']

    atom = [1, 10, 12, 14, 15, 16, 17, 18, 18, 20, 21, 22, 23, 24, 26, 27,
            39, 51, 57, 58, 59, 60, 67, 215, 374, 383, 384, 385]

    sustavalatok = [2, 3, 5, 6, 11, 13, 53, 56, 62, 94, 95, 96, 97, 111,
                    112, 121, 124, 125, 126, 128]

    latky = [4, 7, 8, 9, 36, 40, 55, 78, 79, 105, 117, 118, 119, 120, 143,
             144, 145, 202, 203, 212, 213, 214, 216, 217, 219, 220, 221,
             222, 223, 224, 225, 226, 227, 228, 230, 231, 232, 233, 234,
             235, 236, 237, 238, 239, 240, 241, 243, 244, 246, 247, 249,
             250, 255, 256, 258, 259, 262, 264, 265, 266, 267, 268, 271,
             273, 274, 275, 277, 278, 279, 282, 283, 284, 288, 289, 290,
             291, 296, 297, 298, 300, 303, 304, 305, 306, 307, 308, 312,
             313, 314, 316, 318, 319, 322, 323, 326, 329, 330, 332, 334,
             337, 338, 339, 343, 344, 347, 380]

    psustava = [25, 28, 29, 30, 253, 254, 257, 294, 301, 321, 325, 335,
                336, 341, 342, 345, 348, 349, 350, 352, 353, 355, 356,
                357, 358, 359, 360, 362, 367, 371, 372, 373, 375, 376,
                377, 379, 381]

    chvazba = [31, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44,
               45, 46, 47, 48, 49, 50, 61, 63, 64, 65, 66,
               68, 242, 245, 263, 292, 293, 295, 315]

    nazvoslovie = [52, 54, 70, 147, 148, 149, 150, 151, 152, 153, 154,
                   155, 211, 229, 248, 261, 270, 272, 281, 285, 286,
                   287, 299, 302, 310, 311, 320, 327, 331, 333]

    veliciny = [69, 100, 106, 107, 110, 113, 114, 116,
                122, 123, 129, 130, 136, 139, 140]

    kyszas = [71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84,
              85, 86, 87, 88, 89, 90, 91, 92, 93, 98, 99, 102,
              103, 104, 108, 109, 276, 280, 317, 351]

    reakcie = [101, 115, 127, 131, 132, 133, 134, 135, 137, 138, 141, 142,
               146, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166,
               167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178,
               179, 180, 181, 191, 192, 193, 194, 195, 196, 197, 198, 199,
               200, 201, 204, 205, 206, 207, 208, 209, 210, 218, 251, 252,
               260, 269, 309, 324, 328, 340, 346, 354]

    rovnovaha = [182, 183, 184, 185, 186, 187, 188, 189, 190]

    komplexy = [361, 363, 364, 365, 366, 368, 369, 370, 378, 382]

    priklady = [386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397,
                398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
                410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421,
                422, 423, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434,
                435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446,
                447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458,
                459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470,
                471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482,
                483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494,
                495, 496, 497, 498, 499, 500]

    list_big_mess = [atom,
                     sustavalatok,
                     latky,
                     psustava,
                     chvazba,
                     nazvoslovie,
                     veliciny,
                     kyszas,
                     reakcie,
                     rovnovaha,
                     komplexy,
                     priklady]

    for x in range(len(list_names)):
        dic = {}
        dic.update({"name_of_list": list_of_categories[x]})
        dic.update({"lst": list_big_mess[x]})

        ltable.insert_one(dic)
