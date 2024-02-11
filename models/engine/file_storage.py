#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """Represents a storage engine for serializing and deserializing objects to/from a JSON file.

    Attributes:
        _file_path (str): The path to the JSON file where objects are saved.
        _objects (dict): A dictionary containing instantiated objects.
    """
    _file_path = "file.json"
    _objects = {}

    def all(self):
        """Returns a dictionary containing all stored objects."""
        return FileStorage._objects

    def new(self, obj):
        """Adds a new object to the storage dictionary.

        Args:
            obj: The object to be added.
        """
        object_class_name = obj.__class__.__name__
        FileStorage._objects["{}.{}".format(object_class_name, obj.id)] = obj

    def save(self):
        """Serializes the objects dictionary to the JSON file."""
        objects_dict = {key: value.to_dict() for key, value in FileStorage._objects.items()}
        with open(FileStorage._file_path, "w") as file:
            json.dump(objects_dict, file)

    def reload(self):
        """Deserializes the JSON file to populate the objects dictionary."""
        try:
            with open(FileStorage._file_path) as file:
                objects_dict = json.load(file)
                for obj_data in objects_dict.values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            return