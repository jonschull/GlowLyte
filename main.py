from vpython import *
from layerouter import *

V=vector
    
cones={}
spheres={}
labels={}
labelsVisible=False

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

def newSphere(ID, parent=''):
    if not parent:
        color = randVec()
    else:
        color = similar(spheres[parent].color)
    spheres[ID] = sphere(color=color)
    spheres[ID].kidIDs = []
    spheres[ID].label = label(text=ID, visible=labelsVisible)
    return spheres[ID]

def newCone(eID):
    s,t = eID.split('.')
    cones[eID]= cone(pos=spheres[s].pos)
    cones[eID].axis=spheres[s].pos - spheres[t].pos
    cones[eID].color = spheres[s].color
    spheres[s].kidIDs.append(eID.split('.')[1])
    return cones[eID]

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

def giveBirth(eID): 
    s,t = eID.split('.')
    edgeInts.append((int(s), int(t)))
    nodeIDs.append(t)
    edgeIDs.append(eID)
    params['edgeIDs'] = edgeIDs
    kid = newSphere(t,s)
    kid.pos = spheres[s].pos
    newCone(eID) 
    nodes[t] ={}
    nodes[t]['velocity'] = nodes[s]['velocity']
    nodes[t]['force']    = nodes[s]['force']

def getIDs(edgeInts=[]):
    edgeIDs = [(  str(t[0])+'.'+ str(t[1]) ) for t in edgeInts] # ['1.2', '2.3', '3.1'...
    nodeIDs = list(set('.'.join(edgeIDs).split('.')))           # ['8', '7', '3'...
    return edgeIDs, nodeIDs


if __name__== '__main__':
    edgeInts=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6), (6,7), (7,8),(8,9),(9,6),(9,10),(9,11),(9,12)]
    edgeIDs, nodeIDs = getIDs(edgeInts)

    
    #make spheres and labels
    for ID in nodeIDs:
        newSphere(ID)

    #make cones after spheres exist
    for eID in edgeIDs:
        newCone(eID)

    # Generate nodes
    params={'edgeIDs': edgeIDs,
            'iterations'    : 40,
            'update'        : update,
            'is_3D'         : False,
            'force_strength': 5.0,
            'dampening'     : 0.01,
            'max_velocity'  : 2.0,
            'max_distance'  : 50}

    nodes={}
    run(nodes, params)
    for i in range(3):
        if i==2:
            giveBirth('12.13')
            giveBirth('12.14')
            giveBirth('12.15')
            giveBirth('12.16')
            giveBirth('16.17')
            giveBirth('17.18')
            giveBirth('18.19')
            giveBirth('19.20')

        run(nodes, params)
