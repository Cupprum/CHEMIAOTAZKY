from pymongo import MongoClient
import pprint
import xml.etree.ElementTree as ET


client = MongoClient('mongodb://localhost:27017/')
db = client.chemia
qtable = db.table_questions

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
            dic_otazka = {"ot": None,
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

            qtable.insert_one(dic_otazka)
            counter += 1


insert_all_func()
