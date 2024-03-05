import numpy as np
# import cupy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from fixed_funcs import *
from materials_raytracing import *

w = 400
h = 300


def intersect_polygon(O, D, vertexes, N):
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    nd = np.dot(N, np.mean(vertexes, axis=0)-N)
    d = np.dot(nd - O, N) / denom

    point = Point(O+d*D)
    polygon = Polygon(vertexes)
    if d < 0 or not polygon.contains(point):
        return np.inf
    return d

    
def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'polygon':
        return intersect_polygon(O, D, obj['vertexes'], obj['normal'])


def trace_ray(rayO, rayD):
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    if t == np.inf:
        return
    obj = scene[obj_idx]
    M = rayO + rayD * t
    N = get_normal(obj, M)
    color = get_color(obj, M)
    toL1 = normalize(L1 - M)
    toL2 = normalize(L2 - M)
    toL3 = normalize(L3 - M)
    toO = normalize(O - M)
    l = [intersect(M + N * .0001, toL1, obj_sh) 
            for k, obj_sh in enumerate(scene) if k != obj_idx]
    if l and min(l) < np.inf:
        return


    col_ray = np.array(obj.get('amb', ambient))
    col_ray = np.array(obj.get('dif', diffuse_c)) * np.max(np.dot(N, toL1), 0) * color + col_ray
    col_ray = np.array(obj.get('spe', specular_c)) * max(np.dot(N, normalize(toL1 + toO)), 0) ** obj.get('spe_k', specular_k) * color_light + col_ray
    

    return obj, M, N, col_ray


def add_polygon(vertexes, color=(1,1,1), M=[0,0,0]):
    N = np.cross(vertexes[1]-vertexes[0], vertexes[2]-vertexes[0])
    r = np.mean(vertexes, axis=0) - np.array(M)
    N = N/np.linalg.norm(N)
    if np.dot(r, N) < 0:
        N *= -1
    return dict(type='polygon', vertexes=vertexes, normal=N,
        color=np.array(color), reflection=0.1,
        amb=[0.135,	0.2225,	0.1575], dif=[0.54,	0.89,	0.63], spe=[0.316228,	0.316228,	0.316228], spe_k=0.1)


poly11 = np.array([
    [1, 1, 0],
    [0,0,0],
    [1, 0, 0]
])
poly12 = np.array([
    [1, 1, 0],
    [0,0,0],
    [0, 1, 0]
])

poly21 = np.array([
    [0, 1, 1],
    [0,0,0],
    [0, 1, 0]
])
poly22 = np.array([
    [0, 1, 1],
    [0,0,0],
    [0, 0, 1]
])

poly31 = np.array([
    [1, 0, 1],
    [0,0,0],
    [0, 0, 1]
])
poly32 = np.array([
    [1, 0, 1],
    [0,0,0],
    [1, 0, 0]
])


def load_poly_obj(path="bird.npy"):
    polyarr =  np.load(path)
    polylist = []
    xscale = np.max([np.abs(np.max(polyarr[:, :, 0])), np.abs(np.min(polyarr[:, :, 0]))])
    yscale = np.max([np.abs(np.max(polyarr[:, :, 1])), np.abs(np.min(polyarr[:, :, 1]))])
    zscale = np.max([np.abs(np.max(polyarr[:, :, 2])), np.abs(np.min(polyarr[:, :, 2]))])
    xmean = np.mean(polyarr[:, :, 0])
    ymean = np.mean(polyarr[:, :, 1])
    zmean = np.mean(polyarr[:, :, 2])
    
    transf = np.array([-xmean/xscale, -ymean/yscale, zmean/zscale])
    print(len(polyarr))


    figure = False
    if figure:
        fig = plt.figure()
        ax = fig.gca(projection='3d')

    c =0
    e = 0.01
    for i, poly in enumerate(polyarr[:30]):
        if np.sum(np.abs(poly[0] - poly[1]))< e or\
           np.sum(np.abs(poly[1] - poly[2]))<e or\
           np.sum(np.abs(poly[0] - poly[2]))<e:
            c += 1
            continue
        scaled = poly/np.array([xscale, yscale, zscale]) + transf
        scaled *= 30
        scaled -= np.array([3.5, 11.5, 0])
        print(i, scaled, "    c: ", c)
        polylist.append(add_polygon(scaled, np.mean(scaled, axis=0)))

        if figure:
            ax.plot([scaled[0][0], scaled[1][0]], [scaled[0][1],scaled[1][1]],zs=[scaled[0][2],scaled[1][2]])
            ax.plot([scaled[1][0], scaled[2][0]], [scaled[1][1],scaled[2][1]],zs=[scaled[1][2],scaled[2][2]])
            ax.plot([scaled[2][0], scaled[0][0]], [scaled[2][1],scaled[0][1]],zs=[scaled[2][2],scaled[0][2]])
    if figure:
        plt.xlabel("X--")
        plt.ylabel("Y--")
        plt.show()
        exit()

    
    print(len(polyarr), "    c: ", c)
    return polylist



# List of objects.
scene = [
    add_plane([0., -1, 0.], [0., 1., 0.]),
    silver_ball(),
    emerald_ball(),
    yellow_rubber_ball(),
    black_plastic_ball(),
    ]
transf = np.array([-0.3, 0, -0.9])
scene +=[
    add_polygon(poly11+transf),
    add_polygon(poly12+transf),
    add_polygon(poly21+transf),
    add_polygon(poly22+transf),
    add_polygon(poly31+transf),
    add_polygon(poly32+transf),

    add_polygon(poly11+np.array([0,0,1]+transf)),
    add_polygon(poly12+np.array([0,0,1]+transf)),
    add_polygon(poly21+np.array([1,0,0]+transf)),
    add_polygon(poly22+np.array([1,0,0]+transf)),
    add_polygon(poly31+np.array([0,1,0]+transf)),
    add_polygon(poly32+np.array([0,1,0]+transf)), 
]
# Light position and color.
L1 = np.array([2., 5., 1.])
color_light = np.ones(3)
L2 = np.array([-5., 5., -1.])
color_light = np.ones(3)
L3 = np.array([0., 0., 3.])
color_light = np.ones(3)

# Default light and material parameters.
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
O = np.array([0., 1.5, 10.])  # Camera.
Q = np.array([0., 0., 0.])  # Camera pointing to.
img = np.zeros((h, w, 3))

r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)

start = time.time()
# Loop through all pixels.
for i, x in enumerate(np.linspace(S[0], S[2], w)):
    if i % 5 == 0:
        print( i / float(w) * 100, "%    ", round((time.time() - start)/60, 2), "분")
        # if i / float(w) * 100 > 60:
        #     break
    for j, y in enumerate(np.linspace(S[1], S[3], h)):
        col[:] = 0  
        Q[:2] = (x, y)
        D = normalize(Q - O)
        depth = 0
        rayO, rayD = O, D
        reflection = 1.
        # Loop through initial and secondary rays.
        while depth < depth_max:
            traced = trace_ray(rayO, rayD)
            if not traced:
                break
            obj, M, N, col_ray = traced
            # Reflection: create a new ray.
            rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
            depth += 1
            col += reflection * col_ray
            reflection *= obj.get('reflection', 1.)
        img[h - j - 1, i, :] = np.clip(col, 0, 1)
plt.imsave(f'fig_{str(time.time())[:9]}.png', img)