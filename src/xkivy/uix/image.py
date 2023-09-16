#XImage
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import RoundedRectangle as Rect
from kivy.graphics.context_instructions import Color

# local import code here
from ..effects.uixeffect import UIXEffect

class XImage(UIXEffect,Widget):
	source=StringProperty('')
	def __init__(self,source='',**kwargs):
		super(XImage, self).__init__(**kwargs)
		self.source=source
		if 'xbg_color' not in kwargs.keys():
			self.xbg_color=[1,1,1,1]
		
	def on_source(self,inst,src):
		if hasattr(self,'rect_instruction'):
			self.rect_instruction.source = src
			Clock.schedule_once(lambda x:self.on_source(inst ,src))
		else:
			def x(*_):
				self.rect_instruction.source = src
				if self.rect_instruction.needs_redraw:
					self.on_source(inst ,src)
			Clock.schedule_once(x)
			
	


