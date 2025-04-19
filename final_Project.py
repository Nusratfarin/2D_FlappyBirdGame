from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

dx = 0
dy = 0
d = 0
y = 0
incE = 0
incNE = 0

zone0_x1 = 0
zone0_x2 = 0
zone0_y1 = 0
zone0_y2 = 0



array = []
collision_bird = []

zone0,zone1, zone2, zone3, zone4, zone5, zone6, zone7 = False, False, False, False, False, False, False, False

score = 0
pause = False
game_over = False
click = 0

pillar_collection=[[400,random.randint(275,325)],[275,random.randint(275,325)],[150,random.randint(275,325)]]
collision_pillar=[]
bird_y_move = 0

def draw_points(x, y, colour = None):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    if colour == None:
        glColor3f(1.0, 1.0, 0.0)
    else:
        glColor3f(colour[0], colour[1], colour[2])
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
    glutPostRedisplay()

def draw_circle(center_x, center_y, radius):
    d = 1- radius
    x = 0
    y = radius
    array = [(x, y)]
    while x < y:
        if d < 0:
            d = d + 2*x + 3
            x += 1
        else:
            d = d + 2*x - 2*y + 5
            x += 1
            y -=1
        array.append((x, y))
    array1 = []
    for x, y in array:
        array1.append((x, y))
        array1.append((y, x))
        array1.append((y, -x))
        array1.append((x, -y))
        array1.append((-x, -y))
        array1.append((-y, -x))
        array1.append((-y, x))
        array1.append((-x, y))
    for i in range(len(array1)):
        array1[i] = (array1[i][0] + center_x, array1[i][1] + center_y)
    for x, y in array1:
        draw_points(x,y)

    glutPostRedisplay()

def draw_line(x1, y1, x2, y2, colour = None):
    global dx, dy, d, y, incE, incNE, zone0_x1, zone0_x2, zone0_y1, zone0_y2, zone0, zone1, zone2, zone3, zone4, zone5, zone6, zone7, array
    array = []
    dx = x2 - x1
    dy = y2 - y1

    if dy == 0:
        if x1 < x2:
            for x in range(x1, x2+ 1):
                draw_points(x, y1, colour)
        else:
            for x in range(x2, x1+ 1):
                draw_points(x, y1, colour)
    elif dx == 0:
        if y1 < y2:
            for y in range(y1, y2+ 1):
                draw_points(x1, y, colour)
        else:
            for y in range(y2, y1+ 1):
                draw_points(x1, y, colour)

    else:
        if dx > 0:
            if dy > 0:
                if abs(dx) > abs(dy): #Zone 0

                    zone0 = True           
                    zone0_x1 = x1
                    zone0_x2 = x2
                    zone0_y1 = y1
                    zone0_y2 = y2
                else:     
                    zone1 = True            #Zone 1
                    zone0_x1 = y1
                    zone0_x2 = y2
                    zone0_y1 = x1
                    zone0_y2 = x2
            else:
                if abs(dx) > abs(dy): #Zone 7
                    zone7 = True 
                    zone0_x1 = x1
                    zone0_x2 = x2
                    zone0_y1 = -y1
                    zone0_y2 = -y2
                else:       
                    zone6 = True         #Zone 6
                    zone0_x1 = -y1
                    zone0_x2 = -y2
                    zone0_y1 = x1
                    zone0_y2 = x2
        else:
            if dy > 0:                 
                if abs(dx) > abs(dy): 
                    zone3 = True  #Zone 3
                    zone0_x1 = y1
                    zone0_x2 = y2
                    zone0_y1 = -x1
                    zone0_y2 = -x2
                else:  
                    zone2 = True                # Zone 2
                    zone0_x1 = y1
                    zone0_x2 = y2
                    zone0_y1 = -x1
                    zone0_y2 = -x2                

            else: 
                if abs(dx) > abs(dy):
                    zone4 = True   #Zone 4
                    zone0_x1 = -x1
                    zone0_x2 = -x2
                    zone0_y1 = -y1
                    zone0_y2 = -y2
                else:  
                    zone5 = True                 #Zone 5
                    zone0_x1 = -y1
                    zone0_x2 = -y2
                    zone0_y1 = -x1
                    zone0_y2 = -x2

        dx_new = zone0_x2 - zone0_x1
        dy_new = zone0_y2 - zone0_y1
        d = 2 * dy_new - dx_new
        incE = 2 * dy_new
        incNE = 2 * (dy_new -dx_new)
        y = zone0_y1
        for x in range(zone0_x1, zone0_x2+ 1):
            array.append((x,y))
            if d > 0:
                d += incNE
                y += 1
            else:
                d += incE

        for a, b in array:

            if zone0:
                x, y = a, b
            elif zone1:
                x, y = b, a
            elif zone2:
                x, y = -b, a
            elif zone3:
                x, y = -a, b
            elif zone4:
                x, y = -a, -b
            elif zone5:
                x, y = -b, -a
            elif zone6:
                x, y = b, -a
            elif zone7:
                x, y = a, -b
            
            draw_points(x,y, colour)
    zone0, zone1, zone2, zone3, zone4, zone5, zone6, zone7 = False, False, False, False, False, False, False, False
    glutPostRedisplay()
    




