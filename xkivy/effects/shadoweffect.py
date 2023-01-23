from kivy.properties import ListProperty,NumericProperty
from kivymd.uix.behaviors.elevation import CommonElevationBehavior as CommonElevation

class ShadowEffect(CommonElevation):
	shadow_color=ListProperty([0,0,0,1])
	shadow_size=NumericProperty(3)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.on_shadow_size(self,self.shadow_size)
		self.fbind('xradius',self.on_sh_radius)
		
	def on_shadow_size(self,inst,sz):
		self.elevation=sz
		
	def on_sh_radius(self,inst,rd):
		self.shadow_radius=rd
	
			