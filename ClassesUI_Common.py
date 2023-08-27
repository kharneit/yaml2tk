import ClassesInterface
from importlib import import_module
from tkinter import Misc, ttk
from abc import ABC, abstractmethod

TKINTER_MODULE = 'tkinter'
TKINTER_SUBMODULE = '.Tk'

#   Segregated to this file to avoid circular dependencies when declaring interdependent subclasses 
#   Do not merge into subclasses files.
class ElementUI():
    """ Basic ElementUI-Class all other UI-Elements inherit from. """
    def __init__(self, data: ClassesInterface.ElementUIData) -> None:
        self.data = data        
        self.object: Misc = None

    def build(self) -> None:
        """ Dynamically loads the tkinter subclass that is defined in 
            the data from the configuration file """
        module_name = self.data.module
        master, arguments  = self.data.master, self.data.arguments
        loader, arguments_loader = self.data.loader, self.data.loader_arguments

        module = import_module(TKINTER_MODULE)
        class_tk = getattr(module, module_name)
        object = class_tk(master=master, **arguments)
        function_loader = getattr(object, loader)
        if not arguments_loader is None:
            function_loader(**arguments_loader)
        else: 
            function_loader()

        self.object = object

        if not self.data.attributes is None:
            self.set_attributes()
        if not self.data.sequence_methods is None:
            self.process_method_sequence()

    def set_attributes(self) -> None:
        """ Support method to handle either a single or multiple arguments"""
        for attribute, value in self.data.attributes.items():
            setattr(self.object, attribute, value)

    def process_method_sequence(self, sequence = None) -> None:
        """ Process through all elements of the sequence_methods. 
            Handles lists by recursively calling itself with each
            list entry, if sequence is given by list"""
        if sequence is None: sequence = self.data.sequence_methods
        object = self.object
        if not isinstance(sequence, list):
            for method, value in sequence.items():
                if isinstance(value, dict):
                    getattr(object, method)(**value)
                elif isinstance(value, list):
                    getattr(object, method)(*value)
                else:
                    getattr(object, method)(value)
        else:
            for element in sequence:
                self.process_method_sequence(element)

    def build_post_hook(self, *args) -> None:
        """ Mostly resembles process_method_sequence as additional hook """
        if self.data.post_hook is None: return
        object = self.object
        for method, value in self.data.post_hook.items():
            if isinstance(value, dict):
                getattr(object, method)(**value)
            elif isinstance(value, list):
                getattr(object, method)(*value)
            else:
                getattr(object, method)(value)

class Factory(ABC):
    """ Abstract class to enforce get_instance and post_hook on ancestors to
        ensure extendability """
    @abstractmethod
    def get_instance(self):
        ...
    @abstractmethod
    def post_hook(self):
        ...