from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from tkinter import IntVar
from importlib import import_module
from os import path
from yaml import safe_load
import ClassesInterface
import ContentHandler
import ClassesListObjects
from ClassesUI_Common import ElementUI, Factory, TKINTER_MODULE

ROOT_WINDOW_METHOD = 'Tk'
TKINTER_TTK_SUBMODULE = 'ttk'
TTK_METHOD_REGISTER = 'Notebook'
DEFAULT_GEOMETRY = '600x600'
DEFAULT_TITLE    = 'EasyUI - Main Window'



class FactoryElementUI(Factory):
    """ Generic factory for this modules custom classes """
    def __init__(self, data: ClassesInterface.ElementUIData):
        self.data = data
    def get_instance(self) -> ElementUI:
        data = self.data
        match data.class_ui:
            case 'root': return_object =  WindowElement
            case 'ListBox': return_object =  ClassesListObjects.ListBox
            case 'ListBoxCheckboxes': return_object =  ClassesListObjects.ListBoxCheckboxes
            case 'Button': return_object =  Button
            case 'CheckBox': return_object =  CheckBox
            case 'RegisterElement': return_object =  RegisterElement
            case _: return_object =  ElementUI
        return self.post_hook(return_object, data)
    def post_hook(self, return_object: ElementUI, data: ClassesInterface.ElementUIData = None) -> ElementUI:
        """ Could totally be implemented in self.get_instance but is left seperate as a hook for easy
            overriding of the return_object value in subclasses without redefining the standard cases """
        return  return_object(data)
    
class WindowElement(ElementUI):
    """ Special element for the root window """
    def build(self) -> None:
        arguments = self.data.arguments
        module = import_module(TKINTER_MODULE)
        method = getattr(module, ROOT_WINDOW_METHOD)
        self.object = method(**arguments)

        self.object.geometry(DEFAULT_GEOMETRY)
        self.object.title(DEFAULT_TITLE)

        self.set_attributes()
        self.process_method_sequence()



class Button(ElementUI):
    """ Generic button element for use outside of list contexts"""
    def set_command(self, command_button) -> None:
        self.object.configure(command = command_button)

class CheckBox(ElementUI):
    """ Generic checkbox element for use outside of list contexts """
    def __init__(self, data: ClassesInterface.ElementUIData) -> None:
        super().__init__(data)
        self.status = IntVar()
    def __build__(self) -> None:
        super().build()
        self.object.configure(
            variable = self.status,
            onvalue = 1,
            offvalue = 0
        )
    def get_status(self):
        return self.status.get()
    def set_command(self, command_button) -> None:
        self.object.configure(command = command_button)

class RegisterElement(ElementUI):
    """ Special element for registers/subwindows """
    def build(self) -> None:
        arguments = self.data.arguments
        module = import_module(TKINTER_MODULE)
        submodule = getattr(module, TKINTER_TTK_SUBMODULE)
        self.object = getattr(submodule, TTK_METHOD_REGISTER)(**arguments)
        
        function_loader = getattr(self.object, self.data.loader)
        if not self.data.loader_arguments is None:
            function_loader(**self.data.loader_arguments)
        else: 
            function_loader()
        
    def build_post_hook(self, children, content) -> None:
        for child in children:
            if child.bind_to is None:
                raise Exception(f'Missing bind_to argument in configuration. Element {child.id} can not be constructed. For children of registers a binding is mandatory.')
            getattr(self.object, 'add')(getattr(content, child.bind_to).object, text=child.id)


# Can not be instantiated in the beginning as class is described in this file
DEFAULT_FACTORY = FactoryElementUI

class WindowBuilder():
    """ Handler class to spin up the window and all its children by a given configuration file """
    def __init__(self, path_to_config: str):
        if not path.exists(path_to_config):
            raise FileNotFoundError(f'Could not get configuration file frrom location: {path_to_config}')
        with open(file = path_to_config, mode = 'r', encoding = 'utf8') as file:
            self.configuration = ClassesInterface.ElementUIData(**safe_load(file.read()))
        self.content = ContentHandler.ContentHandler()
        if self.configuration.module is None: self.configuration.module = 'Tk'

    def process_configuration(self, factory_select: Factory = None) -> ContentHandler:
        """ Basic method for external call that handles self.generate_elements and returns the modified self.content"""
        if factory_select is None: factory_select = DEFAULT_FACTORY
        self.generate_elements(self.configuration, factory_select)
        return self.content

    def generate_elements(self, element: ClassesInterface.ElementUIData, factory_select: Factory) -> None:
        """ Recursively sets up window by calling the elements/childrens build methods """
        element_object = factory_select(element).get_instance()
        element_object.build()
        childs_post = []
        #   If the object has a 'bind_to' attribute, append it to contents attributes
        if element.bind_to is not None:
            self.content.add_attribute({element.bind_to: element_object})
        for child in element_object.data.children:
            child.master = element_object.object
            self.generate_elements(child, factory_select)
            childs_post.append(child)
        element_object.build_post_hook(childs_post, self.content)
        return element_object
