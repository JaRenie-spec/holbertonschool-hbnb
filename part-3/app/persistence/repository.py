from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, instance):
        from app import db
        db.session.add(instance)
        db.session.commit()

    def get(self, id):
        from app import db
        return db.session.query(self.model).get(id)

    def get_all(self):
        from app import db
        return db.session.query(self.model).all()

    def update(self, instance):
        from app import db
        db.session.commit()

    def delete(self, instance):
        from app import db
        db.session.delete(instance)
        db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None

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
