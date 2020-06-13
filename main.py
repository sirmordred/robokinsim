import sys
import pygame
import math
from pygame import freetype

def main(argv):
    pygame.init()

    # colors
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)

    gameDisplay = pygame.display.set_mode((800,600))

    first_motor_center = (400,300)
    arm1_len = 200 # first motor's arm lenght
    arm2_len = 240 # second motor's arm lenght
    a2 = arm1_len
    a4 = arm2_len

    normal_j11 = float(0)
    normal_j12 = float(0)
    normal_j21 = float(0)
    normal_j22 = float(0)
    dt = 0  # dt is the time since the last clock.tick call in seconds.
    time = 0
    angle1 = math.radians(0) # in radian
    angle1_per_second = 30 # degree/second, not radian, 30 is initially given as randomly so not important
    angle2 = math.radians(90) # in radian
    angle2_per_second = 30 # degree/second, not radian, 30 is initially given as randomly so not important
    # XXX Note 0 degree(first motor) and 90 degree(sec motor) intially were given because otherwise(0,0 degree) multiplier calculation crashes with 'ZeroDvisionException'
    fps = 30 
    clock = pygame.time.Clock()
    FONT = freetype.Font(None, 32)
    WHITE = pygame.Color('white')

    end_effector_points = []
    requested_speed = 400
    requested_angle = 270 # XXX important: draw straight line with 270 degree slope with speed 400
    x_dot = requested_speed*math.cos(math.radians(requested_angle))
    y_dot = requested_speed*math.sin(math.radians(requested_angle))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        time += dt
        # clear screen
        gameDisplay.fill(black)

        # calculate and update positions
        normal_j11 = (-a4*math.sin(angle1)*math.cos(angle2)) - (a4*math.cos(angle1)*math.sin(angle2)) - (a2*math.sin(angle1))
        normal_j12 = (-a4*math.sin(angle1)*math.cos(angle2)) - (a4*math.cos(angle1)*math.sin(angle2))
        normal_j21 = (a4*math.cos(angle1)*math.cos(angle2)) - (a4*math.sin(angle1)*math.sin(angle2)) + (a2*math.cos(angle1))
        normal_j22 = (a4*math.cos(angle1)*math.cos(angle2)) - (a4*math.sin(angle1)*math.sin(angle2))
        
        multiplier=1.0/((normal_j11*normal_j22) - (normal_j12*normal_j21))
        inverted_j11 = multiplier*normal_j22
        inverted_j12 = multiplier*(-normal_j12)
        inverted_j21 = multiplier*(-normal_j21)
        inverted_j22 = multiplier*normal_j11
        
        theta1_dot = inverted_j11*x_dot + inverted_j12*y_dot # first motor's calculated angular speed
        theta2_dot = inverted_j21*x_dot + inverted_j22*y_dot # second motor's calculated angular speed

        angle1 += math.radians(theta1_dot) * dt
        angle2 += math.radians(theta2_dot) * dt
        # draw all elements
        pygame.draw.circle(gameDisplay, green, (400,300), 15) # first motor
        x = first_motor_center[0] + math.cos(angle1) * arm1_len # end point of first motor's arm
        y = first_motor_center[1] + math.sin(angle1) * arm1_len
        pygame.draw.line(gameDisplay, blue, first_motor_center, (x,y), 5) # first motor arm
        FONT.render_to(gameDisplay, (50, 50), str(round(time, 2)), WHITE)
        
        pygame.draw.circle(gameDisplay, red, (int(round(x)),int(round(y))), 15) # second motor
        x2 = x + math.cos(angle2) * arm2_len # end point of second motor's arm
        y2 = y + math.sin(angle2) * arm2_len
        end_effector_points.append((int(round(x2)),int(round(y2)))) # pencil is on the end effector
        pygame.draw.line(gameDisplay, yellow, (x,y), (x2,y2), 5) # second motor arm

        for point in end_effector_points:
            pygame.draw.circle(gameDisplay, white, (point[0],point[1]), 2) # draw points which end effector passed through
        
        dt = clock.tick(fps) / 1000  # / 1000 to convert it to seconds.
        pygame.display.update()

if __name__ == "__main__":
    main(sys.argv)