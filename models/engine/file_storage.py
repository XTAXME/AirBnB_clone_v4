#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return FileStorage.__objects
        else:
            return {key: value for key, value in FileStorage.__objects.items()
                    if cls.__name__ in key}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
    def delete(self, obj=None):
        """to delete obj from __objects if it’s 
        inside - if obj is equal to None, the method 
        should not do anything

        Args:
            obj (optional): Object to delete. Defaults to None."""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in FileStorage.__objects.keys():
                del FileStorage.__objects[key]
     def get(self, cls, id_):
        """
        Retrieve one object

        Arguments:
            cls: string representing a class name
            id_: string representing the object id

        Return:
           object of cls and id passed in argument
        """
        if (cls not in self.__models_available.keys()) or (id_ is None):
            return None
        all_objs = self.all(cls)
        for k in all_objs.keys():
            if k == id_:
                return all_objs[k]
        return None

    def count(self, cls=None):
        """
        Number of objects in a certain class

        Arguments:
            cls: String representing a class name (default None)

        Return:
            number of objects in that class or in total.
            -1 if the class is not valid
        """
        if cls is None:
            return len(self.__objects)
        if cls in self.__models_available:
            return len(self.all(cls))
        return -1
