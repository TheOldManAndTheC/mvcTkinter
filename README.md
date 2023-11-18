# mvcTkinter

<h2 style="text-align: center;">WIP</h2>

## Description

mvcTkinter is a Python wrapper for the built-in Tkinter widgets that provides some basic MVC (Model-View-Controller) glue code to make writing GUI applications in Python a bit easier, as well as some compound widgets and built-in tooltips.

It emerged from a command line based Python project that was partially a way to learn Python, but grew quite a bit in scope. When I decided to expand the project to have a full fledged GUI, I chose Tkinter to ensure easy portability, but I also missed a lot of MVC features from other languages and frameworks I've used, so it ended up becoming another learning project.

mvcTkinter is far from complete, I've only really worked on the glue code for the Tkinter widgets I've been using, but it should hopefully grow as I use it in more projects.

## Getting Started

To use mvcTkinter in your project, open a terminal or shell and change directory to wherever you want the library to reside, then clone the repository:

	git clone https://github.com/TheOldManAndTheC/mvcTkinter

Then import whatever modules you need into your project. In keeping with normal Tkinter style, I use:

	import mvcTkinter as mtk

In your project you'll want to subclass `Controller`, `Model`, and `View`. 


## Controller

You can pass your `View` or `Model` objects to the `Controller` on creation with the `view` and `model` arguments, or you can set them after creation with `setView` and `setModel`. It is preferred to set up the `Controller` before setting up the `View` however, so the `View` will have a `Controller` to pass to widgets it creates.

In your `Controller` object you should override `valueForWidget` and `widgetUpdated` to allow the widgets in the `View` to request values or notiify the `Controller` that the widget has updated.

You should also override your `Controller`'s `dataForModel` and `modelUpdated` methods to allow the `Model` object to request data or notify the `Controller` that the model has changed.

## Model

You can pass your `Controller` object with the `controller` argument on creation, or set it with `setController` afterwards.

In your `Model` object you can override the `value` and `update` methods to allow the `Controller` to obtain model values or notify the model that it needs to update.

## View and widgets

In your `View` object you can use the widget classes in [`widgets`](widgets) to populate your UI using your `View` as the root `parent`. The widgets in [`widgets.base`](widgets/base) are subclasses of the default Tkinter widgets. The `View` itself is a subclass of the `Frame` widget.

Each widget you create (including the `View`) should have a unique `name`, and register itself to your `Controller` object either by passing the `Controller` object with the `controller` argument during creation, or using its `setController` method.

When creating widgets, you can use the normal Tkinter packing methods to arrange them, or you can also pass pack arguments to them on creation to have them pack automatically. These arguments are camel case concatenations of "pack" and the option name:

	tkPackOptions = {
	    "packAfter": "after",
	    "packAnchor": "anchor",
	    "packBefore": "before",
	    "packExpand": "expand",
	    "packFill": "fill",
	    "packIn": "in",
	    "packIpadx": "ipadx",
	    "packIpady": "ipady",
	    "packPadx": "padx",
	    "packPady": "pady",
	    "packSide": "side",
	}

If no pack options are passed, the widget will not pack automatically and must be packed normally.

A `subWidgets` argument can also be passed, which should contain a list of option dictionaries. Each option dictionary should be a set of keyword options for each child widget, with the addition of a `className` option with the name of a widget class. From each of these option dictionaries, a child widget will be created by the parent widget. This option can be used recursively to define complex widget layout trees using data structures.

If a `tooltip` argument is passed, a `Tooltip` object will be attached to the new widget with the text from the argument.

Once a widget is created, objects can register with the widget to recieve notifications with `registerObserver` and unregister with `unregisterObserver`. When the widget's `controller` is registered, it is automatically registered as an observer of the widget. Observers must implement the `widgetUpdated` method. Check [`core.constants.py`](core/constants.py) and the [widget sources](widgets) for notification keys.

The `Controller` can poll keyed values from widgets using their `value` method, and set the keyed values of widgets with the widget method `setValue`. The `Controller` can also set the state of widgets with `setState`, tell them to redraw with `refresh`, and tell them to fully reset and re-obtain all their values from the `Controller` with `reset`. Check [`core.constants.py`](core/constants.py) and the [widget sources](widgets) for value keys.

Note that while `BooleanVar`, `DoubleVar`, `IntVar`, `StringVar`, and `Variable` are included in `widgets.base`, they are not actually widgets and are included there to implement the MVC widget support that will allow them to communicate with the `Controller` object in the same way widgets do.

Look at [`core.MVCWidget.py`](core/MVCWidget.py) for more details on MVC widget functionality.

The communication methods in the sections above support keyword arguments to allow you to customize things to your needs.

## main

In your main module, after setting up your `Controller`, `Model`, and `View`, you can start the main UI loop with:

	controller.view().mainloop()

## Support

mvcTkinter is free open source software, but if you found it useful and you'd like to support me, you can send me a donation on [Ko-fi](https://ko-fi.com/theoldmanandthec).

## **TODO**:

Add glue code for remaining base widgets:  

- BitmapImage
- Canvas
- Combobox
- LabeledScale
- Labelframe
- Menu
- OptionMenu
- Panedwindow
- PhotoImage
- Progressbar
- Scale
- Separator
- Sizegrip
- Treeview

Create a sample project.

Write more detailed documentation.

## License

mvcTkinter copyright (c) 2023 The Old Man and the C

mvcTkinter is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

mvcTkinter is distributed in the hope that it will be useful,  but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License  for more details.

You should have received a copy of the GNU Affero General Public License along with mvcTkinter. If not, see <https://www.gnu.org/licenses/>.
