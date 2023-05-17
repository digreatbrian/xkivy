from kivy.properties import OptionProperty,NumericProperty,StringProperty,ObjectProperty,ListProperty,BooleanProperty
from math import sqrt
import time
from kivy.metrics import dp

class TouchEvent():
	direction=None
	distance=None
	pos=None
	def __str__(self):
		rp=super().__str__()
		hx=rp.split(' ')[-1].strip('>')
		return '<Touch distance = {} \ndirection = {} \npos = {} >'.format(self.distance,self.direction,self.pos)
		
	
	
class TouchManager():
	direction=OptionProperty(None,options=['top left','top right','bottom left','bottom right'])
	distance=NumericProperty(0)
	speed=NumericProperty(None)
	swipe_speed=NumericProperty(.25)
	allowed_swipe_distance=NumericProperty(dp(25))
	is_swipe=BooleanProperty(False)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.register_event_type('on_swipe_left')
		self.register_event_type('on_swipe_right')
		self.register_event_type('on_move_left')
		self.register_event_type('on_move_right')
		self.register_event_type('on_touch_stop')
		self.register_event_type('on_touch_start')
		self.register_event_type('on_move')
		
	
	def on_swipe_left(self,touch):
		pass
		
	def on_swipe_right(self,touch):
		pass
		
	def on_move(self,touch):
		pass
		
	def on_move_left(self,touch):
		pass
		
	def on_move_right(self,touch):
		pass
		
	def on_touch_stop(self,touch):
		pass
		
	def on_touch_start(self,touch):
		pass
		
	def on_touch_up(self,touch):
		self.touch_up_ev(touch)
		
	def on_touch_down(self,touch):
		self.touch_down_ev(touch)
		
	def on_touch_move(self,touch):
		self.touch_move_ev(touch)
		
	def touch_up_ev(self,touch):
		'''Event called by TouchManager on touch up.'''
		touch.ungrab(self)
		super().on_touch_up(touch)
		self.direction=self.get_direction(self.start_distance_pos,touch.pos)
		#dispatching events
		tch=TouchEvent()
		tch.pos=touch.pos
		tch.distance=self.distance
		tch.direction=self.direction
		########################
		self.speed=time.time()-self.start_time
		#calculating speed we dont want as for swipe event ,using self.swipe_speed
		bound_speed=self.swipe_speed-(self.swipe_speed/1.5)
		self.is_swipe=False
		if self.speed<=self.swipe_speed and self.speed>=bound_speed and self.distance>self.allowed_swipe_distance:
			#this is a swipe
			self.is_swipe=True
			if self.direction:
				if self.direction.split(' ')[1]=='left':
					self.dispatch('on_swipe_left',tch)
				else:
					self.dispatch('on_swipe_right',tch)
		self.continuous_touch=False
		self.dispatch('on_touch_stop',tch)
					
	def touch_down_ev(self,touch):
		'''Event called by TouchManager on touch down.'''
		touch.grab(self)
		super().on_touch_down(touch)
		self.start_time=time.time()
		self.start_distance_pos=touch.pos
		self.center_pos=(self.width/2,self.height/2)
		#dispatching events
		tch=TouchEvent()
		tch.pos=touch.pos
		tch.distance=self.distance
		tch.direction=self.direction
		#self.continuous_touch=True
		self.dispatch('on_touch_start',tch)
		
	def touch_move_ev(self,touch):
		'''Event called by TouchManager on touch move.'''
		super().on_touch_move(touch)
		end_x,end_y=touch.pos
		start_x,start_y=self.start_distance_pos
		#calculating distance using opposite,hypotenuse,adjacent sides
		
		adj=end_x-start_x
		opp=end_y-start_y
		self.distance=sqrt((opp*opp)+(adj*adj))
		#determining touch direction
		#determining if top or bottom
		if hasattr(self,'last_touch_move_pos'):
			start_pos=self.last_touch_move_pos
			end_pos=touch.pos
			self.manage_direction(start_pos,end_pos,touch)
		
		self.last_touch_move_pos=touch.pos
		#####################
		
	def get_direction(self,start_pos,end_pos):
		start_x,start_y=start_pos
		end_x,end_y=end_pos
		if end_y<start_y:
			direction='bottom'
		else:
			direction='top'
		#determiming if left or right
		if end_x<start_x:
			direction+=' left'
		else:
			direction+=' right'
		return direction
	
	def manage_direction(self,start_pos,end_pos,touch):
		start_x,start_y=start_pos
		end_x,end_y=end_pos
		if end_y<start_y:
			direction='bottom'
		else:
			direction='top'
		#determiming if left or right
		if end_x<start_x:
			direction+=' left'
		else:
			direction+=' right'
		if direction:
			self.direction=direction
			tch=TouchEvent()
			tch.pos=touch.pos
			tch.distance=self.distance
			tch.direction=self.direction
			self.dispatch('on_move',tch)
			if direction.split(' ')[1]=='left':
				self.dispatch('on_move_left',tch)
			else:
				self.dispatch('on_move_right',tch)
