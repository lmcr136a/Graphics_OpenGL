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
from materials import *

n = 1

def read_datafile(path="data_file.txt"):
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
    vertex_list = []
    for i in range(len(points)-1):
        
        for j in range(len(points[i])-1):
            
            glColor3d( 0.8*abs(1-2*j/len(points[i])), 0.5,  0.8*(1-abs(1-2*j/len(points[i]))));
            # glColor3d( abs(1-2*j/len(points[i])), 0.8*abs(1-2*j/len(points[i])),  1-abs(1-2*j/len(points[i])));
            ruby()
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
            
            vertex_list.append([points[i][j], points[i][j+1], points[i+1][j]])
            vertex_list.append([points[i][j+1], points[i+1][j+1], points[i+1][j]])
    with open('bird.npy', 'wb') as f:
        np.save(f, np.array(vertex_list))
    exit()

        

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