def mouseListener(button, state, x, y):
    global score, pause, game_over, bird_y_move, pillar_collection

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 450 <= x <= 490 and 450 <= (500 - y) <= 490:  # Cross
            print("Goodbye! Score:", score)
            glutLeaveMainLoop()
        elif 235 <= x <= 270 and 450 <= (500 - y) <= 490:  # Play/Pause
            pause = not pause  # Toggle pause
            print("Pause:", pause)
        elif 30 <= x <= 70 and 450 <= (500 - y) <= 490:  # Arrow (Restart game)
            score = 0
            game_over = False
            bird_y_move = 0
            pillar_collection = [[400, random.randint(275, 325)],
                                 [275, random.randint(275, 325)],
                                 [150, random.randint(275, 325)]]
            print("Restarting game!")

def keyboardListener(key,x,y):
    global bird_y_move
    if pause == False and game_over == False:
        if key==b' ':
            if game_over == False:
                 bird_y_move += 35
                 if bird_y_move > 150:
                     bird_y_move = 150 

def draw_bird(bird_x, bird_y):
    global collision_bird
    radius = 13
    radius2 = 9

    draw_circle(bird_x, bird_y, radius)                                         # Big circle
    draw_circle(bird_x + 20, bird_y + 10, radius2)                              # Small circle
    draw_line(bird_x - 25, bird_y + 10, bird_x - radius, bird_y)                # Tail up
    draw_line(bird_x - 25, bird_y - 10, bird_x - radius, bird_y)                # Tail down
    draw_line(bird_x - 25, bird_y + 10, bird_x - 25, bird_y - 10)               # Tail side
    draw_line(bird_x + 20, bird_y + 1, bird_x + 38, bird_y + 10)                # Beak down
    draw_line(bird_x + 20, bird_y + 19, bird_x + 38, bird_y + 10)               # Beak up


                        # head                          left leg                               right leg                    front
    collision_bird = [(bird_x + 20, bird_y + 19), (bird_x - 5, bird_y - radius - 6), (bird_x + 5, bird_y - radius - 6), (bird_x + 38, bird_y + 10)]

    glutPostRedisplay()


def draw_pillar():
    global pillar_collection, collision_pillar
    collision_list=[]
    for x,y in pillar_collection:
        x,y=int(x),int(y)
        draw_line(x,y,x+90,y,(1,1,1))
        draw_line(x,y+20,x+90,y+20,(1,1,1))
        draw_line(x,y,x,y+20,(1,1,1))
        draw_line(x+90,y,x+90,y+20,(1,1,1))
        draw_line(x+10,440,x+10,y+20,(1,1,1))
        draw_line(x+80,440,x+80,y+20,(1,1,1))

        draw_line(x, y-100,x+90,y-100,(1,1,1))
        draw_line(x, y-120, x+90, y-120,(1,1,1))
        draw_line(x,y-100, x ,y-120,(1,1,1))
        draw_line(x+90,y-100,x+90, y-120,(1,1,1))
        draw_line(x+10, 0, x+10, y-120,(1,1,1))
        draw_line(x+80, 0, x+80, y-120,(1,1,1))

        for i in range(91):
            collision_list.append([x+i,y])
            collision_list.append([x+i,y-100])
        for i in range(1,21):
            collision_list.append([x,y+i])
            collision_list.append([x+90,y+i])
            collision_list.append([x,y-i-100])
            collision_list.append([x+90,y-i-100])
        for i in range(y+20,441):
            collision_list.append([x+10,i])
            collision_list.append([x+80,i])
        for i in range(y-120,-1,-1):
            collision_list.append([x+10,i])
            collision_list.append([x+80,i])
    collision_pillar=collision_list


def animate():
    glutPostRedisplay()
    global game_over,pause, pillar_collection, score
    lst=[]
    if not game_over:
        if not pause:
            for x,y in pillar_collection:
                if x-1<0:
                    lst.append([400,random.randint(275,325)])
                    score+=1
                    print("Score: ",score)
                else:
                    lst.append([x-1,y])
            pillar_collection=lst
           
            
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_icons():
    global pause
    draw_line(450, 490, 490, 450, (1.0, 0.0, 0.0)) # Drawing the cross
    draw_line(450, 450, 490, 490, (1.0, 0.0, 0.0))

    if pause == True:
        draw_line(240, 450, 240, 490, (0.82, 0.5, 0.22)) # Play button
        draw_line(240, 450, 270, 470, (0.82, 0.5, 0.22))
        draw_line(240, 490, 270, 470, (0.82, 0.5, 0.22))
    else:
        draw_line(235, 450, 235, 490, (0.82, 0.5, 0.22)) # Pause button
        draw_line(265, 490, 265, 450, (0.82, 0.5, 0.22))

    draw_line(30, 470, 70, 470, (0.27, 0.79, 0.79))  # Drawing the arrow ###### Functionalities left
    draw_line(30, 470, 55, 450, (0.27, 0.79, 0.79))
    draw_line(30, 470, 55, 490, (0.27, 0.79, 0.79))

        

    

def showScreen():
    global bird_y_move, game_over, score
    global collision_bird, collision_pillar, pillar_collection



    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    draw_icons()

    x_offset = 20


    draw_pillar()
    draw_bird(75, 250 + bird_y_move)

    if pause == False and game_over == False:
        for x, y in collision_bird:
            for i, j in collision_pillar:
                if x == i and y == j:
                    draw_points(x, y, (1.0, 0, 0))
                    game_over = True

        if game_over:
            print("Game Over! Score: ", score)

        if bird_y_move < -200:
            bird_y_move = -200
            game_over = True
        else:
            bird_y_move -= 1

        glutPostRedisplay()

    glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"tap tap bird") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)

glutMainLoop()