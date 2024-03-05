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


name = 'Hello..'
T = 20

def draw_ref_plane():
    glColor3d(0.6, 0.5, 0.9);
    glBegin(GL_QUADS);
    glVertex3f(100, 100, -5);
    glVertex3f(100, -100, -5);
    glVertex3f(-100, -100, -5);
    glVertex3f(-100, 100, -5);
    glEnd();
    glPointSize(20);
    glColor3d(1, 0, 0);
    glBegin(GL_POINTS);
    glVertex3f(100, 100, -5);
    glVertex3f(100, -100, -5);
    glVertex3f(-100, -100, -5);
    glVertex3f(-100, 100, -5);
    glEnd()

def setting_default_config():
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


def setting_light_config():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.9, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])


def get_quadric(far=1000., origin=30):
    cur_quadric = gluNewQuadric() 
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90., window_size[0]/window_size[1], 0.1, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(origin, 1, 0, 0, 0, 0, origin, 1, 0)
    return cur_quadric


def main_drawing(cur_quadric, time1=None, time2=None):
    glPushMatrix()
    line_mode, cps, t_elements, cp_num = read_datafile()
    points = draw_splines(cps, line_mode, t_elements)
    draw_surface(points, cp_num)

    glPopMatrix()
    return

def read_datafile(path="coke_bottle.txt"):
# def read_datafile(path="data_file.txt"):
    df = open(path).read()
    df = df.split("\n")
    df = [line.split("#")[0] for line in df]
    line_mode = df[0]
    line_mode = line_mode.replace(" ", "")
    cross_section = int(df[1].replace(" ", ""))
    cp_num = int(df[2].replace(" ", ""))
    cps = []
    t_elements = []
    extra_whitespace = 0
    for i in range(cross_section):
        cp_idx = 4+i*cp_num + i*4 + extra_whitespace
        while df[cp_idx] == "":
            cp_idx += 1
            extra_whitespace += 1
        cp = df[cp_idx : cp_idx + cp_num]
        cp_group = []
        for ccp in cp:
            one_cp = []
            for ccpp in ccp.split(" "):
                if ccpp != "":
                    one_cp.append(float(ccpp))
            cp_group.append(one_cp)
        cps.append(cp_group)
        if len(df) > 4 + (i+1)*cp_num + i*3 + 3:
            t_idx = cp_idx + cp_num
            ts = df[t_idx : t_idx + 3]
            s = float(ts[0].replace(" ", ""))
            r = []
            for t1 in ts[1].split(" "):
                if t1 != "":
                    r.append(float(t1))
            t = []
            for t2 in ts[2].split(" "):
                if t2 != "":
                    t.append(float(t2))
            t_elements.append([s, r, t])
    return line_mode, cps, t_elements, cp_num


def draw_splines(cps, line_mode, t_elements):
    glPushMatrix()
    points = []
    for i in range(len(cps)):
        control_points = cps[i]+ cps[i][:4]

        if i < len(t_elements):
            glPushMatrix()##########################################################
            s = t_elements[i][0]
            if s == 0:
                s = 1
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix() ######### ########3 ########
            glLoadIdentity()
            glTranslatef(*t_elements[i][2])
            glRotatef(*t_elements[i][1])
            glScalef(s,s,s)
            mat = glGetFloatv(GL_MODELVIEW_MATRIX)
            glPopMatrix() ######### ########3 ########
            glTranslatef(*t_elements[i][2])
            glRotatef(*t_elements[i][1])
            glScalef(s,s,s)
            
        for rot in range(len(cps[i])): # 그룹당 cp 개수
            control_point_group = control_points[rot:rot+4]
            spline_points = splines(line_mode, control_point_group, i, cps)
            point = get_word_coor(mat, spline_points)
            points.append(point)
        glPopMatrix()##########################################################
    glPopMatrix()
    return points        


def get_word_coor(mat, spline_points):
    points = []
    for spline_point in spline_points:
        x = spline_point[0]
        y = 0
        z = spline_point[1]
        xNew = mat[0][0] * x + mat[1][0] * y + mat[2][0] * z + mat[3][0];
        yNew = mat[0][1] * x + mat[1][1] * y + mat[2][1] * z + mat[3][1];
        zNew = mat[0][2] * x + mat[1][2] * y + mat[2][2] * z + mat[3][2];
        points.append((xNew, yNew, zNew))
    return points

