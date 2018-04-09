import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url = urlparse(os.environ["DATABASE_URL"])
db_syntax = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
db_syntax_final = ('postgresql://' + url.username + ':' + url.password + '@' + url.hostname + '/' + url.path[1:])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_syntax_final
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class jedlo_sql(db.Model):
    __tablename__ = 'chemia'
    nazov = db.Column(db.String(256), primary_key=True)
    attribute = db.Column(db.String(256))
    link = db.Column(db.String(256))


tree = ET.parse('chemia.xml')
root = tree.getroot()


def create_func():
    db.create_all()


def drop_func():
    db.drop_all()


def insert_all_func():
    db.create_all()
    ypsilon = 1
    for jedlo_xml in root.findall('jedlo'):
        number = jedlo_xml.attrib.get('number')
        if str(ypsilon) == number:
                nazov_xml = str(jedlo_xml.find('nazov').text)
                attribute_xml = str(jedlo_xml.find('attribute').text)
                link_xml = str(jedlo_xml.find('link').text)
                nazov_xml = nazov_xml[13:-9]
                attribute_xml = attribute_xml[13:-9]
                link_xml = link_xml[13:-9]
                exists = jedlo_sql.query.filter_by(nazov=nazov_xml).first()
                if exists is None:
                    jedlo_pridavane = jedlo_sql(nazov=nazov_xml, attribute=attribute_xml, link=link_xml)
                    db.session.add(jedlo_pridavane)
                ypsilon += 1
    db.session.commit()
