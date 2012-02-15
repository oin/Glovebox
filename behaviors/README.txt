You are in the Glovebox `behaviors` folder. Here you can edit and create additional behaviors using the Python programming language (http://www.python.org) and the Puredata environment (http://puredata.info). This file is meant as a (veeeeeery short) guide to dive in and make Glovebox grow.

Look at the existing behaviors in order to grasp how it works.

You have to follow a rather strict convention, eg. for an extension called FooBar :

- the extension must be somewhere in the `behaviors` directory (on in a subdirectory)
- the directory must be called `foo_bar`
- inside the directory, there must be a file called `foo_bar.py`
- inside this Python module, the class FooBarBehavior must be defined as a subclass of glovebox.play.Behavior.Behavior, and there must be the following global variables :
	* `behavior_name` : a string containing the display name of the behavior
	* `behavior_description` : a string containing a quick description of the behavior
	* `behavior_menu` : a list containing the menu path to access the extension when you want to attach it to a tracked object

You can create Puredata patches and load them from your behavior. However, remember that as Glovebox uses an embedded version on Puredata, only the *vanilla* abstractions are usable (no `expr`, for instance).