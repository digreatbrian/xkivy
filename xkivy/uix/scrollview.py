from kivy.uix.scrollview import ScrollView
from .layouts import XBoxLayout
from ..effects.scrolleffect import StiffScrollEffect
from kivy.properties import StringProperty,NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp

class XScrollView(ScrollView):
	effect_cls=StiffScrollEffect
		
class XScrollBoxLayout(XScrollView):
	orientation=StringProperty('vertical')
	spacing=NumericProperty(dp(0))
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_orientation(self,inst,o):
		if not hasattr(self,'initialised'):
			self.prepare_scrollboxlayout()
		self._container.orientation=o
		
	def on_spacing(self,inst,s):
		if not hasattr(self,'initialised'):
			self.prepare_scrollboxlayout()
		self._container.spacing=s
		
	def on_parent(self,*_):
		self.prepare_scrollboxlayout()
		
	def prepare_scrollboxlayout(self,*_):
		if hasattr(self,'initialised'):
			if self.initialised==True:return
		self._container=XBoxLayout()
		self._container.orientation=self.orientation
		self._container.spacing=self.spacing
		self._container.size_hint=[1,1]
		
		super().add_widget(self._container)
		
		self.initialised=True
		
		Clock.schedule_interval(self.update_cont_size,.1)
		
	def update_wid_size(self,wid):
		if self.width==100 or self.height==100:
			def x(delta):
				self.update_wid_size(wid)
			Clock.schedule_once(x)
			return
		####################
		x_hint,y_hint=wid.size_hint
		if x_hint is not None:
			width=x_hint*self.width
		else:
			width=wid.width
			
		if y_hint is not None:
			height=y_hint*self.height
		else:
			height=wid.height
		wid.size_hint=[None,None]
		wid.size=[width,height]
			
	def update_cont_size(self,*_):
		if not hasattr(self,"initialised"):
			self.prepare_scrollboxlayout()
		if self.width==100 or self.height==100:
			def x(delta):
				self.update_cont_size()
			Clock.schedule_once(x)
			return
		width,height=0,0
		if not self._container.children:
			self._container.size_hint=[None,None];self._container.size=[width,height]
			return
		if self._container.orientation=='vertical':
			width=self._container.children[0].width
			for x in self._container.children:
				height+=x.height
				height+=self._container.spacing
			height-=self._container.spacing
			
		else:
			height=self._container.children[0].height
			for x in self._container.children:
				width+=x.width
				width+=self._container.spacing
			width-=self._container.spacing
		
		self._container.size_hint=[None,None]
		self._container.size=[width,height]
		
	def add_widget(self,wid):
		if not hasattr(self,"initialised"):
			self.prepare_scrollboxlayout()
		self._container.add_widget(wid)
		self.update_wid_size(wid)
		self.update_cont_size()
		
		def update_wid_size(*_):
			self.update_wid_size(wid)
			
		wid.fbind('size',update_wid_size)
		wid.fbind('size_hint',update_wid_size)
		wid.bind(on_size=update_wid_size)
		wid.bind(on_size_hint=update_wid_size)
		
	def remove_widget(self,wid):
		if not hasattr(self,"initialised"):
			self.prepare_scrollboxlayout()
		self._container.remove_widget(wid)
		
	def clear_widgets(self):
		if not hasattr(self,"initialised"):
			self.prepare_scrollboxlayout()
		self._container.clear_widgets()
		