#!/usr/bin/env python3
"""contains the entry point of the command interpreter"""

import cmd
import json
import models
import readline
import resource
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage



class HBNBCommand(cmd.Cmd):
    """
        handles:
            EOF/'quit': exit the program
            'create': creates instances of AirBnB clone objects
            'show': prints string representation of an instance based on its id
            'destroy': deletes an instance
            'all': prints string representation of all instances
            'update': updates an instance based on its id
    """

    prompt: '(hbnb)'
    classes = [
        'BaseModel',
        'User',
        'State',
        'City',
        'Amenity',
        'Place',
        'Review'
    ]

    def do_EOF(self, arg):
        '''Exit the program'''
        return True

    def do_quit(self, arg):
        '''Exit command'''
        return True
    
    def emptyline(self):
        '''
            Method called when an empty line is entered in response to the prompt.
            If this method is not overridden, 
            it repeats the last nonempty command entered.
        '''
        pass

    def precmd(self, line):
        '''
            Hook method executed just before the command line line is interpreted, 
            but after the input prompt is generated and issued. 
        '''
        return (line)

    def default(self, arg):
        '''
            Method called on an input line when the command prefix is not recognized. 
            If this method is not overridden, it prints an error message and returns.
        '''
        try:
            cmd_info = arg.split('.')
            resource = cmd_info[0]
            passed_arg = cmd_info[1].strip('()').split('(')
            if passed_arg[0] == 'all':
                self.do_all(resource)
            elif passed_arg[0] == 'count':
                entries = FileStorage._FileStorage__objects
                entry_list = str(entries.keys())
                resource_count = entry_list.count(resource)
                print(resource_count)
            elif passed_arg[0] == 'show':
                payload = ''
                payload = resource + ' ' + passed_arg[1]
                self.do_show(payload)
            elif passed_arg[0] == 'destroy':
                payload = ''
                payload = resource + ' ' + passed_arg[1]
                self.do_destroy(payload)
            elif passed_arg[0] == 'update':
                options = str(passed_arg[1].replace(',', ''))
                payload = resource + ' ' + options
                self.do_update(payload)
            else:
                pass
        except IndexError:
            self.stdout.write('*** unknown syntax: %s\n'%arg)

    def do_create(self, arg):
        '''
            Creates a new instance of any AirBnB clone class
            and saves to JSON file
            Usage: create <class name>
        '''
        args = arg.split(" ")
        if not args[0]:
            print("** Class name is missing **")
            pass
        elif args[0] in HBNBCommand.classes:
            new = eval(args[0])()
            print(new.id)
            models.storage.save()
        else:
            print('** class does not exist **')

    def do_show(self, arg):
        '''
            Prints the string representation of an instance
            based on its ID number
            Usage: show <class name> <id>
        '''
        models.storage.reload()
        if len(arg) < 1:
            print('no class name recognised')
            pass
        else:
            arg = arg.split(' ')
            if arg[0] not in HBNBCommand.classes:
                print('Class does not exist')
            elif arg[0] in HBNBCommand.classes:
                if len(arg) < 2:
                    print('** instance id missing **')
                    return
                key = arg[0] + '.' + arg[1]
                if key in FileStorage._FileStorage__objects:
                    print(FileStorage._FileStorage__objects[key])
                else:
                    print('** No instance id Found **')

    def do_destroy(self, arg):
        '''
            Destroys an instance based on its ID number.
            Usage: destroy <class name> <id>
        '''
        if len(arg) < 1:
            print('** no class name recognised **')
            pass
        else:
            arg = arg.split(' ')
            if arg[0] not in HBNBCommand.classes:
                print('Class does not exist')
            elif arg[0] in HBNBCommand.classes:
                if len(arg) < 2:
                    print('** instance id missing **')
                    return
                key = arg[0] + '.' + arg[1]
                if key in FileStorage._FileStorage__objects:
                    FileStorage._FileStorage__objects.pop(key)
                    models.storage.save()
                else:
                    print("** no instance id found **")

    def do_all(self, arg):
        '''
             Prints the string representation of all instances.
            If only "all" is passed, all instances will be printed.
            If a class name is passed after "all", all instances of that
            class will be printed.
            Usage: all <class name>
        '''
        models.storage.reload()
        if len(arg) < 1:
            all_items = []
            for value in FileStorage._FileStorage_objects.values():
                all_items.append(str(value))
            if not all_items:
                return
            print(all_items)
        else:
            arg = arg.split(' ')
            if arg[0] not in HBNBCommand.classes:
                print('** class doesnt exist **')
            elif arg[0] in HBNBCommand.classes:
                all_items = []
                for value in FileStorage._FileStorage__objects.values():
                    if arg[0] in value.__class__.__name__:
                        all_items.append(str(value))
                if not all_items:
                    return
                print(all_items)

    def do_update(self, arg):
        '''
            Updates an attribute of an instance based on its ID number.
            Usage: update <class name> <id> <attribute> <value>
            id, created_at, and updated_at cannot be updated.   
        '''
        models.storage.reload()
        if len(arg) < 1:
            print("** class name missing **")
            pass
        else:
            arg = shlex.split(arg)
            if arg[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif arg[0] in HBNBCommand.classes:
                if len(arg) < 2:
                    print("** instance id missing **")
                    return
                key = arg[0] + '.' + arg[1]
                if key in FileStorage._FileStorage__objects:
                    dict_to_update = \
                        FileStorage._FileStorage__objects[key].__dict__
                    if len(arg) < 3:
                        print('**Attribute name missing**')
                    elif len(arg) < 4:
                        print("** value missing **")
                    else:
                        k = arg[2]
                        try:
                            attrtype = type(dict_to_update[k])
                            v = attrtype(arg[3])
                        except KeyError:
                            v = arg[3]
                        dict_to_update[k] = v
                        models.storage.save()
                else:
                    print('**No instance Found**')

if __name__ == '__main__':
    HBNBCommand().cmdloop()
