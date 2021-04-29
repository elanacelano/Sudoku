# plyer is a one stop shop that udner the hood knows how to call native api's for a number of different os/systems
import plyer

# Program to Show how to create a switch
# import kivy module	
import kivy
from kivy.properties import ObjectProperty
# base Class of your App inherits from the App class.	
# app:always refers to the instance of your application
from kivy.app import App
from kivy.uix.gridlayout import GridLayout	
from kivy.logger import Logger
# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# Builder is used when .kv file is
# to be used in .py file
from kivy.lang import Builder

# The screen manager is a widget
# dedicated to managing multiple screens for your application.
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
SlideTransition, CardTransition, SwapTransition,
FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
from components.board import Board, UnwriteableSquareError, InvalidSquareValueError, InvalidMoveError

# You can create your kv code in the Python file
Builder.load_file('gui/gui.kv')

# Global variables
options = {
	"training_wheels":True
 }

game = Board(board_data=None)

# Create a class for all screens in which you can include
# helpful methods specific to that screen
class SplashScreen(Screen):
	pass

class NewGame(Screen):
	def __init__(self, **kwargs):
		super(Screen,self).__init__(**kwargs)
		self.initialize_board()
	
	def on_enter(self):
		plyer.notification.notify(title='New Game!!', message='Play new game!', app_name='Sudoku Solver', app_icon='', timeout=10, ticker='Incominggg', toast=False)

	def initialize_board(self):
		"""
		Sets the hardcoded values to the board upon loading
		"""
		for screen in self.walk():
			for text_input in screen.walk():
				if isinstance(text_input, kivy.uix.textinput.TextInput):
					value = game.get_value(text_input.board_row, text_input.board_col)
					text_input.text = str(value)

	def set_value(self, instance):
		"""
		Tries to set the value of the sudoku square to the inputted user value.
		Args:
			instance: the TextInput component that had its text changed
		"""
		try:
			value = int(instance.text)
			game.change_square(instance.board_row, instance.board_col, value)
		except UnwriteableSquareError as e:
			# Handles when a person tries to over write a hardcoded value, write back old value
			old_value = game.get_value(instance.board_row, instance.board_col)
			instance.text = str(old_value)
		except InvalidSquareValueError as e:
			# Handles values < 1 or > 9 
			old_value = game.get_value(instance.board_row, instance.board_col)
			instance.text = str(old_value)
		except ValueError as e:
			# Handles non-integer inputs - clear square/don't allow
			instance.text = ''
		except InvalidMoveError as e:
			content = Button(text=str(e))
			popup = Popup(title='Invalid Move', content=content, auto_dismiss=False, size=(10, 10))
			content.bind(on_press=popup.dismiss)
			popup.open()
			instance.text = ''
		finally:
			self.check_win()
	
	def check_win(self):
		"""
		After every move, good or bad, just check the win 
		"""
		if game.won:
			Logger.info("You won!")

class Options(Screen):
	def __init__(self, **kwargs):
		super(Screen,self).__init__(**kwargs)
		game.training_wheels = options['training_wheels']

	def training_wheels_initial_value(self):
		return options['training_wheels']

	def set_training_wheels(self, instance, value):
		"""
		Turns on the training wheels.  Won't allow invalid moves.
		"""
		options['training_wheels'] = value
		game.training_wheels = value

class ScreenFour(Screen):
	pass


# The ScreenManager controls moving between screens
# You can change the transitions accorsingly
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(SplashScreen(name ="Splash Screen"))
screen_manager.add_widget(NewGame(name ="New Game"))
screen_manager.add_widget(Options(name ="Options"))
screen_manager.add_widget(ScreenFour(name ="Screen 4"))

# Create the App class
class ScreenApp(App):
	def build(self):
		return screen_manager

# run the app
if __name__ == "__main__":
    sample_app = ScreenApp()
    sample_app.run()