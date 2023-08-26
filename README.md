# **yaml2tk**
Support package for tkinter to define basic user-interfaces in yaml
| | |
|-|-|
|License|This package is licensed under the [2-Clause-BSD license](./LICENSE) so you can use it for any private or commercial projects, as long as you include the linked files contents. Be aware that there is no warranty and make sure to read and understand the whole license (It is a very short document), as this explanation is only a short overview.|
|Dependencies <br> *(Standard-library)*|*dataclasses <br> abc <br> os <br> typing <br> tkinter <br> importlib*  <br> [pyyaml](https://github.com/yaml/pyyaml)

# Content

- Description
  - Scope
- Explanations
  - Internal arguments
  - Tkinter-basics
    - Structure
    - instantiating an element
    - Displaying an object
- Usage
  - Creating a window
  - Implementation
  - Customization
- Reference 

# Description
Reads content from given files and creates a object-structure of tkinter interface elements and 
supports them to a object where they can be accessed as attributes named by arguments in the
configuration file.
### Scope
**This projects scope** is to supply a method to quickly implement basic user interfaces in a
easily replicable and adaptable manner. By storing all required information to spin up 
a filled and initialized window with interactable elements in a yaml file, this can quickly 
be set up to initialize a project. Due to its modular structure its easy to extend.
Another priority is to keep dependencies low. Reducing them to only python-standard-libraries is
one target of the further development.

**Not part of the scope** is to support each and every of tkinters classes and functionalities.
Anyways, due to the generic structure of interpreting certain arguments as tkinter classes
and function calls, it might be appliable to more than the explicitlitly mentioned classes
in this document.

# Explanations

## Internal arguments

There are a few arguments in the configuration that are needed by this program to create
the window structure:
|name|description|
|-|-|
|**`id`**| **Mandatory**: Unique id for each element
|*`bind_to`*| *Optional*: Output objects attribute that will be connected with the given object
|*`class_ui`*| *Optional*: Set internal handler class, if not explicitly mentioned, this will be set to the common ElementUI-class


## Tkinter-basics
If you're used to tkinter, you can easily skipt this segment.
If not, here are some basics about tkinter to improve the comprehensibility of 
further segments of this document. If you're looking for further explanation of this,
have a look at [tkinter's documentation](https://docs.python.org/3/library/tk.html).

### Structure
> Whether it seems appropriate or not, tkinters names the root element of any of its children
> as its *master*. To prevent any unneccesary confusion, i will stick to tkinters internal name
> to maintain intelligibility.

In tkinter, all displayed elements like areas of windows, buttons, lists,
are bound to their master-element up until they reach the root element of the structure,
your main window. The form of this structure is reflected in your config file, as you 
create your root element, add children elements and expand those children further.

### instantiating an object

When creating a tkinter object you always need to pass its master-element and further
optional arguments, like background color or text. Some other parameters are set by directly 
accessing the objects element or using methods of the object.
This resembles the following elements of the configuration:
|argument|description|
|-|-|
|**`module`**|Refers to the tkinter-subclass you want to instantiate the object with, like Frame or Label.[^1] **Mandatory** on any element except for window-elements|
|*`arguments`*| Dictionary of key-value-pairs that it used to instantiate the object. The master argument is supplied automaticly according to the structure of the config file.|
|*`attributes`*| are attributes that are directly set on the instantiated objects.|
|*`sequence_methods`*| A dictionary or a list with key:value pairs that resemble called method: arguments. If you want to apply the same method multiple times, you need to pass the arguments as a list of dictionaries.| 
|*`post_hook`*| Like `sequence_methods` but it is applied after all children are processed.

### Displaying an element
After you created your tkinter-element you need to load it to bring it onto the display. This is done by applying one of three loader methods: `grid`, `pack`, `place`.
Grid is used for column layouts, pack places elements dynamically by only a few directional commands and place can be used to put an element to a certain, specified 
location inside its master-element.
When calling the loader-method, you can supply different arguments, depending on the loader, that affect the position and size of the element.
This is done by placing `children_loader` in the master-elements configuration, which sets the loader-method to use, and placing `loader_arguments` in the childs
configuration to support further arguments on the method call of the loader method by passing in an dictionary with the arguments.

# Usage

This is a short guide to create an simple window with the yaml2tk module.

## Creating a window

Define your window element as the first element in config.yaml.
Place all children element as a list inside of the argument `children`.
Continue as a recursive structure containing further elements as `children` arguments.
**The root element can only have children, not siblings.**
As the arguments are common for every child and parent, most arguments are 
applicable to all instances of tkinter objects. 
As some of them will be parsed as tkinter modules, classes and functions/methods,
have a further look at [tkinter's documentation](https://docs.python.org/3/library/tk.html).


### Example config.yaml
```
id: 'main'
bind_to: 'main_window'
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
> this module instead uses `children_loader` arguments, to set it once for all `children`, as all `children` elements
> anyways must use the same loader.

> On some tkinter method calls for the loader, like `columnconfigure` or `rowconfigure`, you might have multiple method calls
> applied to the same object. In this case, you need to pass the `sequence_methods` argument as a list, else the dictionary
> key will be overwritten by the last entry in your configuration.

## Implementation
You can instantiate the window like in this example:
```
from yaml2tk.ClassesUI import WindowBuilder

CONFIG_PATH = '/path/to/configuration/file.yaml'

if __name__ == '__main__':
  content = WindowHandler(CONFIG_PATH)
```
This returns an instantiated `WindowHandler` object with every attribute you defined as a bind_to to on any object
in your configuration. You can access it by `content.BIND_TO_ARGUMENT.object`. Besides that, `content.data` contains
every attribute you described for this object in you config file.

### Example
Considering the following segments of the former examples:
```
id: 'main'
...
children:
-
  id: 'left'
  module: 'Frame'
  bind_to: 'frame_left'
  ...
```
and
```
content = WindowHandler(CONFIG_PATH)
```
you could acces the frames tkinter object by calling `content.frame_left.object` as well as all its
initialization data by calling `content.frame_left.data`

## Customization
If you want to extend the given functionalities, it is supposed to create your own class that inherits from
the class `ElementUI` (or one of it's ancestors) to ensure compatibility with the other parts of this module.

---

# Reference

|Attribute|Description|
|---------|-----------|
|id|Unique identifier for this object |
|classes_ui|string with yaml2tk classes name (ElementUI, WindowElement, ListBox, ListBoxCheckboxes, ListElement, ...)[^1] |
|module|tkinter module to load for this object(Tk, Frame, Label, Entry, Listbox, List, Button, ...)[^1] |
|bind_to|content.ATTRIBUTE to associate this object with |
|arguments|dictionary of initializations arguments of the class set in module, be aware of compatibility between the attribute and the class |
|sequence_methods|dictionary or list of dictionaries with method:arguments pairs that are applied to the instantiated module object [^2]|
|post_hook|same, but applied after all childrens are processed |
|children_loader|  Loader to apply on any child element |
|*loader*| Internal arguments that is set to the parends children_loader element when children are instantiated and thats actually processed by the build method|
[^1]: When instantiating the root element, these arguments are overridden by the needed arguments to spawn the main window
[^2]: If you want to call the same method multiple times on the same object, you have to pass the sequence_methods as a list and not a nested dictionary. Else, the argument will be overwritten.
