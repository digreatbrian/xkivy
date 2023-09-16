
"""Create a Flexible DropDown .

Example::
	from kivy.app import App
	from xkivy.uix.dropdown import XDropDown
	
	class TestDropDown(XDropDown):
		def __init__(**kwargs):
			self.spacing=10
			self.xfg_color=[1,1,1,1]
			self.xradius=[1,1,1,1]
			self.values=["python","java","c"]
			
		def on_option_release(self,instance):
			print(instance.text)
			
	class MyApp(App):
		def build(self):
			return TestDropDown()
			
	MyApp().run()
	
"""

from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner ,SpinnerOption
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
	ListProperty,
	NumericProperty,
	ObjectProperty,
	ColorProperty)

from ..effects.uixeffect import UIXEffect
from ..effects.clickeffect import (
	RectangularRippleEffect,
	TouchEffect
	)

from functools import partial

class OptionCls(UIXEffect,RectangularRippleEffect,
TouchEffect,SpinnerOption):
	caller=ObjectProperty()
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.xradius=[dp(22)]*4
	
	def on_caller(self,inst,c):
		self.on_release=partial(c.on_option_release,self)

class DropDownCls(UIXEffect,DropDown):
	spacing=NumericProperty(None)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.xbg_color=(0,0,0,0)
		self.bar_color=self.xbg_color
		
	def on_spacing(self,inst,sp):
		if self.container:
			self.container.spacing=sp
		else:
			def schedule(*_):
				self.on_spacing(inst,sp)
			Clock.schedule_once(schedule)
		
class XDropDown(UIXEffect,RectangularRippleEffect,
TouchEffect,Spinner):
	'''Some Key Attributes::
		option_xbg_color : Set every option background color
		option_fg_color : Set every option text color
		option_widgets : Use it for readonly purposes only ,used to get the options as widgets.
		spacing : Set the DropDown spacing.
		xfg_color : Set DropDown text color.
		
		'''
	option_xbg_color=ColorProperty(None)
	option_xfg_color=ColorProperty(None)
	option_widgets=ListProperty([])
	values= ListProperty([])
	spacing=NumericProperty(None)
	xfg_color=ColorProperty(None)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.dropdown_cls=DropDownCls
		self.option_cls=OptionCls
		self.spacing=dp(2)
		Clock.schedule_once(self._set_option_caller)
		def update_option_wids(*_):
			dropdown_container=self._dropdown.container
			if  dropdown_container:
				for x in dropdown_container.children:
					if x not in self.option_widgets:
						self.option_widgets.append(x)
				for x in self.option_widgets:
					if x not in dropdown_container.children:self.option_widgets.remove(x)
		Clock.schedule_interval(update_option_wids,.1)
		def chk(inst,wids):
			for x in wids:
				if x.text=="$Spacing$":
					x.size_hint=[1,None]
					x.height=self.spacing
					x.xradius=[1]*4
					x.font_size=0
					x.color = [0,0,0,0]
					x.disabled=True
					x.on_xbg_color(inst,[0,0,0,0])
					
		self.bind(option_widgets = chk )
		
	def on_option_widgets(self,inst,children):pass
		
	def _set_option_caller(self,*_):
		#only to be called once for setting options caller
		def set(*_):
			dropdown_container=self._dropdown.container
			if dropdown_container:
				ch=dropdown_container.children
				for x in ch:
					if not x.caller:
						x.caller=self
		Clock.schedule_interval(set,.1)
		
	def on_option_release(self,option_obj):
		'''Called after a release on option.'''
		
	def on_xfg_color(self,inst,cl):
		"""Used to change dropdown text color."""
		self.color=cl
		
	def on_option_xfg_color(self,inst,cl):
		"""Used to change options text color."""
		dropdown_container=self._dropdown.container
		if not dropdown_container:
			def s(*_):
				self.on_option_xfg_color(inst,rd)
			Clock.schedule_once(s)
			return
		childs=dropdown_container.children
		for x in childs:
			x.color=cl
		self.option_cls.color=cl
		
	def on_xradius(self,inst,rd):
		"""Used to change dropdown radius."""
		dropdown_container=self._dropdown.container
		if not dropdown_container:
			def s(*_):
				self.on_xradius(inst,rd)
			Clock.schedule_once(s)
			return
		childs=dropdown_container.children
		for x in childs:
			x.xradius=rd
		self.option_cls.xradius=rd
		
	def on_spacing(self,inst,sp):
		"""Used to change dropdown spacing."""
		self._dropdown.spacing=sp
		self.dropdown_cls.spacing=sp
		
	def on_option_xbg_color(self,inst,cl):
		"""Used to change options background color ."""
		dropdown_container=self._dropdown.container
		if not dropdown_container:
			def s(*_):
				self.on_option_xbg_color(inst,rd)
			Clock.schedule_once(s)
			return
		childs=dropdown_container.children
		for x in childs:
			x.xbg_color=cl
		self.option_cls.xbg_color=cl
	

