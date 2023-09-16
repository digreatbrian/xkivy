from kivy.uix.label import Label
from .layouts import LayoutUIXEffect
from kivy.properties import StringProperty ,ListProperty
from kivy.metrics import dp

class XLabel(LayoutUIXEffect,Label):
    halign = StringProperty('center')
    padding = ListProperty([dp(3) ,dp(3)])
    def __init__(self ,**kwargs):
        super().__init__(**kwargs)
        self.fbind('texture_size' ,self.update_label_size)
        
    def update_label_size(self , inst ,size):
        self.size_hint = [1, None]
        self.size = size
    
    def on_size(self ,inst,sz):
        x,y = sz
        self.text_size = x ,None
        
        



