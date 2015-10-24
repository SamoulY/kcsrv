from sqlalchemy import inspect

from . import db


class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    fuel = db.Column(db.Integer)
    ammo = db.Column(db.Integer)
    steel = db.Column(db.Integer)
    baux = db.Column(db.Integer)


    def to_list(self):
        data = []
        if self.fuel is not None:
            data.append(self.fuel)
        if self.ammo is not None:
            data.append(self.ammo)
        if self.steel is not None:
            data.append(self.steel)
        if self.baux is not None:
            data.append(self.baux)
        return data


    def none(self):
        self.ammo = self.fuel = self.steel = self.baux = None
        return self


class Stats(db.Model):
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    luck = db.Column(db.Integer)
    firepower = db.Column(db.Integer)
    armour = db.Column(db.Integer)
    torpedo = db.Column(db.Integer)
    antiair = db.Column(db.Integer)
    antisub = db.Column(db.Integer)
    evasion = db.Column(db.Integer)
    los = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    dive_bomber = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    range_ = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    ammo = db.Column(db.Integer)
    fuel = db.Column(db.Integer)


    def copy(self, target=None):
        target = target if target else Stats()
        mapper = inspect(self)
        for column in mapper.attrs:
            if column.key != "id":
                setattr(target, column.key, getattr(self, column.key))
        return target


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    chance = db.Column(db.Integer)
    ship_id = db.Column(db.ForeignKey('ship.id'))
    min_resources_id = db.Column(db.ForeignKey('resources.id'), index=True)
    max_resources_id = db.Column(db.ForeignKey('resources.id'), index=True)

    max_resources = db.relationship('Resources', primaryjoin='Recipe.max_resources_id == Resources.id')
    min_resources = db.relationship('Resources', primaryjoin='Recipe.min_resources_id == Resources.id')
