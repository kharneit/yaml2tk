from tkinter import Misc, Tk

class ContentHandler():
    def add_attribute(self, ui_element: dict[str:Misc]) -> None:
        self.__dict__ = { **self.__dict__ , **ui_element }