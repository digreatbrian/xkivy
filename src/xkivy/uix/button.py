from kivy.uix.button import Button
from kivy.metrics import dp
from ..effects.uixeffect import UIXEffect
from ..effects.clickeffect import (CircularRippleEffect,
				   RectangularRippleEffect,
				   TouchEffect
				   )
from kivy.properties import StringProperty


class XRectangularButton(UIXEffect, RectangularRippleEffect, TouchEffect, Button):
	halign = StringProperty('center')
	valign = StringProperty('center')
	def on_size(self ,instance ,sz): self.text_size = sz
	
class XCircularButton(UIXEffect, CircularRippleEffect, TouchEffect, Button):
	halign = StringProperty('center')
	valign = StringProperty('center')
	def on_size(self ,instance ,sz): self.text_size = sz

