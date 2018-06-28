
from layerouter import *

edgeInts=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6), (6,7), (7,8),(8,9),(9,6)]
cones={}
spheres={}
labels={}

edges = [{'source' : str(s), 'target' : str(t)} for s, t in edgeInts]

def getIDs(edges):
    IDs=[]
    for t in edges:
        IDs.append(str(t[0]))
        IDs.append(str(t[1]))
    return set(IDs)

IDs = getIDs(edgeInts) #IDs are strings: '2'

showLabels=False
niceColor=color.orange

V=vector
def randShift():
    return V(random()-0.5, random()-0.5, 0)

def randVec():
    return V(random(),random(), random())

def upTune(v): #lighten color so one component =1
    m = max(v.x,v.y,v.z)
    v= v*1/m
    return v

def similar(c):
    return upTune(c + randVec())
 

#make spheres and labels
for ID in IDs:
    spheres[ID] = sphere(color=randVec())
    spheres[ID].kids = 0
    labels[ID]  = label(text=ID, visible=showLabels)

def edgeUtil(edge): #eID for '1' -> '2' is '1.2'
    s,t = edge['source'], edge['target']
    return s,t, s+'.'+t

#make cones
for edge in edges:
    s,t,eID = edgeUtil(edge)
    cones[eID]= cone(pos=spheres[s].pos, axis=spheres[s].pos - spheres[t].pos)
    cones[eID].color = upTune(spheres[s].color + spheres[t].color)
    spheres[s].kids += 1


#sphere volume proportional to descendants
def cube_root(num):
    return num ** (1. / 3)
def getRadius(volume):
    return cube_root( ((1+volume) / pi)  * (3./ 4) )

def updateSpheres(nodes):
    for k,v in oItems(nodes):
        x,y,z = v['velocity']
        spheres[k].pos = vector(x,y,z)
        spheres[k].radius = getRadius(spheres[k].kids)
        labels[k].pos  = spheres[k].pos

def update(nodes, edges):
     updateSpheres(nodes)
     for eID in oKeys(cones):
         s,t = eID.split('.')
         cones[eID].pos = spheres[s].pos
         cones[eID].axis= spheres[t].pos - spheres[s].pos
         cones[eID].radius= spheres[s].radius


# Generate nodes
params={'edges':edges,
        'iterations'    : 300,
        'update'        : update,
        'is_3D'         : False,
        'force_strength': 5.0,
        'dampening'     : 0.01,
        'max_velocity'  : 2.0,
        'max_distance'  : 50}


nodes = run(params)
