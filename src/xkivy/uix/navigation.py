from kivy.graphics import Rectangle
from ..utils.touchmanager import TouchManager
from ..uix.screenmanager import XScreen
from ..effects.shadoweffect import ShadowEffect

from .layouts import (
    XBoxLayout
	)
from ..colors import default

from kivy.properties import BoundedNumericProperty as BoundProperty
from kivy.properties import (
	ObjectProperty,
	NumericProperty,
	BooleanProperty,
	OptionProperty,
	StringProperty,
	ListProperty
	)
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

from math import radians
from kivy.vector import Vector
from kivy.graphics.transformation import Matrix


class XDrawer(ShadowEffect ,XBoxLayout):
	xbg_color = ListProperty(default)
	size_hint = [1 ,1]
	

class XNavigationManager(TouchManager ,XScreen):
	"""
	Navigation Manager Widget
	
	Example::
		
		from xkivy.uix.navigation import XNavigationManager
		from xkivy.uix.button import XRectangleButton as XButton
		
		nav= XNavigationManager()
		btn= XButton(text="hie")
		btn2=XButton(text="good")
		
		nav.add_widget(btn)
		nav.drawer_add_widget(btn2)
		
	
	Some attributes
	
	drawer : Drawer Object Instance
	open_hint : Drawer Size Hint
	drawer_state : The state of the drawer which includes [open,opening,closed,closing] ,it is updated automatically.
	anim_running : bool on either if there is an opening drawer/closing drawer animation running or not.
	start_open : Position x that you will allow for drawer to start to open.
	black_opacity : The dark color applied to NavigationManager when opening/closing drawer.
	close_on_click : Close on click event outside the drawer.
	
	"""
	drawer=ObjectProperty(XDrawer())
	_scatter=ObjectProperty(Scatter())
	open_hint=BoundProperty(.8,min=.3,max=.9)
	drawer_state=OptionProperty("closed",options=["open","opening","closed","closing"])
	anim_running=BooleanProperty(False)
	start_open=NumericProperty(dp(7))
	black_opacity=BoundProperty(1,min=0,max=1)
	close_on_click=BooleanProperty(True)
	opening_anim=StringProperty("linear")
	closing_anim=StringProperty("linear")
	opening_anim_time=NumericProperty(.45)
	closing_anim_time=NumericProperty(.45)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.prepare_nav ,1)
		
	def on_black_opacity(self,inst,op):
		if not self.drawer.parent:
			def repeat_func(*_):
				self.on_black_opacity(inst,op)
			Clock.schedule_once(repeat_func)
			return
		self.xbg_color = [0,0,0,op]
		
	def on_open_hint(self,inst,h):
		"""Event called to ajust drawer size hint ."""
		self.drawer.width = self.width * h

	def on_touch_start(self ,touch):
		self.tdown_pos = touch.pos
		if self.drawer_state == 'open' or self.drawer_state == 'opening':
				if self.collide_point(*touch.pos):
						if not self.drawer.collide_point(*touch.pos):
							if self.close_on_click:
									self.close_drawer()
					
					
	def on_drawer_progress(self,*a):
		drx,dry = self._scatter.pos
		px = drx + self.drawer.width
		op = px/self.width
		
		if op < 0:op=0
		
		elif op > 1:op=1
		
		if (op > 411):
			op -= .411

		if op < 0:
			op = 0

		if op == self.open_hint:
			self.disabled = True
		else:
			self.disabled = False

		self.on_black_opacity(self ,op)
		self.manage_drawer_state()

	def on_size(self ,inst ,value):
		if value == 100:
			Clock.schedule_once(lambda x :self.on_size)
			return
		x ,y = value
		self.drawer.height = y
		self.drawer.width = self.width * self.open_hint
		self._scatter.pos = -self.drawer.width ,list(self._scatter.pos)[1]
		
	def on_swipe_right(self,touch):
		"""Swipe Right Event ."""
		x,y=self._scatter.pos
		if list(self.tdown_pos)[0] <= self.start_open:
				#we allow user to open drawer
				#coz he is swiping from the right bounds we know his intentions
				#we dont want mistaken actions
				self.open_drawer()
		else:
			return
			
	def on_swipe_left(self,touch):
		"""Swipe Left Event ."""
		self.close_drawer()
					
	def on_touch_stop(self,touch):
		"""Event called on drawer touch stop."""
		def f(*_):
			dposx,dposy = self._scatter.pos
			dposx = dposx + self.drawer.width
			center_posx = self.width/2
			def _round(nm:int):
				#rounding number to the whole number
				return round(nm + 1 ,- (len(str(int(nm))) - 1))
			if dposx < center_posx and _round(dposx) < _round(self.width * self.open_hint) :
				if not self.anim_running:
					self.close_drawer()
			else:
				if not self.anim_running:
					self.open_drawer()
		
		# do a little delay
		Clock.schedule_once(f)

	def prepare_nav(self,*_):
		"""Method for first initialisation."""
		def manage(*__none__):
			if self.drawer.width == 100:
				#sizes not updated yet
				return
			#else
			#self.manage_drawer_state()
			if not hasattr(self,"window"):
				self.manage_window()
				
		if not hasattr(self,"initialised_nav"):
			def on_scatter_touch_down(touch):
				self._scatter.super_on_touch_down(touch)
				self._scatter.canvas.after.add(Rectangle(size=(0 ,0) ,opacity=0))
				
			self._scatter.add_widget(self.drawer)
			self._scatter.do_translation_y = False
			self._scatter.transform_with_touch = self.scatter_transform_with_touch
			self._scatter.super_on_touch_move = self._scatter.on_touch_move
			self._scatter.super_on_touch_down = self._scatter.on_touch_down
			self._scatter.on_touch_move = self.scatter_on_touch_move
			self._scatter.on_touch_down = on_scatter_touch_down
			self._scatter.fbind('pos',self.on_drawer_progress)
			self.drawer.size_hint=[None,None]
			self.drawer.size=self.size

			if self._scatter not in self.children:
				self.add_widget(self._scatter)

			self.initialised_nav=True
			self._scatter.pos=-self.width,0
			self.on_open_hint(self,self.open_hint)

		Clock.schedule_interval(manage,.1)
		
	def manage_drawer_state(self,*args):
		"""Method for managing drawer state."""
		drx,dry=self._scatter.pos
		center_x=self.width/2
		w=self.drawer.width
		px=drx+w
		
		if drx==0.0:
			self.drawer_state="open"
		else:
			if drx<=-self.width:
				self.drawer_state='closed'
			elif drx<0.0 and drx<-center_x:
				self.drawer_state="closing"
			else:
				if drx>=-center_x:
					self.drawer_state="opening"
									
	def handle_keyboard_key_down(self,window,key,*args):
		if self.drawer_state=='open':
			if int(key)==27:
				self.close_drawer()
				if self.close_on_click:
					return True
				
	def manage_window(self,*_):
		self.window=Window
		if not self.window:
			Clock.schedule_once(self.manage_window)
			return
		self.window.bind(on_key_down=self.handle_keyboard_key_down)
					
	def open_drawer(self):
		self.anim_running=True
		if self.drawer.width == 100:
			#sizes not updated to widgets yet
			def open(*_):
				self.open_drawer()
			Clock.schedule_once(open)
			return
		pos=0,list(self.drawer.pos)[1]
		anim=Animation(pos=pos,duration = self.opening_anim_time, transition=self.opening_anim)
		anim.cancel_property(self,'pos')
		self.drawer_state="opening"
		self._scatter.pos = pos

		def on_finish(*a):
			self.drawer_state = "open"
			self.anim_running = False

		anim.on_complete =  on_finish
		
	def close_drawer(self):
		self.anim_running=True
		if self.drawer.width==100:
			#sizes not updated to widgets yet
			def close(*_):
				self.close_drawer()
			Clock.schedule_once(close)
			return
		pos =- self.drawer.width,list(self.drawer.pos)[1]
		anim = Animation(pos=pos,duration=self.closing_anim_time,transition=self.closing_anim)
		
		anim.cancel_property(self,'pos')
		self.drawer_state="closing"
		anim.start(self._scatter)
		def on_finish(*a):
			self.drawer_state="closed"
			self.anim_running=False

		anim.on_complete =  on_finish
		
	def scatter_on_touch_move(self,touch):
		"""Event called on drawer touch move."""
		x,y=self._scatter.pos
		if x==-self.drawer.width:
			#drawer is closed
			if list(self.tdown_pos)[0]<=self.start_open:
				#we allow user to open drawer
				#coz he is scrolling from the right bounds we know his intentions
				#we dont want mistaken actions
				pass
			else:return
		else:
			#drawer is half opened or closed
			pass
		self._scatter.super_on_touch_move(touch)
		
	def get_drawer(self,):
		return self.drawer
		
	def add_drawer_widget(self,wid):
		self.drawer.add_widget(wid)
	
	def remove_drawer_widget(self,wid):
		self.drawer.remove_widget(wid)
		
	def clear_drawer_widgets(self,):
		self.drawer.clear_widgets()
	
	def scatter_transform_with_touch(self, touch):
		"""Method to translate drawer position using touch pos."""
	    #used to move drawer
	    #using translation on x-axis to parent
	    #of self.drawer ,that is self._scatter
		tx, ty=touch.pos
		if not tx <= self.drawer.width:
			return
		changed = False
		if len(self._scatter._touches) == self._scatter.translation_touches:
			# _last_touch_pos has last pos in correct parent space,
			# just like incoming touch
			dx = (touch.x - self._scatter._last_touch_pos[touch][0]) \
			* self._scatter.do_translation_x
			dy = (touch.y - self._scatter._last_touch_pos[touch][1]) \
			* self._scatter.do_translation_y
			dx = dx / self._scatter.translation_touches
			dy = dy / self._scatter.translation_touches
			#drawer pos
			drx,dry=self._scatter.pos
			if drx+dx>0:dx=0
			self._scatter.apply_transform(Matrix().translate(dx, dy, 0))
			changed = True
		
		if len(self._scatter._touches) == 1:
			return changed
		
		# we have more than one touch... list of last known pos
		
		points = [Vector(self._scatter._last_touch_pos[t]) for t in self._scatter._touches if t is not touch]
		# add current touch last
		points.append(Vector(touch.pos))
		
		# we only want to transform if the touch is part of the two touches
		# farthest apart! So first we find anchor, the point to transform
		# around as another touch farthest away from current touch's pos
		anchor = max(points[:-1], key=lambda p: p.distance(touch.pos))
		
		# now we find the touch farthest away from anchor, if its not the
		# same as touch. Touch is not one of the two touches used to transform
		farthest = max(points, key=anchor.distance)
		if farthest is not points[-1]:
			return changed
		
		# ok, so we have touch, and anchor, so we can actually compute the
		# transformation
		old_line = Vector(*touch.ppos) - anchor
		new_line = Vector(*touch.pos) - anchor
		if not old_line.length():
			return changed
		
		angle = radians(new_line.angle(old_line)) * self._scatter.do_rotation
		if angle:
			changed = True
		self._scatter.apply_transform(Matrix().rotate(angle, 0, 0, 1), anchor=anchor)
		
		if self._scatter.do_scale:
			scale = new_line.length() / old_line.length()
			new_scale = scale * self._scatter.scale
			if new_scale < self._scatter.scale_min:
				scale = self._scatter.scale_min / self._scatter.scale
			elif new_scale > self._scatter.scale_max:
				scale = self._scatter.scale_max / self._scatter.scale
			self._scatter.apply_transform(Matrix().scale(scale, scale, scale),anchor=anchor)
			changed = True
		return changed