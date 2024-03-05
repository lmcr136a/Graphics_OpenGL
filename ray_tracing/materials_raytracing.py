import numpy as np


plane = 0

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position), 
        radius=np.array(radius), color=np.array(color), reflection=.5,
        amb=0, dif=0, spe=0, spe_k=0)

def silver_ball(R=0.3):
    ball = add_sphere([0.3, R-plane, 0.5], R, [1,1,1])
    amb, dif, spe, shine = silver()
    ball["amb"]=amb
    ball["dif"]=dif
    ball["spe"]=spe
    ball["spe_k"]=shine*100
    ball["reflection"] = shine
    return ball


def emerald_ball(R=0.22):
    ball = add_sphere([-0.3, R-plane, 0.6], R, [0.2, 0.9, 0.8])
    amb, dif, spe, shine = silver()
    ball["amb"]=amb
    ball["dif"]=dif
    ball["spe"]=spe
    ball["spe_k"]=shine*100
    ball["reflection"] = shine
    return ball

def yellow_rubber_ball(R=0.1):
    ball = add_sphere([-0.2, R-plane, 0.9], R, [1., 0.7, 0.1])
    amb, dif, spe, shine = yellow_rubber()
    ball["amb"]=amb
    ball["dif"]=dif
    ball["spe"]=spe
    ball["spe_k"]=shine*100
    ball["reflection"] = shine
    return ball

def black_plastic_ball(R=0.1):
    ball = add_sphere([0.25, R-plane, 0.99], R, [0., 0, 0])
    amb, dif, spe, shine = black_plastic()
    ball["amb"]=amb
    ball["dif"]=dif
    ball["spe"]=spe
    ball["spe_k"]=shine*100
    ball["reflection"] = shine
    return ball


def yellow_rubber():
    amb = [0.05, 0.05, 0.]
    dif = [0.5, 0.5, 0.4]
    spe = [0.7, 0.7, 0.04]
    shine = 0.0078125
    return amb, dif, spe, shine

def emerald():
    amb = [0.0215, 0.1745, 0.0215]
    dif = [0.07568, 0.61424, 0.07568]
    spe = [0.633, 0.727811, 0.633]
    shine = 0.7
    return amb, dif, spe, shine

def black_plastic():
    amb = [0., 0., 0.]
    dif = [0.01, 0.01, 0.01]
    spe = [0.50, 0.50, 0.50]
    shine = 0.25
    return amb, dif, spe, shine

def pearl():
    amb = [0.25, 0.20725, 0.20725]
    dif = [1, 0.829, 0.829]
    spe = [0.296648, 0.296648, 0.296648]
    shine = 0.088
    return amb, dif, spe, shine


def ruby():
    amb = [0.1745, 0.01175, 0.01175]
    dif = [0.61424, 0.04136, 0.04136]
    spe = [0.727811, 0.626959, 0.626959]
    shine = 0.6
    return amb, dif, spe, shine


def silver():
    amb = [0.19225, 0.19225, 0.19225]
    dif = [0.50754, 0.50754, 0.50754]
    spe = [0.508273, 0.508273, 0.508273]
    shine = 0.4
    return amb, dif, spe, shine


def jade():
    amb = [0.135,	0.2225,	0.1575]
    dif = [0.54,	0.89,	0.63]
    spe = [0.316228,	0.316228,	0.316228]
    shine = 0.1
    return amb, dif, spe, shine