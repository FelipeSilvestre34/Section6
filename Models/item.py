from Db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def save_to_db(self): #funciona como insert/update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self): #str para o json
        return {
        'id': self.id, 
        'name': self.name,
        'price': self.price,
        'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        #SELECT * FROM items WHERE name=name cls=ItemModel
        return cls.query.filter_by(name=name,).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
