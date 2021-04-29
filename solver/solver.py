from queue import LifoQueue
import sys
sys.path.append('..')
from components.board import Board

class Solver():
	"""
	This class takes the Sudoku board class as a parameter and implements a stack of instructions for solving it, that grows/
	dynamically changes as numbers are found.  Abstract  - to help build other solvers faster.
	Properties:
		possible_answers: 2D list of sets with possible answers.  sets of size are the correct answer
		instruction_stack: LifoQueue, of tuples, of the form (function, *args, **kwargs).  ex: (self.do_something,(1,2,3),("keyword_argument_1":"value_1"))

	What YOU eed to implement if you inherit this-
		self.is_empty()- put some functions, args, kwargs into the stack when you have nothing left to do.

	"""
	possible_answers = None
	instructions_performed = []
	answers_written = 0

	def __init__(self, board):
		self.board = board
		self.instruction_stack = LifoQueue()
		self.initialize_possible_answers()
		
	def initialize_possible_answers(self):
		"""
		Before creating any instructions, we first determine possible values for each empty square.
		We do this on initialization in case we want this information to be used in determining our first
		instruction.

		While this does work and runs fine and could potentially solve many puzzles, its' not using the stack
		structure like I want.
		"""
		self.possible_answers = [[],[],[],[],[],[],[],[],[]]
		for i in range(0, 9):
			self.possible_answers[i] = [None, None, None, None, None, None, None, None, None]
		for row_num, row in enumerate(self.board.board_data):
			row_values = self.get_row_set(row_num,skip=True)
			for col_num, square in enumerate(row):
#				col_values = self.get_col_set(col_num)
#				group_values = self.get_group_set(row_num, col_num)
				if square.value is not None:
					self.possible_answers[row_num][col_num] = set([square.value])
				else:
					full_values = set([1,2,3,4,5,6,7,8,9])
					self.possible_answers[row_num][col_num] = full_values
#					This function should be purely to initalize for usage, not start solving.  We want to do all solving
#					via our stack structure
#					sets_to_subtract = [row_values, col_values, group_values]
#					self.possible_answers[row_num][col_num] = full_values.difference(*sets_to_subtract)
		self.print_possible_answers()
	
	def write_to_board(self, row, col, value):
		"""Writes a answer provided by the Solver to the board.  If this throws an error, thats fine, we let that bubble up
		to the custom solver class"""
		self.board.change_square(row, col, value)
		instructions_performed = [(self.write_to_board, (row, col,value), {})]
		self.answers_written += 1

	def print_possible_answers(self):
		"""
		Prints out current possible answers per square.
		"""
		print(f"poss answers {self.possible_answers}")
		for row_num, row in enumerate(self.possible_answers):
			for col_num, set_values in enumerate(row):
				only_one_answer_left_and_not_on_board_and_not_erasable = len(set_values) == 1 and self.board.board_data[row_num][col_num].value is None and self.board.board_data[row_num][col_num].erasable
				if  only_one_answer_left_and_not_on_board_and_not_erasable:
					print(f"Found new answer {set_values} for {row_num},{col_num}")


	def get_row_set(self, row,skip=False):
		"""
		Returns a set of all numbers that appear in the row
		Args:
			row: int, 0-9
			skip: bool, if true, dont'write to instructions performed.  only this one needs it
			for initalization.
		"""
		if not skip:
			self.instructions_performed.append((self.get_row_set,(row,),{}))
		return set([x.value for x in self.board.board_data[row]])		

	def get_col_set(self, col):
		"""
		Returns set of all numbers that appear in the column
		"""
		self.instructions_performed.append((self.get_col_set,(col,),{}))
		return  set([row[col].value for row in self.board.board_data])

	def get_group_set(self, row, col):
		"""
		Get set of values in group
		"""
		self.instructions_performed.append((self.get_group_set,(row,col),{}))
		group_num = self.board.board_data[row][col].group
		return self.board.get_group_value_set(group_num)

	def if_empty():
		"""
		What's your baseline instruction when there's nothing obvious to do?
		"""
		pass

	def do_next_step(self):
		"""
		Creates, and then does, next step into stack.
		"""
		if self.instruction_stack.empty():
			self.if_empty()
		func, params, keyword_params = self.instruction_stack.get()
		func(*params, **keyword_params)

	def get_group_reference_numbers(self, group_num):
		group_row_col_mapping = {
			1: (slice(0,3), slice(0,3),0,0),
			2: (slice(0,3), slice(3,6),0,3),
			3: (slice(0,3), slice(6,9),0,6),
			4: (slice(3,6), slice(0,3),3,0),
			5: (slice(3,6), slice(3,6),3,3),
			6: (slice(3,6), slice(6,9),3,6),
			7: (slice(6,9), slice(0,3),6,0),
			8: (slice(6,9), slice(3,6),6,3),
			9: (slice(6,9), slice(6,9),6,6)
		}
		return group_row_col_mapping[group_num]
	
	def change_possible_answer(self, row, col, new_set):
		value_to_write = set(new_set)
		self.possible_answers[row][col]=new_set
		self.instructions_performed.append((self.change_possible_answer,(row, col, new_set),{}))

