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
		super(XImage,self).__init__(**kwargs)
		self.source=source
		if 'xbg_color' not in kwargs.keys():
			self.xbg_color=[1,1,1,1]
		
	def on_source(self,inst,src):
		if hasattr(self,'rect_instruction'):
			self.rect_instruction.source=src
			if self.rect_instruction.needs_redraw:
				self.redraw_canvas(src)
		else:
			def x(*_):
				self.rect_instruction.source=src
				
				if self.rect_instruction.needs_redraw:self.redraw_canvas(src)
				pass
			Clock.schedule_once(x)
			
	def redraw_canvas(self,source):
		canvas=self.canvas.before
		
		newcolor=Color(rgba=self.xbg_color)
		newrect=Rect(source=source,size=self.size,pos=self.pos)
		
		canvas.remove(self.rect_instruction)
		canvas.remove(self.color_instruction)
		
		self.color_instruction=newcolor
		self.rect_instruction=newrect
		
		canvas.add(newcolor)
		canvas.add(newrect)
		





