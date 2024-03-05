from math import degrees
import sys
import numpy as np
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from pygame.locals import *
from PIL import Image as Image

from dog_model import *
from view_functions import *
from bird import *
from main_drawing import main_drawing

from cube_map import *


name = 'Hello..'
T = 20


def setting_default_config():
    glEnable(GL_DEPTH_TEST);
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


def setting_light_config():
    ambient0 = np.array([1., 0., 0., 0.])
    ambient1 = np.array([0., 0., 1., 0.])
    ambient2 = np.array([0., 1., 0., 0.])
    diffuse = np.array([1,1,1,0])

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 40, -70, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, 0.6*diffuse)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, 0.6*diffuse)

    glLightfv(GL_LIGHT1, GL_POSITION, [-1, 0, 0, 0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, 0.3*ambient0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, 0.3*ambient0)
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1,1,1, 0))

    glLightfv(GL_LIGHT2, GL_POSITION, [1, 0, 0, 0])
    glLightfv(GL_LIGHT2, GL_AMBIENT, 0.3*ambient1)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, 0.3*ambient1)
    glLightfv(GL_LIGHT2, GL_SPECULAR, (1,1,1, 0))



def get_quadric(far=1000., origin=120):
    cur_quadric = gluNewQuadric() 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90., window_size[0]/window_size[1], 0.1, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, -40, origin, 0, 0, 0, 0, 1, origin+20)
    return cur_quadric


def main():  #####################################
    glutInit(sys.argv)
    pygame.init()
    scree = pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
    
    far = 10000.

    setting_default_config()
    setting_light_config()
    cur_quadric = get_quadric(far=far)

    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    ##############################################
    displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
    clicked = False
    rotatings = [[(0,0,1), 0]]
    cur_rotating = None
    startpoint = [0,0]
    users_axis = None
    fov = 45.
    
    run = True
    time1 = 0.0
    paused = False
    while run: ##################################
        paused, run = handle_pause_and_quit(displayCenter, paused, run) 

        if not paused:
            keypress = pygame.key.get_pressed()
            fov =  handle_zoom(keypress, fov, far=far)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            glPushMatrix()

            # 이동, 좌우움직임
            handle_movement(keypress)

            # 변환 적용 / pop matrix / 적용
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            # 조명
            glEnable(GL_LIGHTING);
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHT1)
            glEnable(GL_LIGHT2)

            users_axis = get_users_axis(keypress, cur_quadric, users_axis=users_axis)

            textname = load_cubemap_texture(PARAM=GL_OBJECT_LINEAR) ##############
            draw_skybox(textname)
            
            # rotating
            if pygame.mouse.get_pressed()[0]:
                endpoint = get_mouse_position()
                if not clicked:  # 딸
                    clicked = True
                    startpoint = endpoint

            elif clicked and not pygame.mouse.get_pressed()[0]:  # 깍
                clicked = False
                users_axis = None
                rotatings.append(cur_rotating)
            cur_rotating = rotate_view(startpoint, rotatings, keypress, users_axis)

            
            # 본격 그리기
            main_drawing(cur_quadric, time1)
                            # users axis

            if not keypress[pygame.K_e]:
                for l in range(len(rotatings)):
                    glPopMatrix()
                if pygame.mouse.get_pressed()[0]:
                    glPopMatrix()
            time1 += 1

            pygame.display.flip()
            pygame.time.wait(10)
    pygame.quit()


if __name__ == '__main__':
    main()