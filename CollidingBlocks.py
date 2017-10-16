from tkinter import*
import random


 #=========CONSTANTS=============#


TITLE = "TeCollidingBlocks"
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BACKGROUND_COLOR = 'white'
BLOCK_SIZE = 30
MIN_BLOCK_SIZE = 15
MAX_BLOCK_SIZE = 40
ENEMY_COLOR = "red"
NUM_OF_BLOCKS = 20
COLORS = [ENEMY_COLOR, "powder blue", "gold", ENEMY_COLOR, "Slate Blue",
      "Turquoise", ENEMY_COLOR, "Olive Drab", "Deep Pink", ENEMY_COLOR,
      "aqua", "dark green", ENEMY_COLOR, "Dark Violet"]
BLOCK_COLOR = "blue"
BLOCK_VX = 1
BLOCK_VY = 1
ANIM_DELAY = 20


class Game(Tk):
       
    def __init__(self, parent = None ):
        Tk.__init__( self, parent )
        self.title(TITLE)
        self.player_block = None
        self.blocks = []
        self.canvas = Canvas( self, width = WINDOW_WIDTH, height = WINDOW_HEIGHT,
                                 bg = BACKGROUND_COLOR )
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.mouse_click)
        self.canvas.bind('<Button-2>', self.on_wheel_click)
        self.canvas.bind('<Button-3>', self.mouse_click, '+')

        self.start_new_game()
        self.main()
        
    #main loop of the game

    def main(self):
        if not (self.player_block is None):
            self.player_block.move()
            self.handle_wall_collision()
            self.handle_collision_with_other_blocks()            
            self.check_win()
        self.after(ANIM_DELAY, self.main)

        
    def count_friendly_blocks(self):
        counter = 0
        for b in self.blocks:
            if b.color != ENEMY_COLOR:
                counter += 1
        return counter
            

    def on_wheel_click(self, event):
        self.start_new_game()

        
    def start_new_game(self):
        if not (self.player_block is None):
            self.player_block.hide()
            self.player_block = None
        self.create_blocks()
        self.title(TITLE)
        

    def check_win(self):
        if self.player_block is None:
            return        
        if self.count_friendly_blocks() == 0:
            self.title(TITLE + " - You won!!!")
            self.player_block.dx = 0
            self.player_block.dy = 0
        elif self.player_block.dx == 0 and self.player_block.dy == 0:
            self.title(TITLE + " - You lost!")


    def create_blocks(self):
        for b in self.blocks:
            b.hide()
        self.blocks.clear()
        while len(self.blocks) < NUM_OF_BLOCKS:
            rand_size = random.choice(range(MIN_BLOCK_SIZE, MAX_BLOCK_SIZE))
            next_block = Block( self.canvas, random.choice(range(MAX_BLOCK_SIZE,
                                              WINDOW_WIDTH - MAX_BLOCK_SIZE)),
                          random.choice(range(MAX_BLOCK_SIZE,
                                              WINDOW_HEIGHT - MAX_BLOCK_SIZE)),
                          rand_size, rand_size, random.choice(COLORS) )
            is_pos_OK = True
            for b in self.blocks:
                if next_block.is_collision(b):
                    is_pos_OK = False
                    break
            if is_pos_OK:
                self.blocks.append(next_block)
                next_block.draw()
                
            
    def turn_left(self):
        if self.player_block.dx * self.player_block.dy < 0:
            self.player_block.dx *= -1
        else:
            self.player_block.dy *= -1


    def turn_right(self):
        if self.player_block.dx * self.player_block.dy < 0:
            self.player_block.dy *= -1
        else:
            self.player_block.dx *= -1
            

    def handle_wall_collision(self):
        if((self.player_block.left() <= 0) or
          (self.player_block.right() >= WINDOW_WIDTH)):
            self.player_block.dx *= -1
        if((self.player_block.top() <= 0) or
          (self.player_block.bottom() >= WINDOW_HEIGHT)):
            self.player_block.dy *= -1


    def handle_collision_with_other_blocks(self):
        for other in self.blocks:
            if self.player_block.is_collision(other):
                if(other.color == ENEMY_COLOR):
                    self.player_block.dx = 0
                    self.player_block.dy = 0
                else:
                    self.player_block.dx *= -1
                    self.player_block.dy *= -1
                    self.blocks.remove(other)
                    other.hide()

                    
    #mouse events
    def mouse_click(self, event):
        if event.num == 1:
            if self.player_block is None:
                self.player_block = Block( self.canvas, event.x, event.y, BLOCK_SIZE, BLOCK_SIZE,
                                           BLOCK_COLOR, BLOCK_VX, BLOCK_VY )
                self.player_block.draw()
            else:
                self.turn_left()

        elif event.num == 3:
            self.turn_right()  


#Block class
class Block():
    
    def __init__(self, canvas, x = -100, y = -100, w = 0, h = 0, color = "blue", dx = 0, dy = 0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.dx = dx
        self.dy = dy


    def left(self):
        return self.x


    def top(self):
        return self.y


    def right(self):
        return self.x + self.w


    def bottom(self):
        return self.y + self.h


    def draw(self):
        self.canvas.create_rectangle( self.x, self.y,self.x + self.w,self.y + self.h,
                                fill=self.color)


    def hide(self):
        self.canvas.create_rectangle( self.x, self.y,self.right(),self.bottom(),
                                 fill= BACKGROUND_COLOR,
                                 outline = BACKGROUND_COLOR )



    def is_collision(self, other):
        return not ( (self.right() < other.left()) or
                     (self.bottom() < other.top()) or
                     (self.left() > other.right()) or
                     (self.top() > other.bottom()) )

    
    def move(self):
        self.hide();
        self.x += self.dx
        self.y += self.dy
        self.draw();
                  

game = Game()
game.mainloop()
