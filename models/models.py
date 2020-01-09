from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class FeatureContent(Base):
    __tablename__ = 'featurecontents'
    id = Column(Integer, primary_key=True)
    feature = Column(String(128), unique=True)
    details = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, feature=None, details=None, date=None):
        self.feature = feature
        self.details = details
        self.date = date

    def __repr__(self):
        return '<Feature %r>' % (self.feature)

#DBにユーザーの名前とパスワードを格納するためのusersテーブル
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)