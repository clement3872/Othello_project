import tkinter as tk
from tkinter import messagebox as tkm
import board


class Interface:
	def __init__(self, nb_players):
		self.width, self.height = 600, 600 # canvas size
		self.game_board = board.Board(nb_players)

		self.size_x = self.width//8
		self.size_y = self.height//8
		self.player_scores = {"black": 2, "white": 2}

		self.root1 = tk.Tk()
		self.root1.title("Plateau de l'Othello")

		self.canvas = tk.Canvas(self.root1, width=self.width, height=self.height, bg="#21854d") 
		self.canvas.pack() 

		self.canvas.bind("<Button-1>", self.on_click)

		self.label_display = tk.Label(self.root1, text=self.game_board.player_team)

		self.game_board.update_with_possible_moves()
		self.display_grid()
		self.display_pawns()

		self.score_blk = tk.Label(self.root1, text="Black: " + str(self.player_scores["black"])) 
		self.score_wht = tk.Label(self.root1, text="White: " + str(self.player_scores["white"]))

		self.score_blk.pack(side=tk.LEFT)
		self.score_wht.pack(side=tk.LEFT)


	def on_click(self, event):
		# get current position for array
		x, y = event.x//self.size_x, event.y//self.size_y 
		if self.game_board.get(x,y) == 0 or self.game_board.get(x,y) in ("white","black"):
			print("You cannot play this move")
			self.label_display.pack_forget()
			self.label_display = tk.Label(self.root1, text="you cannot play here")
			self.label_display.pack()
			return 1

		self.game_board.place_pawn(x,y)
		self.label_display.pack_forget()
		self.label_display = tk.Label(self.root1, text=self.game_board.player_team)
		self.label_display.pack()
		# x, y = x*self.size_x+ self.size_x//2, y*self.size_y+ self.size_y//2
		# self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")

		self.clear_canvas()
		self.display_grid()
		self.display_pawns()
		self.check_board_is_full()
		self.update_score()


	def clear_canvas(self):
		self.canvas.delete("all")
		self.display_grid()

	def display_pawns(self):
		# "radius" for the pawns
		pawn_size_x = self.size_x//2.5
		pawn_size_y = self.size_y//2.5
		# To place the pawns in the center of a box
		half_box_x = self.size_x//2
		half_box_y = self.size_y//2

		for i in range(8): # column
			for j in range(8): # row
				pawn = self.game_board.get(i,j)
				if pawn in ("white","black"):
					color = pawn
					self.canvas.create_oval(
						self.size_x*i-pawn_size_x + half_box_x, 
						self.size_y*j-pawn_size_y + half_box_y,
						self.size_x*i+pawn_size_x + half_box_x, 
						self.size_y*j+pawn_size_y + half_box_y,
						fill=color, outline=color)
				elif pawn > 0:
					# possible moves marker
					self.canvas.create_oval(
						self.size_x*i-pawn_size_x//2 + half_box_x, 
						self.size_y*j-pawn_size_y//2 + half_box_y,
						self.size_x*i+pawn_size_x//2 + half_box_x, 
						self.size_y*j+pawn_size_y//2 + half_box_y,
						fill="gray", outline="orange")


	def display_grid(self):
		for i in range(1,8):
			tmp_x = self.size_x*i
			tmp_y = self.size_y*i
			self.canvas.create_line(tmp_x,0,tmp_x, self.height, width=3)
			self.canvas.create_line(0,tmp_y,self.width, tmp_y, width=3)
	
	def check_board_is_full(self):
		if self.game_board.board_is_full():
			tkm.showinfo("Finish !")
	
	def update_score(self):
		"""
		For each move, calculate the number of occurrences of pawns in the list
		"""
		b_score = self.game_board.board_list.count("black")
		w_score = self.game_board.board_list.count("white")

		self.player_scores["black"] = b_score
		self.player_scores["white"] = w_score

		self.score_blk.config(text="Black: " + str(self.player_scores["black"]))
		self.score_wht.config(text="White: " + str(self.player_scores["white"]))


if __name__ == "__main__":
	app = Interface(2)