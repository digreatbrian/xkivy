from kivy.uix.button import Button
from kivy.metrics import dp
from ..effects.uixeffect import UIXEffect
from ..effects.clickeffect import (CircularRippleEffect,RectangularRippleEffect,
TouchEffect)


class XRectangularButton(UIXEffect,RectangularRippleEffect,TouchEffect,Button):
	pass
	
class XCircularButton(UIXEffect,CircularRippleEffect,TouchEffect,Button):
	pass