class BruteForceSolver(Solver):
	"""
	Niave brute force solver.  Goes square byt square, gets the set subtraction of {1,2,3,4,5,6,7,8,9} from row, col and group sets.
	If a square becomes a set of one we know it is the answer and write it.  We do this, at least in this iteration, in a type-writer
	fashion - left to write ftopt o bottom.
	"""
	def __init__(self, board):
		super().__init__(board)
		self.do_next_step()

	def work_on_square(self, row, col):
		row_set = self.get_row_set(row)
		col_set = self.get_col_set(col)
		group_set = self.get_group_set(row, col)
		sets_to_subtract = [row_set, col_set, group_set]
#		self.possible_answers[row_num][col_num] = full_values.difference(*sets_to_subtract)
		curr_answer = self.possible_answers[row][col]
		if len(curr_answer)>1:
			new_answer = curr_answer.difference(*sets_to_subtract)
#			print(f"({row},{col})curr answer is {curr_answer} and new answer is {new_answer}")
			
			if len(new_answer) == 1:
				self.possible_answers[row][col]=new_answer.copy()
				self.write_to_board(row, col, new_answer.pop())					

	def start_from_beginning(self):
		for row_num, row in enumerate(self.possible_answers):
			for col_num, possible_answers in enumerate(row):
				self.work_on_square(row_num, col_num)
		print(f"{self.answers_written} answers written this round")
		self.board.print_board()
		if not self.board.won:
			self.do_next_step()

	def if_empty(self):
		self.instruction_stack.put((self.start_from_beginning,(), {}))

class BrianMethod(Solver):
	"""
	My personal method of solving sudoku puzzles in books. Just to get started.
	Think I have a pretty good method, think it should help dowell.
	"""
	def __init__(self, board):
		super().__init__(board)
		self.do_next_step()

	def work_on_group(self, number):
		"""Does my patented brian method on the grou}p"""
		print(f"Doing work on number {number}")
		row_slice, col_slice, row_start, col_start = self.get_group_reference_numbers(number)
		print(f"row nums is {row_slice} col nums is {col_slice}")
		for cur_row, row in enumerate(self.possible_answers[row_slice], start=row_start):
			# no need to get row every time getting columng
			row_set = self.get_row_set(cur_row)
			for cur_col, current_possible_answers in enumerate(self.possible_answers[cur_row][col_slice], start=col_start):
				col_set = self.get_col_set(cur_col)
				print(f"row num {cur_row} col num {cur_col} has {current_possible_answers}")
		print(f"{self.instructions_performed}")

	def if_empty(self):
		self.instruction_stack.put((self.work_on_group,(1,),{}))

if __name__ == "__main__":
	new_game = Board()
	my_solver = BruteForceSolver(new_game)