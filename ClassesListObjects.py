from ClassesUI_Common import ElementUI, Factory
from ClassesInterface import ElementUIData, ListElementData
from tkinter import Misc, IntVar, Button
from typing import Any

class ListBox(ElementUI):
    def __init__(self, data: ElementUIData):
        super().__init__(data)
        self.elements: list[ListBoxElement] = []
   
    def add_element(self, title: str, factory: Factory = None, element_data: ListElementData = None):
        if factory == None: factory = FactoryListBoxElement
        if element_data is None:
            element_data = self.get_element_data(title)
        element_object = factory().get_instance(element_data)
        element_object.build()
        self.elements.append(element_object)
    
    def get_element_data(self, title: str) -> ListElementData:
        element_data = ListElementData(
            parent_object=self.object, 
            parent_class=self.__class__.__name__, 
            child_id=f'generic:{self.data.id}.{title}',
            arguments={'text': title}
        )
        return element_data

    def clear(self):
        for element in self.elements:
            element.container.object.destroy()
            element.object.destroy()
        self.elements = []

class ListBoxTables(ListBox):
    """ Until now same behaviour as ListBox. Anyways implemented as the FactoryListBoxElement differs by
        parents class """
    ...


class ListBoxCheckboxes(ListBoxTables):
    def get_elements_status(self) -> list[bool]:
        result: list[bool] = []
        for element in self.elements:
            result.append(bool(element.status.get()))
        return result
    
    def are_any_true(self) -> bool:
        return True in self.get_elements_status()
    
    def are_all_true(self) -> bool:
        return not False in self.get_elements_status()


class ListBoxElement(ElementUI):
    def __init__(self, data: ListElementData):
        """ Create container as list row for formatting reasons and then call hook for 
            specific elements configuration """
        self.container = ElementUI(
            ElementUIData(
                id='container', 
                master= data.parent_object, 
                module='Frame', 
                loader='pack',
                loader_arguments={
                    'fill':'x',
                    'side':'top',
                    'expand': False
                }
            )    
        )
        self.container.build()
        element_data = self.configure(data)
        super().__init__(element_data)
        
    def configure(self, data: ListElementData) -> ElementUIData:
        """ Moved to seperate method to maintain overrideability in ancestor-classes """
        element_data = ElementUIData(
            id=data.child_id, 
            master=self.container.object,
            module='Label',
            arguments={'text': data.arguments['text']},
            loader='pack',
            loader_arguments={
                'side': 'left',
                'expand': False
            }
        )
        return element_data

class ListBoxElementCheckboxes(ListBoxElement):
    def configure(self, data: ListElementData) -> ElementUIData:
        self.status = IntVar()
        self.status.set(1)
        element_data = ElementUIData(
            id=data.child_id,
            master=self.container.object,
            module='Checkbutton',
            arguments={
                'text':data.arguments['text'],
                'variable': self.status
            },
            loader='pack',
            loader_arguments={
                'side': 'left',
                'expand': False
            }
        )
        return element_data 
    
    def get_status(self) -> bool:
        return bool(self.status.get())

        
class FactoryListBoxElement(Factory):
    def get_instance(self, data: ListElementData) -> ListBoxElement:
        class_parent = data.parent_class
        result = None
        match class_parent:
            case 'ListBox': result = ListBoxElement
            case 'ListBoxCheckboxes': result = ListBoxElementCheckboxes                 
        return self.post_hook(result, data)
    def post_hook(self, class_element: type, data: ListElementData) -> ListBoxElement:
        if class_element is None: raise NotImplementedError('There is no default ListBoxElement for the given ListBox-subclass.')
        return class_element(data)