from kivy.uix.popup import Popup
from ..effects.uixeffect import UIXEffect
from .scrollview import XScrollBoxLayout as XBoxScroll
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty


class InitError(Exception):
	pass

class XPopup(Popup,UIXEffect):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	
		
class XPlainPopup(ModalView,UIXEffect):
	is_open=BooleanProperty(False)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.overlay_color=self.xbg_color
		self.opacity=2
		def update_open(*_):
			self.is_open=True
			
		def update_dismiss(*_):
			self.is_open=False
			
		self.bind(on_open=update_open)
		self.bind(on_dismiss=update_dismiss)
		
	def on_open(self):
		pass
		
class XBoxPopup(XPlainPopup):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.init_popup()
		
	def on_parent(self,inst,par):
		if not hasattr(self,'initialised'):
			self.init_popup()
		
	def init_popup(self):
		self._container=XBoxScroll(orientation='vertical');super().add_widget(self._container)
		self.initialised=True
		
	def add_widget(self,wid):
		if not hasattr(self,'initialised'):
			raise InitError('Popup not initialised yet, use method init_popup.')
		self._container.add_widget(wid)
		
	def remove_widget(self,wid):
		if not hasattr(self,'initialised'):
			raise InitError('Popup not initialised yet, use method init_popup.')
		self._container.remove_widget(wid)
	
	def clear_widgets(self):
		if not hasattr(self,'initialised'):
			raise InitError('Popup not initialised yet, use method init_popup.')
		self._container.clear_widgets()
		
