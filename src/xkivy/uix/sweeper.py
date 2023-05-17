
#XSweeper

from kivy.clock import Clock
from kivy.properties import (StringProperty,
ObjectProperty,
NumericProperty,
ListProperty,
DictProperty,
BooleanProperty)
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.screenmanager import (FadeTransition,FallOutTransition,NoTransition,CardTransition,RiseInTransition,ShaderTransition,SlideTransition,SwapTransition,WipeTransition)


TRANSITIONS={'fade':FadeTransition,
'fall_out':FallOutTransition,
'none':NoTransition,
'card':CardTransition,
'rise_in':RiseInTransition,
'shader':ShaderTransition,
'slide':SlideTransition,
'swap':SwapTransition,
"wipe":WipeTransition
}

# local import code here
from ..colors import default
from .image import XImage
from ..effects.uixeffect import UIXEffect
from .layouts import XBoxLayout,XFloatLayout
from .button import XRectangularButton as XButton

class Dotter(XBoxLayout):
	#Dot Container for showing dots when the image changes
	dot_num=NumericProperty(1)
	dot_color=ListProperty(default)
	dot_size=NumericProperty(dp(15))
	dot_spacing=NumericProperty(dp(5))
	dots=ListProperty([])
	def __init__(self,dot_num=1,**kw):
		super(Dotter,self).__init__(**kw)
		self.dot_num=dot_num
		self.orientation='horizontal'
		self.spacing=self.dot_spacing
		self.size_hint=[None,None]
		
	def on_parent(self,inst,par):
		Clock.schedule_interval(self.adjust_size,.1)
		
	def adjust_size(self,*_):
		totalDotWidth=(self.dot_num*self.dot_size)+(self.dot_spacing*(self.dot_num-1))+((1/2)*self.dot_size)
		totalDotHeight=self.dot_size+((1/4)*self.dot_size)
		self.width=totalDotWidth
		self.height=totalDotHeight
		
		
	def on_dot_num(self,inst,num):
		if not self.canvas:
			Clock.schedule_once(self.load,1)
		else:
			self.load()
		
	def on_dot_size(self,inst,size):
		for x in self.children:
			x.size=[size]*2
	
	def on_dot_color(self,inst,cl):
		def on(*_):
			for x in self.dots:
				x.xbg_color=cl
		if not self.children:
			Clock.schedule_once(on,1)
		else:
			on()
		
	def on_dot_spacing(self,inst,sp):
		self.spacing=sp
		
	def on_parent(self,inst,par):
		Clock.schedule_once(self.load,1)
		
	def load(self,*_):
		try:self._load()
		except:pass
		
	def _load(self,*_):
		self.size_hint=[None,None]
		size=self.dot_size
		if len(self.children)>self.dot_num:
			#removing some dots
			ln=len(self.children)-self.dot_num
			for x in self.children[:ln]:
				self.remove_widget(x)
				self.width-=x.width
		if len(self.children)<self.dot_num:
			#adding some dots
			ln=self.dot_num-len(self.children)	
			for x in range(0,ln):
				dot=XBoxLayout(size_hint=[None,None],size=[self.dot_size]*2,xbg_color=self.dot_color,xradius=[5000]*4,pos_hint={"center_y":.5,"center_x":.5})
				self.add_widget(dot)
			totalDotWidth=(self.dot_num*self.dot_size)+(self.dot_spacing*(self.dot_num-1))+((1/2)*self.dot_size)
			totalDotHeight=self.dot_size+((1/4)*self.dot_size)
			self.width=totalDotWidth
			self.height=totalDotHeight
	
	def add_widget(self,wid):
		super(Dotter,self).add_widget(wid)
		self.dots.append(wid)
		
	def remove_widget(self,wid):
		super(Dotter,self).remove_widget(wid)
		self.dots.remove(wid)
		
	def clear_widgets(self):
		super(Dotter,self).clear_widgets()
		self.dots.clear()	
		
