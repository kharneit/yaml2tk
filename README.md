# **yaml2tk**
Support package for tkinter to define basic user-interfaces in yaml.
This package is licensed under the [2-Clause-BSD license](./LICENSE).

# Description
Reads content from given files and creates a object-structure of tkinter interface elements and 
supports them to a object where they can be accessed as attributes named by arguments in the
configuration file.
### Scope
**The projects scope** is to supply a method to quickly implement basic user interfaces in a
easily replicable and adaptable manner. By storing all required information to spin up 
a filled and initialized window with interactable elements in a yaml file, this can quickly 
be set up to initialize a project. Due to its modular structure its easy to extend.
Another priority is to keep dependencies low.

**Not part of the scope** is to support each and every of tkinters classes and functionalities.
Anyways, due to the generic structure of interpreting certain arguments as tkinter classes
and function calls, it might be appliable to more than the explicitlitly mentioned classes
in this document.

---

# Usage

This is a short guide to create an simple window with the yaml2tk module.


## Creating a window

Define your window element as the first element in config.yaml.
Place all children element as a list inside of the argument "children".
Continue as a recursive structure containing further elements as children arguments.
The root element can only have children, not siblings.
As the arguments are common for every child and parent, most arguments are 
applicable to all instances of tkinter objects. 
As some of them will be parsed as tkinter modules, classes and functions/methods,
have a further look at [tkinter's documentation](https://docs.python.org/3/library/tk.html).


### Example config.yaml
```
id: 'main'
children_loader: 'pack'
children:
-
  id: 'left'
  module: 'Frame'
  bind_to: 'frame_left'
  arguments:
    bg: 'red'
  loader_arguments:
    fill: 'both'
    expand: True
- id: 'right'
  module: 'Frame'
  arguments:
    bg: 'blue'
    expand: True
  loader_arguments:
    fill: 'both'
    expand: True
```
This is equivalent to the window structure created by the following code:
```
from yaml2tk.ContentHandler import ContentHandler
def build():
    content = ContentHandler()
    content.main = tk.Tk()
    main.pack()
    content.left = tk.Frame(
        background = 'red'
    )
    content.left.pack(
        fill='both',
        expand=True
    )
    right = tk.Frame(
        background = 'blue'
        expand=True
    )
    right.pack(
        fill = 'both'
        expand = True
    )
    return(contentHandler)
```
> *Be aware of subtle differences in the structure:* While the loader is set per element in plain-tkinter,
> this module instead uses `children_loader` arguments, to set it once for all children, as all children elements
> anyways must use the same loader.

## Implementation
You can instanciate the window like in this example:
```
from yaml2tk.ClassesUI import WindowBuilder

CONFIG_PATH = '/path/to/configuration/file.yaml'

if __name__ == '__main__':
  content = WindowHandler(CONFIG_PATH)
```
This returns an instanciated WindowHandler object with every attribute you defined as a bind_to to on any object
in your configuration. You can access it by `content.BIND_TO_ARGUMENT.object`. Besides that, `content.data` contains
every attribute you described for this object in you config file.

---

# Reference

|Attribute|Description|
|---------|-----------|
|id|Unique identifier for this object |
|classes_ui|string with yaml2tk classes name (ElementUI, WindowElement, ListBox, ListBoxCheckboxes, ListElement, ...)[^1] |
|module|tkinter module to load for this object(Tk, Frame, Label, Entry, Listbox, List, Button, ...)[^1] |
|bind_to|content.ATTRIBUTE to associate this object with |
|arguments|dictionary of initializations arguments of the class set in module, be aware of compatibility between the attribute and the class |
|sequence_methods|dictionary with method:arguments pairs that are applied to the instanciated module object |
|post_hook|same, but applied after all childrens are processed |
|children_loader| | loader to use to load children |
|*loader*| Internal arguments that is set to the parends children_loader element when children are instanciated and thats actually processed by the build method|
[^1]: When instanciating the root element, these arguments are overridden by the needed arguments to spawn the main window
