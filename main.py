import random as r

class Space:
  SAFE = 0;
  BOMB = 1;

class Visual: 
  COVERED = 2
  UNCOVERED = 3
  FLAGGED = 4

class Board:
  def __init__(self, size, n_bombs):
    self.bombs = n_bombs;
    self.matrix = [];
    self.visual = [];
    self.init_board(size);
  
  def init_board(self, size):
    y = 0
    x = 0
    while(y<size):
      # Set the temp row for the actual matrix
      temp_row_matrix = []

      # Set the temp row for the visusal matrix
      temp_row_visual = []

      while(x<size):

        # Create an entry in the actual matrix
        temp_row_matrix.append(Space.SAFE);

        # Create an entry in teh visual matrix
        temp_row_visual.append(Visual.COVERED)

        x+=1
      
      # Add in the temp_rows
      self.matrix.append(temp_row_matrix);
      self.visual.append(temp_row_visual);

      x=0
      y+=1

    # Add in bombs to the actual matrix
    self.randomize_bombs(self.bombs);

  def randomize_bombs(self, n):
    i=0
    while(i<n):
      i+=1
      x = -1
      y = -1

      # Ensure No duplicates
      while(x<=0 or self.getSpace(x,y) == Space.BOMB):
        x = r.randint(0,len(self)-1);
        y = r.randint(0,len(self)-1);
      
      # Set space to bomb
      self.setSpace(x,y,Space.BOMB)

  def getSpace(self, x, y):
    return self.matrix[y][x];

  def setSpace(self, x, y, value):
    self.matrix[y][x] = value

  def getVisualSpace(self, x, y):
    return self.visual[y][x]
  
  def setVisualSpace(self, x, y, value):
    self.visual[y][x] = value
  
  def printBombs(self):
    string = ""
    for row in self.matrix: 
      for item in row:
        string+=str(item)+" ";
      string+="\n"
    print(string);

  def printView(self):
    string = "   "

    # Create Top Row
    for x in range(0,len(self)):
      n = str(x+1)
      string+=n
      if(len(n)<2):
        string+=" "
    string+="\n"

    # Create Board
    for y, row in enumerate(self.visual): 
      string+=str(y+1)+" "
      if(len(str(y+1))<2):
        string+=" "
      for x, item in enumerate(row):
        if(item==Visual.COVERED):
          string+="■ "
        elif(item==Visual.FLAGGED):
          string+="⚑ "
        elif(item==Visual.UNCOVERED):
          if(self.getNumberOfBombs(x,y)>0):
            string+=str(self.getNumberOfBombs(x,y))+" "
          else:
            string+=str("  ")
      string+="\n"
    print(string);

  def getNumberOfBombs(self, x, y):
    # if is bomb then return -1
    if self.isBomb(x,y):
      return -1
    
    # Get number of adjacent Bombs
    count =\
    self.countBomb(x, y, -1, -1)+self.countBomb(x, y, 0, -1)+self.countBomb(x, y, 1, -1)+self.countBomb(x, y, -1, 0)+self.countBomb(x, y, 1, 0)+self.countBomb(x, y, -1, 1)+self.countBomb(x, y, 0, 1)+self.countBomb(x, y, 1, 1)

    return count

  def isBomb(self, x, y):
    return self.getSpace(x,y)==Space.BOMB

  def countBomb(self, x, y, add_x=0, add_y=0):
    new_x = x+add_x
    new_y = y+add_y

    if(self.inBounds(new_x, new_y)):
       return self.isBomb(new_x,new_y)
    return 0

  def isUncovered(self, x, y):
    return self.getVisualSpace(x, y) == Visual.UNCOVERED
    
  def flag(self, x, y):
    if(self.getVisualSpace(x,y)==Visual.FLAGGED):
      self.setVisualSpace(x,y,Visual.COVERED)
    else:
      self.setVisualSpace(x,y,Visual.FLAGGED)

  def uncover(self, x, y, x_add = 0, y_add = 0):
    # Check bounds
    new_x = x+x_add
    new_y = y+y_add
    
    # if out of bounds
    if(not self.inBounds(new_x, new_y)):
      return None

    # Check that space hasn't already been uncovered
    if(self.isUncovered(new_x, new_y)):
      return None

    # Check that space is not flagged
    if(self.getVisualSpace(new_x,new_y)==Visual.FLAGGED):
      return None

    # if in bound set x and y to new values
    x = new_x
    y = new_y


    # Check that self isn't bomb
    if(self.isBomb(x, y)):

      # end program if is bomb
      if(x_add == 0 and y_add == 0):
        return -1;
      return None

    # Set the current space to uncovered
    self.setVisualSpace(x, y, Visual.UNCOVERED)

    # Get number of bombs adjacent to space
    count = self.getNumberOfBombs(x,y);

    # If there are no bombs on tile
    if(count == 0):
      self.uncover(x, y, -1, -1)
      self.uncover(x, y, 0, -1)
      self.uncover(x, y, 1, -1)
      self.uncover(x, y, -1, 0)
      self.uncover(x, y, 1, 0)
      self.uncover(x, y, -1, 1)
      self.uncover(x, y, 0, 1)
      self.uncover(x, y, 1, 1)
      

        

  def __len__(self):
    return len(self.matrix)

  def inBounds(self, x, y):
    return x<len(self) and x>=0 and y<len(self) and y>=0

b= Board(20,50)

while(True):
  print()
  b.printView()
  flag = input("Flag? (y/n):")
  x = int(input("x: "))-1
  y = int(input("y: "))-1
  if(flag=="n"):
    if(b.uncover(x,y)==-1):
      print("Bomb Hit!!")
      print("Game Over")
      break;
  elif(flag=="y"):
    b.flag(x,y)
