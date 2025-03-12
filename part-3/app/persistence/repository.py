import uuid
from app import db

# Interface de base pour le dépôt


class Repository:
    def add(self, obj):
        raise NotImplementedError

    def get(self, obj_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def update(self, obj_id, data):
        raise NotImplementedError

    def delete(self, obj_id):
        raise NotImplementedError

    def get_by_attribute(self, attr_name, attr_value):
        raise NotImplementedError

# Implémentation du dépôt avec SQLAlchemy


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


class InMemoryRepository:
    """
    Simple in-memory repository for storing objects.
    """

    def __init__(self):
        self.storage = {}

    def add(self, obj):
        if not obj.id:
            obj.id = str(uuid.uuid4())
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def delete(self, obj_id):
        return self.storage.pop(obj_id, None)

    def update(self, obj_id, new_obj):
        if obj_id in self.storage:
            self.storage[obj_id] = new_obj
            return new_obj
        return None

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self.storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None

    def get_all(self):
        return list(self.storage.values())
