from kivy.uix.popup import Popup
from .layouts import LayoutUIXEffect as LayoutEffect
from .layouts import XFloatLayout
from ..effects.uixeffect import CanvasAfterUIXEffect ,UIXEffect
from ..effects.shadoweffect import ShadowEffect
from .scrollview import XScrollBoxLayout as XBoxScroll
from .button import XCircularButton as XButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty ,OptionProperty ,NumericProperty
from kivy.uix.modalview import ModalView
from kivy.metrics import dp

class InitError(Exception):
    pass

class XPopup(UIXEffect, Popup):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    @property
    def is_open(self):
        return self._is_open

        
class XPlainPopup(ModalView, ShadowEffect, CanvasAfterUIXEffect):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #we use canvasafteruixeffect instead of just uixeffect because we want to draw in canvas.after rather canvas.before
    
    @property
    def is_open(self):
        return self._is_open
        
class XBoxPopup(XPlainPopup):
    orientation = OptionProperty('vertical',options=['vertical','horizontal'])
    spacing = NumericProperty(0)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_popup()
        
    def on_parent(self,inst,par):
        if not hasattr(self,'initialised'):
            self.init_popup()
            
    def on_spacing(self ,instance ,space):
        if not hasattr(self,'initialised'):
            self.init_popup()
        self._container.spacing=space
        
    def on_orientation(self ,instance ,orientation):
        if not hasattr(self,'initialised'):
            self.init_popup()
        self._container.orientation=orientation
        
    def init_popup(self):
        self._container=XBoxScroll(orientation=self.orientation,spacing = self.spacing)
        super().add_widget(self._container)
        self._container.size_hint=[.9,.9]
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
        
        
class XExitButtonBoxPopup(XPlainPopup):
    #it has the custom exit button to quit the popup
    orientation = OptionProperty('vertical',options=['vertical','horizontal'])
    spacing = NumericProperty(0)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_popup()
        
    def on_parent(self,inst,par):
        if not hasattr(self,'initialised'):
            self.init_popup()
            
    def on_spacing(self ,instance ,space):
        if not hasattr(self,'initialised'):
            self.init_popup()
        self._container.spacing=space
        
    def on_orientation(self ,instance ,orientation):
        if not hasattr(self,'initialised'):
            self.init_popup()
        self._container.orientation=orientation
        
    def init_popup(self):
        #exit button container
        self._exit_container = XFloatLayout()
        #exit button
        self._exit_button = XButton(text='X',size_hint=[.05 ,.05],color = [.7,.1,0,.6],xbg_color=[0]*4 ,pos_hint={'center_x':.95,'center_y':.95})
        self._exit_button.ripple_color= self._exit_button.color
        #main container
        self._container=XBoxScroll(orientation=self.orientation,spacing = self.spacing);
        self._container.size_hint=[.9,.85]
        #adding the exit button to its container
        self._exit_container.add_widget(self._exit_button)
        #adiing both containers
        super().add_widget(self._exit_container)
        super().add_widget(self._container)
        
        def exit_callback(instance):
            self.dismiss()
        self._exit_button.bind(on_release=exit_callback)
        
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
        




