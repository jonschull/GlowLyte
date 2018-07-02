from vpython import *
from layerouter import *

V=vector

cones={}
spheres={}
labels={}
labelsVisible=0
nodes={}


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

def newCone(eID):
    s,t = eID.split(':')
    cones[eID]= cone(pos=spheres[s].pos)
    cones[eID].axis=spheres[t].pos - spheres[s].pos
    cones[eID].color = spheres[s].color
    cones[eID].label = label(text = eID, visible=False)
    spheres[s].kidIDs.append(eID.split(':')[1])
    return cones[eID]

#sphere volume proportional to descendants
def cube_root(num):
    return num ** (1. / 3)

def getRadius(sphere):
    volume = descendants(sphere.ID)
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
        s,t = eID.split(':')
        cones[eID].pos = spheres[s].pos
        cones[eID].axis= spheres[t].pos - spheres[s].pos
        cones[eID].radius= spheres[s].radius


def newSphere(ID, parentID=''):
    if not parentID:
        color = randVec()
    else:
        color = similar(spheres[parentID].color)
        
    embryo = sphere(color=color)
    
    embryo.ID = ID
    embryo.ancestorIDs=[]
    if parentID:
        embryo.ancestorIDs.append(parentID)

    embryo.kidIDs = []
    embryo.label = label(text=ID, visible=labelsVisible)
    
    spheres[ID]=embryo
    return spheres[ID]


def giveBirth(eID): #assumes the source sphere exists
    s,t = eID.split(':') 
    nodeIDs.append(t)
    edgeIDs.append(eID)

    kid = newSphere(t,s)
    kid.pos = spheres[s].pos

    parent = spheres[s]
    kid.ancestorIDs = [s] + parent.ancestorIDs

    newCone(eID)
    nodes[t] ={}
    nodes[t]['velocity'] = nodes[s]['velocity']
    nodes[t]['force']    = nodes[s]['force']


def showLabels():
    for sphere in oValues(spheres):
        sphere.label.visible=True
def hideLabels():
    for sphere in oValues(spheres):
        sphere.label.visible=False

def descendants(ID):
    return len([sphere for sphere in oValues(spheres) if ID in sphere.ancestorIDs])


def clickHandler(event):
    hit=None
    try:
        hit = scene.mouse.pick.label.text
    except Exception as e:
       hit='no_hit'
    if hit:
        print(event.event, hit)

scene.bind('click', clickHandler)


if __name__== '__main__':
    graphString = 'root:1'
    edgeIDs = list(graphString.split(' '))  #' ' needed for RapydScript; list needed lest we get an array
    nodeIDs = list(set(str.replace(graphString, ':', ' ').split(' '))) # '0 1 2 3 4'.split(' ')
    ########   graphstring.replace won't work.        RapydScript quirk
    
    #make spheres and labels
    for ID in nodeIDs:
        newSphere(ID)
    
    
    #make cones after spheres exist
    for eID in edgeIDs:
        newCone(eID)


    spheres['root'].visible=False
    spheres['root'].label.visible=False
    cones['root:1'].visible=False

    # Generate nodes
    params={'edgeIDs': edgeIDs,
            'iterations'    : 10,
            'update'        : update,
            'is_3D'         : False,
            'force_strength': 5.0,
            'dampening'     : 0.01,
            'max_velocity'  : 2.0,
            'max_distance'  : 50}

    nodes = run(nodes, params)
    giveBirth('1:13')
    for i in range(15):
        giveBirth(f'{13+i}:{13+i+1}')
        nodes = run(nodes, params)
        
    params['iterations']=100
    nodes = run(nodes, params)
