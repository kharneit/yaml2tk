from abc import ABC
from dataclasses import dataclass, field
from tkinter import Misc, Frame, Label, Entry, Listbox, Checkbutton, Button
from typing import Any

@dataclass
class InterfaceContent():
    id:                 str
    object:             Misc

@dataclass
class ElementUIData():
    id:                 str                                     # Unique ID for each UI-Element
    module:             str     = None                          # Element-Type according to Tkinter-Subclasses
    loader:             str     = None                          # Tkinter loader to apply on this element (grid|pack|place)
    children_loader:    str     = None
    master:             str     = None                          # Master-Elements ID
    class_ui:           str     = None                          # Apply certain UI-Class
    arguments:          dict    = field(default_factory=dict)   # Arguments for element initialization
    attributes:         dict    = field(default_factory=dict)   # Attributes to be set after initialization
    loader_arguments:   dict    = field(default_factory=dict)   # Arguments for loader
    sequence_methods:   dict    = field(default_factory=dict)   # Sequence of methods with key-value pairs
    post_hook:          dict    = field(default_factory=dict)   # Sequence of methods to apply after all children elements are loaded
    bind_to:            str     = None                          # If given, bind to this local variable
    children:           list['ElementUIData'] = field(default_factory=list) # Elements children elements
    children_objects:   list['Misc'] = field(default_factory=list)

    def __post_init__(self):
        #   Set parent value of each child to this id
        if self.children is None: return
        children = []
        for child in self.children:
            child = ElementUIData(**child)
            child.loader = self.children_loader
            children.append(child)
        self.children = children

@dataclass
class ListElementData():
    parent_object: Any
    parent_class: str
    child_id: str
    arguments: dict[str:Any]
