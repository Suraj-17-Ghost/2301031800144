import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=15):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()
        
    def create_widgets(self):
        # Create menu
        menubar = tk.Menu(self.master)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.master.config(menu=menubar)
        
        # Create buttons grid
        for row in range(self.rows):
            for col in range(self.cols):
                btn = tk.Button(self.master, text=' ', width=3, height=1,
                              command=lambda r=row, c=col: self.on_click(r, c))
                btn.bind('<Button-3>', lambda e, r=row, c=col: self.on_right_click(r, c))
                btn.grid(row=row, column=col)
                self.buttons[(row, col)] = btn
    
    def place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mine_positions = set(random.sample(positions, self.mines))
        
    def calculate_adjacent_mines(self):
        self.adjacent_mines = {}
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.mine_positions:
                    self.adjacent_mines[(row, col)] = -1  # -1 means it's a mine
                    continue
                
                count = 0
                for r in range(max(0, row-1), min(self.rows, row+2)):
                    for c in range(max(0, col-1), min(self.cols, col+2)):
                        if (r, c) in self.mine_positions:
                            count += 1
                self.adjacent_mines[(row, col)] = count
    
    def on_click(self, row, col):
        if (row, col) in self.mine_positions:
            self.game_over()
            return
            
        self.reveal_cell(row, col)
        self.check_win()
    
    def on_right_click(self, row, col):
        btn = self.buttons[(row, col)]
        if btn['state'] == 'normal':
            btn.config(text='🚩', state='disabled')
        elif btn['text'] == '🚩':
            btn.config(text=' ', state='normal')
    
    def reveal_cell(self, row, col):
        btn = self.buttons[(row, col)]
        if btn['state'] == 'disabled':
            return
            
        mines_nearby = self.adjacent_mines[(row, col)]
        if mines_nearby > 0:
            btn.config(text=str(mines_nearby), state='disabled', relief=tk.SUNKEN)
            colors = ['', 'blue', 'green', 'red', 'darkblue', 'brown', 'cyan', 'black', 'gray']
            btn.config(fg=colors[mines_nearby])
        else:
            btn.config(text=' ', state='disabled', relief=tk.SUNKEN)
            # Reveal adjacent cells
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if (r, c) != (row, col):
                        self.reveal_cell(r, c)
    
    def game_over(self):
        for (row, col) in self.mine_positions:
            self.buttons[(row, col)].config(text='💣', bg='red')
        for btn in self.buttons.values():
            btn.config(state='disabled')
        messagebox.showinfo("Game Over", "You hit a mine! Game over.")
    
    def check_win(self):
        unrevealed = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.mine_positions and self.buttons[(row, col)]['state'] == 'normal':
                    unrevealed += 1
        if unrevealed == 0:
            for (row, col) in self.mine_positions:
                self.buttons[(row, col)].config(text='🚩')
            messagebox.showinfo("Congratulations!", "You won!")
    
    def reset_game(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons = {}
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()