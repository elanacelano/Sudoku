class UnwriteableSquareError(Exception):
	pass

class InvalidSquareValueError(Exception):
	pass

class InvalidMoveError(Exception):
	pass

class Square():
	"""
	Represents a singular square on the sudoku board.  Made so that the square can "know" its own group, and add properties like
    is it erasableor is it part ofthe board?
	"""
	row = None
	column = None
	value = None
	group = None
	erasable = True
	def __init__(self, row, column, value, initial_setup=False):
		self.row = row
		self.column = column
		self.value = value
		# Want to track and make sure that the numbers which are make up the board initially are not erasable
		if initial_setup:
			self.erasable = False
		self.calculate_group()

	def calculate_group(self):
		first_row = self.row >= 0 and self.row < 3
		second_row = self.row >= 3 and self.row < 6
		third_row = self.row >= 6 and self.row <= 8
		first_column = self.column >= 0 and self.column < 3
		second_column = self.column >=3 and self.column < 6
		third_column = self.column >=6 and self.column <= 8
		if first_row and first_column:
			self.group = 1
		elif first_row and second_column:
			self.group = 2
		elif first_row and third_column:
			self.group = 3
		elif second_row and first_column:
			self.group = 4
		elif second_row and second_column:
			self.group = 5
		elif second_row and third_column:
			self.group = 6
		elif third_row and first_column:
			self.group = 7
		elif third_row and second_column:
			self.group = 8
		elif third_row and third_column:
			self.group = 9

	def change_value(self, value):
		if self.erasable:
			if value is None or (isinstance(value, int) and 1 <= value <= 9):
				self.value = value
			else:
				raise InvalidSquareValueError("Square must be an integer between 1 and 9")
		else:
			raise UnwriteableSquareError("You cannot change a value that is hardcoded to the board")

from samples.sample_boards import test_board_1