class SweeperItem(BoxLayout):
	img_src=StringProperty("")
	name=StringProperty('')
	xradius=ListProperty([0]*4)
	def __init__(self,img_src='',**kwargs):
		super(SweeperItem,self).__init__(**kwargs);self.img=XImage()
		if img_src:
			self.img_src=img_src
		
	def on_xradius(self,inst,rd):
		try:
			self.img.xradius=rd
		except:
			super(SweeperItem,self).__init__()
			self.on_xradius(inst,rd)
		
	def on_name(self,inst,nm):
		if self.parent:
			self.parent.name=nm
		
	def on_parent(self,inst,par):
		if par:
			try:self.add_widget(self.img)
			except:raise
		
	def on_img_src(self,inst,src):
		self.img.source=src

class SweeperButton(XButton):
	pass
	
class ScreenX(UIXEffect,Screen,):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.xbg_color=[0,0,0,0]
	
class ScreenManagerX(UIXEffect,ScreenManager,):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.xbg_color=[0,0,0,0]

class XSweeper(SweeperButton):
	'''::Key Attributes::
		data : Dict
		Info : Data of sweeper in form of {"name": {"image":image_source,"action": function/method ,"action_args":function/method args}} ,you can add as many sweeper items/screens in this way just extend the dictionary.
		
		dotter : Object 
		Info : Widget Object for managing dots attached to the sweeper
		
		switch_transition : String
		Info : String for manipulating the transition which will be used by the sweeper.
		
		switch_direction : String
		Info : String to set the direction that the sweeper will switch to when switching to new screen/image.
		
		switch_duration : Interger
		Info : The time taken in switching screens in seconds.
		
		dot_color : List [4 items]
		Info : The color of the dots applied on the sweeper.
		
		'''
	initialised=BooleanProperty(False)
	data=DictProperty({}) 
	#Data Format --> {"name":{"image" : "","action":func,"action_args":""}}
	_items=[] #items
	dotter=ObjectProperty()
	switch_direction=StringProperty('left')
	switch_transition=StringProperty('slide')
	switch_duration=NumericProperty(4)
	dot_color=ListProperty(default)
	xbg_color=ListProperty([0,0,0,0])
	def __init__(self,data={'':{}},**kwargs):
		super(XSweeper,self).__init__(**kwargs)
		self.data=data
		
	def on_switch_direction(self,inst,d):
		directions=["left","right"]
		if d.lower() not in directions:
			raise TypeError("Switch direction should be either right/left.")
			
	def on_switch_transition(self,inst,t):
		if t.lower() not in TRANSITIONS:
			raise TypeError("Transition should be one of %s ."%list(TRANSITIONS.keys()))
		
	def on_dot_color(self,inst,cl):
		self._dot_color=cl
		if self.dotter:
			self.dotter.dot_color=cl
		else:
			def retry(*_):
				self.on_dot_color(self,cl)
				
			Clock.schedule_once(retry,1)
		
	def on_click_release(self,*args):
		'''Function Fired whenever the sweeper is released after a press.'''
		data=self.data
		def onclick(*_):
			crnt=self.screenmanager.current
			action=data.get(crnt)
			args=data.get(crnt)
			if action:
				action=action.get('action')
			if args:
				args=args.get('args')
			######
			if not args:
				args=()
			if action:
				try:
					action(*args)
				except: raise
		onclick()
		
	def on_xradius(self,inst,rd):
		super(XSweeper,self).on_xradius(inst,rd)
		def load(*_):
			for x in self._items:
				x.item.xradius=rd
			if hasattr(self,"screenmanager"):
				self.screenmanager.xradius=rd
				for i in self.screenmanager.children:i.xradius=rd
				
		def load_and_init(*_):
			self.init_sweeper()
			load()
			
		if not self.initialised:
			try:self.init_sweeper()
			except:Clock.schedule_once(load_and_init,1)
		else:
			load()
		
	def on_data(self,inst,dat):
		#for every name in data
		def load(*_):
			self.dotter.dot_num=len(dat.keys())
			self.clear_widgets()
			self._items.clear()
			self.dotter.pos_hint={"center_x":.5,'center_y':.1}
			for name in dat.keys():
				options=dat['{}'.format(name)] #dict
				if "image" not in options.keys() or 'action' not in options.keys() or 'args' not in options.keys():
					#raise TypeError("Data should be in JSON-like format with keys ['image','action','args'] .Eg data={'name':{'image':'test.png','action':testfunc,'args':(1,'teststring')}} ")
					pass
				img_src=options.get('image')
				action=options.get("action")
				s=ScreenX(name=name)
				s.item=SweeperItem(img_src)
				if hasattr(self,"xradius"):
					s.item.xradius=self.xradius
				s.add_widget(s.item)
				self.add_widget(s)
				if s not in self._items:
					self._items.append(s)
		
		def load_and_init(*_):
			self.init_sweeper()
			load()
			
		if not self.initialised:
			try:self.init_sweeper();load()
			except:Clock.schedule_once(load_and_init,1)
		else:
			load()
		
	def on_initialised(self,*_):
		if not hasattr(self,"_initialised_"):
			raise TypeError("Could not set read-only attribute 'initialised' ")
			
	def on_parent(self,*_):
		Clock.schedule_once(self.init_sweeper,.5)
		
	def start_sweeper_effect(self):
		'''Start the sweeper effect of switching images/windows.'''
		def start(*_):
			def st():
				ch=self._items
				crnt_scrn=self.screenmanager.current_screen
				crnt_index=ch.index(crnt_scrn)
				targ_index=crnt_index+1
				if targ_index>=len(ch):
					targ_index=0
				targ_screen=ch[targ_index]
				if self.switch_duration>=2:
					duration=1
				if self.switch_duration<2:
					duration=self.switch_duration
				self.on_switch_transition(self,self.switch_transition)
				self.screenmanager.switch_to(targ_screen,duration=duration,direction=self.switch_direction,transition=TRANSITIONS.get(self.switch_transition)())
				#targetting Dotter
				dt=self.dotter
				dots=[]
				for t in dt.dots:
					dots.append(t)
				crntx=crnt_index
				for x in dots:
					if dots.index(x)==crntx:
						x.xbg_color=self.dot_color
						#setting real bg_color to switch-dots
					else:
						#blending white color to other dots by reducing opacity
						rx=list(self.dot_color)
						opacity=rx.pop()
						reduction=(1/2)*opacity
						opacity-=reduction
						rx.append(opacity)
						x.xbg_color=rx
			try:st()
			except:pass
		Clock.schedule_interval(start,self.switch_duration)
					
		
	def on_size(self,inst,sz):
		if not self.initialised:
			try:self.init_sweeper()
			except:
				Clock.schedule_once(self.init_sweeper,1)
				def onsize(*_):
					self.on_size(inst,sz)
				Clock.schedule_once(onsize,1)
				return
		self.floatlayoutcont.size=sz
		self.screenmanager.size=sz
			
	def on_pos(self,inst,pos):
		if not self.initialised:
			try:self.init_sweeper()
			except:
				Clock.schedule_once(self.init_sweeper,1)
				def onpos(*_):
					self.on_pos(inst,pos)
				Clock.schedule_once(onpos,1)
				return
		self.floatlayoutcont.pos=pos
		self.screenmanager.pos=pos
		
	def init_sweeper(self,*args):
		'''Base method to initialise the sweeper.'''
		#adding screenmanager to floatlayout and adding floatlayout to self
		#all sweeper items will be added directly to screenmanager by method "add_widget" within this class
		#Dotter is going to be added to floatlayout
		if not self.initialised:
			floatlayout=FloatLayout()
			#floatlayout.size=self.size
			sm=ScreenManagerX()
			self.dotter=Dotter(pos_hint={'center_x':.5,'center_y':.1})
			
			floatlayout.add_widget(sm)
			super(XSweeper,self).add_widget(floatlayout)
			
			self.screenmanager=sm
			self.floatlayoutcont=floatlayout
			
			floatlayout.add_widget(self.dotter)
			self._initialised_=True
			self.initialised=True
			self.start_sweeper_effect()
			self.fbind('on_release',self.on_click_release)
			self.xbg_color=(0,0,0,0)
		
	def add_widget(self,wid):
		if self.initialised:
			self.screenmanager.add_widget(wid)
			if wid not in self._items:
				self._items.append(wid)
		else:
			raise TypeError('XSweeper is not initialised use method "init_sweeper" for manual initialisation ')
		
	def remove_widget(self,wid):
		if self.initialised:
			self.screenmanager.remove_widget(wid)
			self._items.remove(wid)
		else:
			raise TypeError('XSweeper is not initialised use method "init_sweeper" for manual initialisation ')
			
	def clear_widgets(self):
		try:
			for x in self.screenmanager.children:self.remove_widget(x)
		except:
			pass

