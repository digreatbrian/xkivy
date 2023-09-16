from kivy.uix.scrollview import ScrollView
from kivy.properties import (StringProperty,NumericProperty,
VariableListProperty, ObjectProperty)
from kivy.clock import Clock
from kivy.metrics import dp
from ..effects.scrolleffect import StiffScrollEffect
from .layouts import XBoxLayout ,LayoutUIXEffect
from kivy.core.window  import Window
from platform import platform

class XScrollView(ScrollView):
    always_overscroll = False
    def __init__(self ,**kwargs):
        super().__init__(**kwargs)
        self.load_bar()
        
    def load_bar(self):
        if len(platform().split('android'))>1 or len(platform().split('mobile'))>1:
            #this means we are on an android or any kind of mobile phone
            return
        self.bar_margin = dp(3)
        self.bar_width = dp(8)
        self.scroll_type = ['bars' ,'content']
    
    def _do_touch_up(self ,*args):
        try:
            super()._do_touch_up(*args)
        except:pass
        
class XScrollBoxLayout(LayoutUIXEffect,XScrollView):
    """Widget which consists of scrollview and boxlayout .
    Please set the XScrollBoxLayout size_hint for best results.'''
    """
    orientation = StringProperty('vertical')
    spacing = NumericProperty(dp(0))
    def __init__(self,**kwargs):
        self._container=XBoxLayout(size_hint=[1,1])
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
        
        self._container.orientation=self.orientation
        self._container.spacing=self.spacing
        self._container.size_hint=[1,.8]
        
        super().add_widget(self._container)
        Clock.schedule_interval(self.update_cont_size ,.8)
        self.initialised = True
        
    def update_wid_size(self ,wid):
        def update(dt):
            if not hasattr(wid ,'shint'):
                wid.shint = wid.size_hint
            x_hint ,y_hint = wid.shint
            x ,y = self.size
            if x ==100 or y==100:
                 #default height ,hasnt updated yet
                 try:
                     Clock.schedule_once(lambda x:self.update_wid_size(wid))
                     return
                 except:pass
            if self._container.orientation == 'vertical':
                if y_hint:
                    wid.size_hint=[x_hint,None]
                    wid.height = y_hint*list(self.size)[1]
            else:
                if x_hint:
                    wid.size_hint=[None ,y_hint]
                    wid.width = x_hint*list(self.size)[0]
            self.update_cont_size()       
            def on_wid_size_hint(instance ,hint):
               x ,y = hint
               hint_x ,hint_y = wid.shint
               if x and x is not None :
                   hint_x = x
               if y and y is not None:
                   hint_y = y
               instance.shint = hint_x ,hint_y
               self.update_wid_size(instance)
               
            if not hasattr(wid ,'binded_update'):
                wid.binded_update = True
                wid.bind(size_hint = on_wid_size_hint)
                
        Clock.schedule_once(update)
        
    def update_cont_size(self,*r):
        def update(dt):
            width ,height= 0 ,0
            iter_stage = 0
            for widget in self._container.children:
               if self._container.orientation == 'vertical':
                   height += widget.height
                   width = self._container.width 
               else:
                   height = self._container.height
                   width += widget.width
               if iter_stage >= 0:
                   if self._container.orientation == 'vertical':
                       height += self._container.spacing
                   else:
                       width += self._container.spacing
               iter_stage += 1
            if self._container.orientation == 'vertical':
                xhint ,yhint =self._container.size_hint
                self._container.size_hint=[xhint ,None]
                self._container.height = height
            else:
                xhint ,yhint =self._container.size_hint
                self._container.size_hint=[None,yhint]
                self._container.width = width
        Clock.schedule_once(update)
        
    def add_widget(self,wid):
        self._xadd_widget(wid)
        
    def remove_widget(self,wid):
        self._xremove_widget(wid)
                
    def clear_widgets(self,):
        self._xclear_widgets()
                
    def _xadd_widget(self,wid):
        if not hasattr(self,"initialised"):
            self.prepare_scrollboxlayout()
        self.update_wid_size(wid)
        self._container.add_widget(wid)
        self.update_cont_size()
        
    def _xremove_widget(self,wid):
        if not hasattr(self,"initialised"):
            self.prepare_scrollboxlayout()
        self._container.remove_widget(wid)
        self.update_cont_size()
        
    def _xclear_widgets(self):
        if not hasattr(self,"initialised"):
            self.prepare_scrollboxlayout()
        self._container.clear_widgets()
        self.update_cont_size()



