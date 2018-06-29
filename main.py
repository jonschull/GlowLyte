from vpython import *
from layerouter import *

edgeInts=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6), (6,7), (7,8),(8,9),(9,6),(9,10),(9,11),(9,12)]
edgeIDs = [(  str(t[0])+'.'+ str(t[1]) ) for t in edgeInts] #eids  ['1.2', '2.3', '3.1'...
nodeIDs = list(set('.'.join(edgeIDs).split('.')))           #nIds  ['8', '7', '3',

cones={}
spheres={}
labels={}
showLabels=False 

####color utils
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

def newSphere(ID):
    spheres[ID] = sphere(color=randVec())
    spheres[ID].kidIDs = []
    spheres[ID].label = label(text=ID, visible=showLabels)
    return spheres[ID]

def newCone(eID):
    s,t = eID.split('.')
    cones[eID]= cone(pos=spheres[s].pos, axis=spheres[s].pos - spheres[t].pos)
    cones[eID].color = upTune(spheres[s].color + spheres[t].color)
    spheres[s].kidIDs.append(eID.split('.')[1])
    return cones[eID]

#make spheres and labels
for ID in nodeIDs:
    newSphere(ID)

#make cones after spheres exist
for eID in edgeIDs:
    newCone(eID)

#sphere volume proportional to descendants
def cube_root(num):
    return num ** (1. / 3)

def getRadius(sphere):
    volume = len(sphere.kidIDs)
    return cube_root( ((1+volume) / pi)  * (3./ 4) )

def updateSpheres(nodes):
    for k,v in oItems(nodes):
        x,y,z = v['velocity']
        spheres[k].pos = vector(x,y,z)
        spheres[k].radius = getRadius(spheres[k]) *1.5
        spheres[k].label.pos  = spheres[k].pos

def update(nodes): #function passed in to run(params)
    global n
    updateSpheres(nodes)
    for eID in oKeys(cones):
        s,t = eID.split('.')
        cones[eID].pos = spheres[s].pos
        cones[eID].axis= spheres[t].pos - spheres[s].pos
        cones[eID].radius= spheres[s].radius

# Generate nodes
params={'edgeIDs': edgeIDs,
        'iterations'    : 40,
        'update'        : update,
        'is_3D'         : False,
        'force_strength': 5.0,
        'dampening'     : 0.01,
        'max_velocity'  : 2.0,
        'max_distance'  : 50}

def giveBirth(eID): 
    s,t = eID.split('.')
    edgeInts.append((int(s), int(t)))
    nodeIDs.append(t)
    edgeIDs.append(eID)
    params['edgeIDs'] = edgeIDs
    kid = newSphere(t)
    kid.pos = spheres[s].pos
    newCone(eID)
    nodes[t] ={}
    nodes[t]['velocity'] = nodes[s]['velocity']
    nodes[t]['force']    = nodes[s]['force']

nodes={}
nodes = run(nodes, params)
for i in range(5):
    print('round ', i)
    if i==2:
        print(edgeIDs)
        giveBirth('12.13')
        giveBirth('12.14')
 
        print(edgeIDs)
    run(nodes, params)  