def draw_surface(points, cp_num):
    try:
        points = np.reshape(points, (len(points)//cp_num, cp_num*len(points[0]), 3))
    except:
        return 0
    for i in range(len(points)-1):
        
        for j in range(len(points[i])-1):
            glColor3d( abs(1-2*j/len(points[i])), 0.8*abs(1-2*j/len(points[i])),  1-abs(1-2*j/len(points[i])));
            glBegin(GL_TRIANGLES)
            glVertex3f(*points[i][j])
            glVertex3f(*points[i][j+1])
            glVertex3f(*points[i+1][j])
            glEnd()
            glBegin(GL_TRIANGLES)
            glVertex3f(*points[i][j+1])
            glVertex3f(*points[i+1][j+1])
            glVertex3f(*points[i+1][j])
            glEnd()
        

def draw_spline_points(points):
    glPointSize(5);
    glBegin(GL_POINTS);
    glColor3d(0, 1, 1);
    points = np.reshape(points, (len(points)//4, 4*len(points[0]), 3))
    for points_in_a_line in points:
        for point in points_in_a_line:
            # point = [ppp for pp in point for ppp in pp]
            glVertex3f(*point)
    glEnd();


def get_ratio(t, a, b, c, d):
    return a*t**3 + b*t**2 + c*t + d


def b_spline(cp_group):
    n = 50
    derta = 1.0/n
    glPointSize(2)
    spline_points = []
    glBegin(GL_LINE_STRIP)
    for i in range(0, n+1):
        t = derta * i
        ratio = [
            1/6*get_ratio(t, -1, 3, -3, 1),
            1/6*get_ratio(t, 3, -6, 0, 4),
            1/6*get_ratio(t, -3, 3, 3, 1),
            1/6*get_ratio(t, 1, 0, 0, 0)
        ]
        x, z = 0., 0.
        for j in range(len(cp_group)):
            x += ratio[j] * cp_group[j][0]
            z += ratio[j] * cp_group[j][1]
        # glVertex3f(x, 0., z)
        spline_points.append((x, z))
    glEnd()
    return spline_points


def catmull_rom(cp_group):
    n = 50
    derta = 1.0/n
    glPointSize(2)
    spline_points = []
    glBegin(GL_LINE_STRIP)
    for i in range(0, n+1):
        t = derta * i
        ratio = [
            get_ratio(t, -0.5, 1, -0.5, 0),
            get_ratio(t, 1.5, -2.5, 0, 1),
            get_ratio(t, -1.5, 2, 0.5, 0),
            get_ratio(t, 0.5, -0.5, 0, 0)
        ]
        x, z = 0., 0.
        for j in range(len(cp_group)):
            x += ratio[j] * cp_group[j][0]
            z += ratio[j] * cp_group[j][1]
        # glVertex3f(x, 0., z)
        spline_points.append((x, z))
    glEnd()  
    return spline_points

def draw_points(cps):
    glPointSize(5);
    glColor3d(1, 0, 0);
    glBegin(GL_POINTS);
    for i, cp_group in enumerate(cps):
        for cp in cp_group:
            glColor3d(1, i/len(cps), 0);
            glVertex3f(cp[0], cp[1], 0);
    glEnd();
    glLineWidth(2);
    glBegin(GL_LINE_STRIP);
    for i, cp_group in enumerate(cps):
        for cp in cp_group:
            glColor3d(0, i/len(cps), 1);
            glVertex3f(cp[0], cp[1], 0);
    glEnd();


def splines(line_mode, control_point_group, i, cps):
    if line_mode == "BSPLINE":
        glColor3d(1, i/len(cps), 0)
        spline_points = b_spline(control_point_group)
    elif line_mode == "CATMULL_ROM":
        spline_points = catmull_rom(control_point_group)
    else:
        print("line mode should be BSPLINE or CATMULL_ROM")
    return spline_points



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
            glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

            users_axis = get_users_axis(keypress, cur_quadric, users_axis=users_axis)

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