class Board():
	"""
	Represents the full Sudoku board.  Allows entering of values into None, as long as it is currently valid.
	Also allows erasing of inputted values.  Cannot erase values that were given by the board.
	"""
	raw_board_data = None
	board_data = None
	won = False
	training_wheels = False
	def __init__(self, board_data=None):
		if board_data is None:
			board_data = test_board_1
		self.raw_board_data = board_data
		self.initialize_board()
		self.parse_board_data()

	def initialize_board(self):
        # To make the right sized board to then overwritewith squares
		self.board_data = [[],[],[],[],[],[],[],[],[]]
		for i in range(0, 9):
			self.board_data[i] = [None, None, None, None, None, None, None, None, None]

	def parse_board_data(self):
        # To fill in with raw boarddata
		for row_ind, row in enumerate(self.raw_board_data):
			for col_ind, value in enumerate(row):
				initial_setup = value is not None
				self.board_data[row_ind][col_ind] = Square(row_ind, col_ind, value, initial_setup=initial_setup)
	
	def print_value(self, square):
		"""
		Last part of pretty print, decide how to print each number.
		  Args:
			square: Square class either an int or None
		  Returns:
			None
		"""
		if square.value is not None:
			print(f" {square.value} ", end='')
		else:
			print("   ", end='')

	def print_row(self, row):
		"""
		Pretty prints a single row of the board
		  Args:
			row: list of 9 numbers or Nones
		  Returns:
			None
		"""
		for index, square in enumerate(row, start=0):
			if index == 0:
				print("|", end='')
				self.print_value(square)
			elif index == 2 or index == 5:
				self.print_value(square)
				print("|", end='')
			elif index == 8:
				self.print_value(square)
				print("|", end='\n')
			else:
				self.print_value(square)

	def print_board(self):
		"""
		Pretty prints current board.
		  Arg: 
			Board
		  Returns:
			None
		"""
		border = "-------------------------------"
		print(border, end='\n')
		for index, row in enumerate(self.board_data):
			self.print_row(row)
			if index == 2 or index == 5:
				print(border, end='\n')
		print(border, end='\n')

	def change_square(self, row, col, value):
		"""
		Used to change value of underlying square class
		"""
		if value == 0 or value == '':
			self.board_data[row][col].change_value(None)
		else:
			#  Allow the user to decide if we check for valid moves or not
			print("changing square")
			if self.training_wheels:
				print("checking if valid move")
				self.is_valid_move(row, col, value)
			self.board_data[row][col].change_value(value)
			self.check_win()
		# except ValueError as e:
		# 	print(e)
		# except IndexError:
		# 	print("Column or row is too large.  Remember to use 0 through 8.")

	def get_value(self, row, col):
		"""
		Retrieve value of square
		"""
		return self.board_data[row][col].value

	def check_win(self):
		"""
		Runs after every number a user goes down.  Checks 3 win conditions.
		All rows have 1-9, all columns have 1-9, and squares of 9 have 1-9,
		"""
		self.won = False
		row_win = self.check_row_win()
		col_win = self.check_col_win()
		group_win = self.check_group_win()
		print(f"Row win: {row_win}, Col win: {col_win}, Group win: {group_win}")
		if row_win and col_win and group_win:
			self.won = True

	def check_row_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for row_ind, row in enumerate(self.board_data):
			row_values = set([value.value for value in row])
			equals = correct_answer.issubset(row_values) and row_values.issubset(correct_answer)
			if not equals:
				all_true = False
				break
		return all_true
	
	def check_col_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for col_ind in range(0, 9):
			col_values = set([row[col_ind].value for row in self.board_data])
			equals = correct_answer.issubset(col_values) and col_values.issubset(correct_answer)
			if not equals:
				all_true = False
				break
		return all_true

	def check_group_win(self):
		correct_answer = {1, 2, 3, 4, 5, 6, 7, 8, 9}
		all_true = True
		for group_num in range(1,10):
			# turns a 2d list into a set
			group_values = self.get_group_value_set(group_num)
			equals = correct_answer.issubset(group_values) and group_values.issubset(correct_answer)
			if not equals:
				all_true = False
				break
		return all_true

	def get_group_values(self, group_num):
		"""
		Gets all values for a group.  Group 1 being the block of 9 numbers in the top left,
		group 2 being the 9 numbers in the top middle, 3 top 9 numbers top right, and so on.
        Helper function for all around.
		  Args:
		    group_num: int, between 1 and 9
		    board:  test_board, an infed board, or the answer board
		  Returns:
		    list of values in that group
		"""
		if group_num in (1,2,3):
			first_row = 0
			last_row = 3
		elif group_num in (4,5,6):
			first_row = 3
			last_row = 6
		elif group_num in (7,8,9):
			first_row = 6
			last_row = 9
		else:
			raise ValueError("Group number is invalid")

		if group_num in (1,4, 7):
			first_col = 0
			last_col = 3
		elif group_num in (2, 5, 8):
			first_col = 3
			last_col = 6
		elif group_num  in (3, 6, 9):
			first_col = 6
			last_col = 9

		return [[x.value for x in row[first_col:last_col]] for row in self.board_data[first_row:last_row]]
	
	def get_group_value_set(self, group_num):
		# This gets a 2-D list that we then map the set function onto each row, and then finally set.union these three new unions together
		return set.union(*map(set,self.get_group_values(group_num)))

	def is_valid_move(self, row, col, value):
		"""
		Checks all three vectors to see if a move is possible.
		"""
		row_legal = self.check_if_valid_row_value(row, col, value)
		col_legal = self.check_if_valid_col_value(row, col, value)
		group_legal = self.check_if_valid_group_value(row, col, value)
		if row_legal and col_legal and group_legal:
			return
		else:
			error_message_mapping = [(row_legal, f"{value} exists in this row."), (col_legal, f"{value} exists in this column."), (group_legal, f"{value} exists in this group.")]
			error_message = ' '.join([message for (err, message) in error_message_mapping if err])
			raise InvalidMoveError(error_message)

	def check_if_valid_row_value(self, row, col, value):
		"""Checks to see if new input value already exists in row"""
		row_values = set([x.value for x in self.board_data[row]])
		return value in row_values
	
	def check_if_valid_col_value(self, row, col, value):
		"""Checks to see if new input value already exists in cl"""
		col_values =  set([row[col].value for row in self.board_data])
		return value in col_values

	def check_if_valid_group_value(self, row, col, value):
		"""Checks to see if new input value already exists in group"""
		group_num = self.board_data[row][col].group
		group_values = self.get_group_value_set(group_num)
		return value in group_values