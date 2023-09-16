from math import sqrt
from time import time
from kivy.metrics import dp
from kivy.properties import (OptionProperty,
                             NumericProperty,
                             BooleanProperty,
			     			 ListProperty,
							 )

class TouchEvent:
	'''Object that represents a touch event '''
	direction = None
	distance = None
	pos = None
	is_continuous = False
	def __str__(self):
		return '<Touch distance = {} \ndirection = {} \npos = {} >'.format(self.distance, self.direction, self.pos)
			
class TouchManager:
	touch_direction = OptionProperty(None,options=['top left','top right','bottom left','bottom right'])
	touch_distance = NumericProperty(0)
	touch_speed = NumericProperty(None)
	touch_min_recognized_swipe_speed = NumericProperty(.25)
	touch_min_recognized_swipe_distance = NumericProperty(dp(25))
	touch_is_swipe = BooleanProperty(False)
	touch_is_continuous = BooleanProperty(False)
	touch_pos = ListProperty([])
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.register_event_type('on_swipe_left')
		self.register_event_type('on_swipe_right')
		self.register_event_type('on_move_left')
		self.register_event_type('on_move_right')
		self.register_event_type('on_touch_stop')
		self.register_event_type('on_touch_start')
		self.register_event_type('on_move')
		self.register_event_type('on_swipe')

	def on_swipe(self,touch):
		pass
		
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
		
	def on_touch_start(self,touch):
		pass

	def on_touch_stop(self,touch):
		pass

	def on_touch_down(self,touch):
		self.touch_down_ev(touch)
		return super().on_touch_down(touch)
	
	def on_touch_move(self,touch):
		self.touch_move_ev(touch)
		return super().on_touch_move(touch)
			
	def on_touch_up(self,touch):
		self.touch_up_ev(touch)
		return super().on_touch_up(touch)
					
	def touch_down_ev(self,touch):
		'''Event called by TouchManager on touch down.'''
		self._touch_start_time = time()
		self._touch_start_pos = touch.pos
		self._touch_center_pos=(self.width / 2, self.height / 2)
		
		#dispatching events
		tch = TouchEvent()
		tch.pos = touch.pos
		tch.is_continuous = False
		
		self.touch_pos = touch.pos
		self.touch_is_continuous = False
		self.dispatch('on_touch_start',tch)
		
	def touch_move_ev(self,touch):
		'''Event called by TouchManager on touch move.'''
		end_x, end_y = touch.pos
		start_x, start_y = self._touch_start_pos
		#calculating distance using opposite, hypotenuse, adjacent sides
		
		adj = end_x - start_x
		opp = end_y - start_y
		self.touch_distance = sqrt((opp * opp) + (adj * adj))
		self.touch_pos = list(touch.pos)
		self.touch_is_continuous = True
		#determining touch direction
		#determining if left or right
		if hasattr(self, '_touch_move_last_pos'):
			start_pos = self._touch_move_last_pos
			end_pos = touch.pos
			self.touch_direction = self.get_direction(start_pos,end_pos)

			tch = TouchEvent()
			tch.direction = self.touch_direction
			tch.distance = self.touch_distance
			tch.pos = end_pos
			tch.is_continuous = True

			self.dispatch('on_move' ,tch)

			if self.touch_direction.split(' ')[-1] == 'left':
				self.dispatch('on_move_left' ,tch)

			else:
				self.dispatch('on_move_left' ,tch)
		
		self._touch_move_last_pos = touch.pos
		#####################
	
	def touch_up_ev(self,touch):
		'''Event called by TouchManager on touch up.'''
		end_x, end_y = touch.pos
		start_x, start_y = self._touch_start_pos
		#calculatin touch distance ,etc

		adj = end_x - start_x
		opp = end_y - start_y
		self.touch_distance = sqrt((opp * opp) + (adj * adj))
		self.touch_direction = self.get_direction(self._touch_start_pos, touch.pos)
		self.touch_pos = list(touch.pos)

		#dispatching events
		tch = TouchEvent()
		tch.pos = touch.pos
		tch.distance = self.touch_distance
		tch.direction = self.touch_direction
		########################
		self._touch_speed = time() - self._touch_start_time
		
		#calculating speed we dont want as for swipe event ,using self.touch_min_recognized_swipe_speed
		bound_speed = self.touch_min_recognized_swipe_speed - (self.touch_min_recognized_swipe_speed / 1.5)
		
		self.is_swipe = False
		
		if self._touch_speed <= self.touch_min_recognized_swipe_speed and self._touch_speed >= bound_speed and self.touch_distance > self.touch_min_recognized_swipe_distance:
			#this is a swipe
			self.is_swipe = True

			self.dispatch('on_swipe',tch)

			if self.touch_direction:
				if self.touch_direction.split(' ')[1] == 'left':
					self.dispatch('on_swipe_left',tch)
				else:
					self.dispatch('on_swipe_right',tch)

		self.dispatch('on_touch_stop',tch)
		
	def get_direction(self,start_pos,end_pos):
		'''Get direction of the touch depending on start position and end position'''
		start_x, start_y=start_pos
		end_x, end_y=end_pos
		if end_y < start_y:
			direction = 'bottom'
		else:
			direction = 'top'
		#determiming if left or right
		if end_x < start_x:
			direction += ' left'
		else:
			direction += ' right'
		return direction
	