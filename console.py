#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split as shlex_split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def parse(arg):
    curly_braces_match = re.search(r"\{(.*?)\}", arg)
    brackets_match = re.search(r"\[(.*?)\]", arg)
    if curly_braces_match is None:
        if brackets_match is None:
            return [i.strip(",") for i in shlex_split(arg)]
        else:
            lexer = shlex_split(arg[:brackets_match.span()[0]])
            ret_list = [i.strip(",") for i in lexer]
            ret_list.append(brackets_match.group())
            return ret_list
    else:
        lexer = shlex_split(arg[:curly_braces_match.span()[0]])
        ret_list = [i.strip(",") for i in lexer]
        ret_list.append(curly_braces_match.group())
        return ret_list


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """
        Do nothing upon receiving an empty line.
        """
        pass

    def default(self, arg):
        """Defines the default behavior for the `cmd` module when input is invalid."""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match_arg = re.search(r"\.", arg)
        if match_arg is not None:
            arg_var = [arg[:match_arg.span()[0]], arg[match_arg.span()[1]:]]
            match_arg = re.search(r"\((.*?)\)", arg_var[1])
            if match_arg is not None:
                command = [arg_var[1][:match_arg.span()[0]], match_arg.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg_var[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit the program and exit the command interpreter."""
        return True

    def do_EOF(self, arg):
        """Signal to exit the program when encountering EOF (End-of-File)."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of the specified class.

        Usage: create <class_name>

        Parameters:
        - class_name (str): The name of the class to create an instance of.

        Description:
        Creates a new instance of the specified class and prints its unique identifier.
        """
        arg_var = parse(arg)
        if len(arg_var) == 0:
            print("** class name missing **")
        elif arg_var[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_var[0])().id)
            storage.save()

    def do_show(self, arg):
        """Display the string representation of a class instance.

        Usage: show <class> <id> or <class>.show(<id>)

        Parameters:
        - class_name (str): The name of the class of the instance to display.
        - id (int): The identifier of the instance to display.

        Description:
        Displays the string representation of a class instance specified by its id.
        """
        arg_var = parse(arg)
        obj_dict = storage.all()
        if len(arg_var) == 0:
            print("** class name missing **")
        elif arg_var[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_var) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_var[0], arg_var[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_var[0], arg_var[1])])

    def do_destroy(self, arg):
        """Delete a class instance based on its id.

        Usage: destroy <class> <id> or <class>.destroy(<id>)

        Parameters:
        - class_name (str): The name of the class of the instance to be deleted.
        - id (int): The identifier of the instance to be deleted.

        Description:
        Deletes a class instance specified by its id.
        """
        arg_var = parse(arg)
        obj_dict = storage.all()
        if len(arg_var) == 0:
            print("** class name missing **")
        elif arg_var[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_var) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_var[0], arg_var[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_var[0], arg_var[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_var = parse(arg)
        if len(arg_var) > 0 and arg_var[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg_var) > 0 and arg_var[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_var) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Retrieve the number of instances of a given class.

        Usage:
            - count <class>: Retrieve the number of instances of the specified class.
            - <class>.count(): Alternative way to retrieve the number of instances of the specified class.

        Parameters:
        - class_name (optional, str): The name of the class of instances to count.

        Description:
        Retrieves the number of instances of the specified class.
        """
        arg_var = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_var[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Update a class instance of a given id.

        Usage:
            - update <class> <id> <attribute_name> <attribute_value>: Update instance with the specified id by adding or updating a single attribute.
            - <class>.update(<id>, <attribute_name>, <attribute_value>): Alternative way to update instance attributes.
            - <class>.update(<id>, <dictionary>): Update instance attributes using a dictionary.

        Parameters:
        - class_name (str): The name of the class of the instance to update.
        - id (int): The identifier of the instance to update.
        - attribute_name (str): The name of the attribute to add or update.
        - attribute_value (any): The value of the attribute to add or update.
        - dictionary (dict): A dictionary containing attribute key/value pairs to update.

        Description:
        Updates a class instance of a given id by adding or updating a specified attribute key/value pair or dictionary.
        """
        arg_var = parse(arg)
        obj_dict = storage.all()

        if len(arg_var) == 0:
            print("** class name missing **")
            return False
        if arg_var[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_var) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_var[0], arg_var[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_var) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_var) == 3:
            try:
                type(eval(arg_var[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_var) == 4:
            obj = obj_dict["{}.{}".format(arg_var[0], arg_var[1])]
            if arg_var[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_var[2]])
                obj.__dict__[arg_var[2]] = valtype(arg_var[3])
            else:
                obj.__dict__[arg_var[2]] = arg_var[3]
        elif type(eval(arg_var[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_var[0], arg_var[1])]
            for k, v in eval(arg_var[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
