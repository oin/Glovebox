Glovebox is an experimental improvised music environment.

# Introduction

Glovebox is an experimental improvised music environment. It allows you to augment found physical objects with virtual behaviors, some of which can (eventually) produce music. It works using a webcam and preferably a laptop : it analyses the image of the webcam in order to see which different physical objects are present, and displays their augmentations both on the screen and on the speakers. This is somehow an augmented reality application. However, Glovebox is a tangible interface, ie. you don't need any mouse or keyboard to use it, because all you have to do is to manipulate the engaged objects.

Glovebox is made to be fully and easily extensible. It is composed of a C++ module containing the core functions for sound (thanks to [libpd](https://github.com/libpd)), camera input and fiducial tracking (thanks to [ARToolKitPlus](https://code.launchpad.net/artoolkitplus)), a Python package containing the main application logic, and a `behaviors` directory with some conventions allowing you to extend the software by adding virtual behaviors using the Python programming language and Puredata. Because the software uses the wonderful [cocos2d](http://www.cocos2d.org) library, there is also an interactive Python shell, so you can tweak things on the fly while you're playing. Remember, Glovebox is **experimental**.

## Related work

This environment is inspired from previous works about improvised interfaces[1], which are tangible interfaces where the primary means of interaction is found objects. This kind of interaction isn't easy to design because nobody knows which objects (either the physical ones or the virtual parts) will be used until they are used.

## Why ?

Improvised interfaces represent a significant opportunity for creativity-driven uses like musical performance : while computer interfaces are generally not compatible with unintended uses, improvised interfaces generalize them and allow users to adapt them to their immediate requirements. Moreover, the ever-changing nature of these interfaces make it extra easy to rearrange musical controls and structures on the fly.

## Limitations

I didn't aim to develop a full fledged improvised interface : Glovebox has some serious limitations. As you probably don't own a head-mounted display, you won't be able to move freely in your physical environment, so you're limited to a fixed place. Glovebox is also limited to one computer, whereas you may want to play with your friends in the same room, but in a networked setting, being able to pass a physical object, along with its attached behavior, from hand to hand.

## Important notice

**Beware** ! Glovebox is an *experimental-quality* software. This means it is designed to work on my machine for my requirements, but it can possibly blow on your machine. Don't expect everything to work seamlessly. You can also find the source code smells a lot : again, it is _experimental-quality_ software, so it is very far from a stable, elegant and fully working release. However, the source code is under a GPL license, so feel free to fork and reuse anything if you want something this project doesn't provide (eg. stability).

This project has been released to facilitate experimentation with tangible AR interfaces, and especially improvised interfaces. It can also be used by artists or adventurous tinkerers. The fact it runs with Python ensures you can interface it with the Twitter API or your coffee brewer.

# How to use Glovebox

For now, Glovebox only works on fairly recent (>= 2007-2008) Mac OS X Intel machines. It has been tested on Lion and Snow Leopard. You can download the last compiled version in [GitHub](https://github.com/oin/Glovebox/downloads) or in the [official site](http://glovebox.oin.name).

## Preparation

For Glovebox to be able to identify and track a physical object, you have to stick a fiducial marker to it. A fiducial marker is a little (or big, as you want) image encoding an identifier. They are a cheap way to make the computer recognize and track physical objects over time. You can produce fiducial markers easily by printing some of them on sheets. Then, cut a marker out of your sheet and fix it to an object you like with adhesive putty. Find a bunch of objects you like and you're ready to go.

## Setting

You can use Glovebox in a _mirrored augmented-reality_ setting : your screen is in front of you and the webcam is directed towards you. This is a simple way to try out things.

However, the most pleasant way to use Glovebox is with a laptop and the _glovebox_(TM) setting (hence the name) : your screen is in front of you, your webcam is directed towards what is behind your screen, and your hands and objects are behind the screen, the arms lying on each side of your screen. You can watch the screen as if it was a window to the real-virtual world. Yeah, with [real gloveboxes](http://www.google.com/search?q=glovebox&tbm=isch), the hands aren't on the side, but that's the closest image I could find. OK, stop bugging me now !

If you find another comfortable way to use Glovebox (aside from _not_ using it), feel free to tell me about it.

## Building

Once you've got tagged physical objects and you're well installed, you can present your objects to Glovebox and attach virtual behaviors to them. A behavior defines a special kind of augmentation of a physical object. It responds to movements of the physical object and to actions from other behaviors. For instance, the **Maracas** behavior turns any object into a lovely latin music instrument. Physical objects can also interact through their behaviors and their relationships. For instance, the sound of a maracas object can be redirected to an object embodying an echo effect.

In order to attach a behavior to a tracked object, shake it several times until a radial menu appears. The shaking gesture may be hard to master the first time (however, it can be parameterized with some Python lines). Once the menu appears, move your object towards a menu item to select it. Keeping it still on a menu item will activate the item.

## Playing

Behaviors can be very different, so there is no rationale. Moreover, you are likely to add your own behaviors and follow your own conventions. Just remember that shaking an object is a standard technique in Glovebox.

### Modular synthesis

I implemented a tiny set of behaviors to mimic a modular synthesis environment, following [1]. Some behaviors are **Sources**, they can produce sound and their sound can be redirected (using an **AlphaObject**) to behaviors called **Effects** (or FX). An effect is also a source, so its sound can also be redirected. The sound is directed to the speakers by default. **Controllers** are the way to modify parameters of objects (like the frequency of a synthesizer) : you create a controller, then you associate it to an existing source (be it an actual source or an effect), and you can play. In [1], there were also **Tools**, but tools really happen to be any other kind of behavior.

## Webcam performance

For maximum performance, I advise you to get a PS3 Eye webcam. It is cheap and fast enough. To use it on Mac OS X, install [Macam](http://webcam-osx.sourceforge.net), and preferrably a [tweaked version provided by cool people on the openFrameworks forums](http://forum.openframeworks.cc/index.php?topic=1182.225).

# How to extend Glovebox

In the `behaviors` directory (accessible by using the Glovebox application menu), you can easily create new behaviors with Python 2.7. Look at the existing behaviors in order to grasp how it works.

You have to follow a rather strict convention, eg. for an extension called FooBar :

- the extension must be somewhere in the `behaviors` directory (on in a subdirectory)
- the directory must be called `foo_bar`
- inside the directory, there must be a file called `foo_bar.py`
- inside this Python module, the class FooBarBehavior must be defined as a subclass of glovebox.play.Behavior.Behavior, and there must be the following global variables :
	* `behavior_name` : a string containing the display name of the behavior
	* `behavior_description` : a string containing a quick description of the behavior
	* `behavior_menu` : a list containing the menu path to access the extension when you want to attach it to a tracked object

You can create Puredata patches and load them from your behavior. However, remember that as Glovebox uses an embedded version on Puredata, only the *vanilla* abstractions are usable (no `expr`, for instance).

## Resources

If you feel lost, even after watching the existing code base, I advise you to check these resources :

### Python 2.7

* [Official site](http://www.python.org)
* [Dive into Python](http://www.diveintopython.net)
* [Python documentation](http://docs.python.org)

### Puredata

* [Official site](http://puredata.info)

# How to build Glovebox

If you want to tinker with the C++ extension or aren't satisfied with how the binary works, you can build Glovebox from the source.

## Requirements

### C++ extension

* [Python 2.7](http://www.python.org)
* [CMake](http://www.cmake.org)
* [Boost 1.48.0](http://www.boost.org)
* [Portaudio v19](http://www.portaudio.com)
* OpenGL (it's in your system)

ARToolKitPlus 2.2.1 and a recent libpd version are included and statically compiled.

### Python part

* [cocos2d](http://www.cocos2d.org)
* [pyglet](http://www.pyglet.org)

## On Mac OS X

### Notes

You obviously need a recent version of the Apple Developer tools (Xcode) to get a C++ compiler.

As I use a legacy QuickTime component for the webcam (because Macam doesn't work well with QTKit or AVFoundation), you have to get all your binary dependencies compiled in 32 bit.

On Lion, you will have to set the `CMAKE_OSX_SYSROOT` CMake variable to `/Developer/SDKs/MacOSX10.6.sdk`.

In the Glovebox root folder :

	$ cd libglovebox
	$ mkdir build
	$ cd build
	$ cmake ..

If you have to tinker with some environment variables, like the Python path or the SDK, using `ccmake` instead of `cmake` makes it easier.

	$ make
	$ cd ../..
	$ make

You can then eventually modify the Python source code, and run Glovebox with this command :

	$ python Glovebox.py

# References

[1] J. Aceituno, J. Castet, M. Desainte-Catherine, and M. Hachet. Improvised interfaces for real-time musical applications. In Proceedings of the sixth international conference on tangible, embedded and embodied interaction (TEI), 2012.