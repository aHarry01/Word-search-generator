import random
import string
import io
from PIL import Image
from reportlab.lib.utils import ImageReader
import reportlab.pdfgen.canvas
import reportlab.lib.pagesizes
from reportlab.pdfbase.pdfmetrics import stringWidth

#tries to insert in a given direction
#dx and dy are the steps that x and y should make for each subsequent letter in the word
def try_insert_in_direction(grid, word ,x, y, stringSpot, dx, dy):
    #if x or y go out of bounds, then we ran out of room
    if (y+dy) < 0 or (y+dy) > len(grid[0]) or (x+dx) < 0 or (x+dx) > len(grid):
        return False
    elif grid[x][y] != " ": #another letter from another word is already here
        return False
    else: #still good to put a letter here
        grid[x][y] = word[stringSpot]
        if (stringSpot + 1) >= len(word): #make it to the end of the word
            return True
        inserted = try_insert_in_direction(grid, word, x+dx, y+dy, stringSpot+1, dx, dy)
        if inserted == False: #if we couldn't insert in this direction, remove the letter we already put down here
            grid[x][y] = " "
            return False
        else:
            return True

#insert the given word into the grid of the wordsearch, first letter on x,y
def insert_word(grid, word, x, y):
    directions = ["down", "up", "right", "left", "diag", "diag_backwards"]
    rand_dirs = random.sample(directions,len(directions))
    inserted = False
    count = 0
    #insert this word at its randomly generated spot in the grid, in a random direction
    while not inserted and count < len(rand_dirs):
        word = word.replace(" " , "")
        if rand_dirs[count] == "down":
            inserted = try_insert_in_direction(grid,word,x,y,0,1,0)#insert_down(grid,word,x,y,0)
        elif rand_dirs[count] == "up":
            inserted = try_insert_in_direction(grid,word,x,y,0,-1,0) #insert_up(grid,word,x,y,0)
        elif rand_dirs[count] == "right":
            inserted = try_insert_in_direction(grid,word,x,y,0,0,1) #insert_right(grid,word,x,y,0)
        elif rand_dirs[count] == "left":
            inserted = try_insert_in_direction(grid,word,x,y,0,0,-1)  #insert_left(grid,word,x,y,0)
        elif rand_dirs[count] == "diag":
            inserted = try_insert_in_direction(grid,word,x,y,0,1,1) #insert_diagonal(grid,word,x,y,0)
        elif rand_dirs[count] == "diag_backwards":
            inserted = try_insert_in_direction(grid,word,x,y,0,-1,-1) #insert_diagonal_backwards(grid,word,x,y,0)
        count +=1
    if inserted:
        print(word + " inserted at " + str(y) + "," + str(x))
    return inserted

#creates a new pdf, and a canvas with a title on that pdf
def create_canvas(filename, title, background_filename=""):
    letter = reportlab.lib.pagesizes.letter
    c = reportlab.pdfgen.canvas.Canvas(filename, pagesize=letter)
    c.setFont('Courier', 30)

    #user has the option put an background for the pdf
    if background_filename != "":
        img = Image.open(background_filename)
        img_data = io.BytesIO()
        img.save(img_data, format="png")
        img_data.seek(0)
        img_out = ImageReader(img_data)
        c.drawImage(img_out, 0,0)
    
    title_width = stringWidth(title, "Courier", 30)
    textObj = c.beginText((letter[0] - title_width) / 2.0,letter[1]-65)
    textObj.textOut(title)
    c.drawText(textObj)
    return c

#output the wordsearch to a pdf 
def writeOutput(grid,width,height, words, title, output_filename, background=""): 
    c = create_canvas(output_filename, title, background)
    letter = reportlab.lib.pagesizes.letter

    #create & output the actual wordsearch
    c.setFont("Courier", 18)
    str_width = stringWidth("X " * height, "Courier", 18)
    ws_textObj = c.beginText((letter[0] - str_width)/2.0,letter[1]-135)
    ws_textObj.setFont("Courier", 18)
    line = ""
    for x in range(0,width):
        for y in range(0,height):
            if grid[x][y] == " ":
                line = line + " " + random.choice(string.ascii_uppercase)
            else:
                line = line + " " + grid[x][y]
        ws_textObj.textLine(line)
        line = ""    
    c.drawText(ws_textObj)

    #output words on the bottom half of the page
    words_text_half_one = c.beginText(75, letter[1]-525)
    words_text_half_two = c.beginText(250, letter[1]-525)
    words_text_half_one.setFont("Courier", 18)
    words_text_half_two.setFont("Courier", 18)
    count = 0;
    for w in words:
        if count < len(words)/2:
            words_text_half_one.textLine(w.upper())
        else:
            words_text_half_two.textLine(w.upper())
        count += 1
    c.drawText(words_text_half_one)
    c.drawText(words_text_half_two)
    c.showPage()
    c.save()

width = 17
height = 17
another = True

while(another):
    filename = input("word input filename: ")
    output_filename = input("PDF output filename: ")
    title = input("PDF title: ")
    background = input("Background image: ")
    if output_filename == "":
        output_filename = "output.pdf"
    
    f = open(filename,"r")
    words = [line.rstrip() for line in f]
    f.close()

    locs = random.sample(range(0,width*height-1),len(words))
    wordCount = 0
    grid = [[" "] * height for i in range(width)] #wordsearch is currently filled w spaces
    insertedWords = []
    for location in locs:
        x = location % width
        y = location // width
        #try to place the word in that spot
        isInserted = False;
        while not isInserted and x < len(grid) and y < len(grid[0]):
            isInserted = insert_word(grid, words[wordCount].upper(), x,y)
            x += 1
            if x >= len(grid):
                x = 0
                y += 1
        if not isInserted:
            print("WARNING: " + words[wordCount].upper() + " COULD NOT BE INSERTED")
        else:
            insertedWords.append(words[wordCount])
        wordCount += 1
    if background == "":
        writeOutput(grid,width,height,insertedWords, title, output_filename)
    else:
        writeOutput(grid, width, height, insertedWords, title, output_filename, background)
    
    a = input("Make another wordsearch?[Y/N] ")
    if a == 'n' or a == 'N':
        another = False;
