from kivy.properties import ColorProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# local import code here
from ..effects.uixeffect import UIXEffect

class LayoutUIXEffect(UIXEffect):
	xbg_color=ColorProperty([0,0,0,0])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
class XBoxLayout(LayoutUIXEffect,BoxLayout):
	pass

class XFloatLayout(LayoutUIXEffect,FloatLayout,):
	pass
	
class XGridLayout(LayoutUIXEffect,GridLayout,):
	pass
	



