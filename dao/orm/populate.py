import datetime
from werkzeug.security import generate_password_hash
from dao.orm.model import *
from dao.db import PostgresDb

db = PostgresDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

session.query(order).delete()
session.query(wish).delete()
session.query(melody).delete()
session.query(album).delete()
session.query(student).delete()
session.query(genre).delete()
session.query(performer).delete()

atam_blues_0120 = order(id=1, username='@nechla', date=datetime.date(2020, 1, 1), criteria='melody', value="Blues")

Atamanchuk = student(id=1, faculty='FICT', surname='Atamanchuk', name='Lena', username='@nechla', password=generate_password_hash('qwerty12345', 'sha256'))
Yaremchuk = student(id=2, faculty='IASA', surname='Yaremchuk', name='Daniel', username='@reya', password=generate_password_hash('qwerty12345', 'sha256'))
Varzhansky = student(id=3, faculty='FMM', surname='Varzhansky', name='Illya', username='@ilyavl', password=generate_password_hash('qwerty12345', 'sha256'))
Kovtonyuk = student(id=4, faculty='FICT', surname='Kovtonyuk', name='Vova', username='@kovla', password=generate_password_hash('qwerty12345', 'sha256'))
Palyokha = student(id=5, faculty='FICT', surname='Palyokha', name='Sasha', username='@pasha', password=generate_password_hash('qwerty12345', 'sha256'))
Lutska = student(id=6, faculty='FICT', surname='Lutska', name='Liza', username='@lutskayaliz', password=generate_password_hash('qwerty12345', 'sha256'))
Kubenko = student(id=7, faculty='FMM', surname='Kubenko', name='Masha', username='@kubomash', password=generate_password_hash('qwerty12345', 'sha256'))
Samsoniuk = student(id=8, faculty='IASA', surname='Samsoniuk', name='Petya', username='@samsopet', password=generate_password_hash('qwerty12345', 'sha256'))
Popova = student(id=9, faculty='IASA', surname='Popova', name='Rita', username='@ri_ta_po', password=generate_password_hash('qwerty12345', 'sha256'))

pop = genre(id=1, name='pop', psychotype='gipertim')
indie = genre(id=2, name='indie', psychotype='emotive')
rock = genre(id=3, name='rock', psychotype='isteroid')
romans = genre(id=4, name='romans', psychotype='disturbing')
classic = genre(id=5, name='classic', psychotype='PSYCHASTENOID')
blues = genre(id=6, name='blues', psychotype='emotive')
jazz = genre(id=7, name='jazz', psychotype='gipertim')

Elzy = performer(id=1, name='Okean Elzy')
Hardkiss = performer(id=2, name='The Hardkiss')
Babkin = performer(id=3, name='Serhii Babkin')
Zemfira = performer(id=4, name='Zemfira')
Jackson = performer(id=5, name='Michael Jackson')

no_album1 = album(id=0, title='Blues', performer_id=4)
Zemlya = album(id=1, title='Zemlya', performer_id=1)
Closer = album(id=2, title='Closer', performer_id=2)
Muzasfera = album(id=3, title='Muzasfera', performer_id=3)
no_album2 = album(id=4, title='Smooth Criminal', performer_id=5)

Prirva = melody(id=1, title='Prirva', singer='The Hardkiss', release_date=datetime.date(2016, 4, 19), melody_genre=4,album_id=2)
Blues = melody(id=2, title='Blues', singer='Zemfira', release_date=datetime.date(2009, 12, 30), melody_genre=6,album_id=0)
Criminal = melody(id=3, title='Smooth Criminal', singer='Michael Jackson', release_date=datetime.date(1997, 11, 5), melody_genre=1,album_id=4)

atam1912 = wish(id=1, student_id=1, wish_date=datetime.date(2019, 12, 19), wish_criteria='melody', melody_id=1)
kovt1912 = wish(id=2, student_id=4, wish_date=datetime.date(2019, 12, 19), wish_criteria='genre', melody_id=1)
paly1812 = wish(id=3, student_id=5, wish_date=datetime.date(2019, 12, 18), wish_criteria='genre', melody_id=3)
kube1612 = wish(id=4, student_id=7, wish_date=datetime.date(2019, 12, 16), wish_criteria='genre', melody_id=3)
session.add_all([atam_blues_0120, Atamanchuk,Yaremchuk,Varzhansky,Kovtonyuk,Palyokha,Lutska,Kubenko,Samsoniuk,Popova,pop,indie,rock,romans,classic,blues,jazz,
                 Elzy,Hardkiss,Babkin,Zemfira,Jackson,no_album1,Zemlya,Closer,Muzasfera,no_album2,Prirva,Blues,Criminal,atam1912,kovt1912,
                 paly1812, kube1612])

session.commit()