Glovebox is an experimental improvised music environment.

# Introduction

Glovebox is an experimental improvised music environment. It allows you to augment found physical objects with virtual behaviors, some of which can (eventually) produce music. It works using a webcam and preferably a laptop : it analyses the image of the webcam in order to see which different physical objects are present, and displays their augmentations both on the screen and on the speakers. This is somehow an augmented reality application. However, Glovebox is a tangible interface, ie. you don't need any mouse or keyboard to use it, because all you have to do is to manipulate the engaged objects.

## Related work

This environment is inspired from previous works about improvised interfaces[1], which are tangible interfaces where the primary means of interaction is found objects. This kind of interaction isn't easy to design because nobody knows which objects (either the physical ones or the virtual parts) will be used until they are used.

## Why ?

Improvised interfaces represent a significant opportunity for creativity-driven uses like musical performance : while computer interfaces are generally not compatible with unintended uses, improvised interfaces generalize them and allow users to adapt them to their immediate requirements. Moreover, the ever-changing nature of these interfaces make it extra easy to rearrange musical controls and structures on the fly.

## Limitations

I didn't aim to develop a full fledged improvised interface : Glovebox has some serious limitations. As you probably don't own a head-mounted display, you won't be able to move freely in your physical environment, so you're limited to a fixed place. Glovebox is also limited to one computer, whereas you may want to play with your friends in the same room, but in a networked setting, being able to pass a physical object, along with its attached behavior, from hand to hand.

# How to use Glovebox

## Preparation

For Glovebox to be able to identify and track a physical object, you have to stick a fiducial marker to it. A fiducial marker is a little (or big, as you want) image encoding an identifier. They are a cheap way to make the computer recognize and track physical objects over time. You can produce fiducial markers easily by printing some of them on sheets. Then, cut a marker out of your sheet and fix it to an object you like with adhesive putty. Find a bunch of objects you like and you're ready to go.

## Setting

You can use Glovebox in a _mirrored augmented-reality_ setting : your screen is in front of you and the webcam is directed towards you. This is a simple way to try out things.

However, the most pleasant way to use Glovebox is with a laptop and the _glovebox_(TM) setting (hence the name) : your screen is in front of you, your webcam is directed towards what is behind your screen, and your hands and objects are behind the screen, the arms lying on each side of your screen. You can watch the screen as if it was a window to the real-virtual world. Yeah, with [real gloveboxes](http://www.google.com/search?q=glovebox&tbm=isch), the hands aren't on the side, but that's the closest image I could find. OK, stop bugging me now !

If you find another comfortable way to use Glovebox (aside from _not_ using it), feel free to tell me about it.

## Building

Once you've got tagged physical objects and you're well installed, you can present your objects to Glovebox and attach virtual behaviors to them. A behavior defines a special kind of augmentation of a physical object. It responds to movements of the physical object and to actions from other behaviors. For instance, the **Maracas** behavior turns any object into a lovely latin music instrument. Physical objects can also interact through their behaviors and their relationships. For instance, the sound of a maracas object can be redirected to an object embodying an echo effect.

In order to attach a behavior to a tracked object, shake it several times until a radial menu appears. The shaking gesture may be hard to master the first time. However, it can be fully parameterized, as everything in Glovebox.



# References

[1] J. Aceituno, J. Castet, M. Desainte-Catherine, and M. Hachet. Improvised interfaces for real-time musical applications. In Proceedings of the sixth international conference on tangible, embedded and embodied interaction (TEI), 2012.