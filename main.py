
from layerouter import *

def getIDs(edges):
    IDs=[]
    for t in edges:
        IDs.append(str(t[0]))
        IDs.append(str(t[1]))
    return set(IDs)


edgeInts=[(1,2),(2,3), (3,1), (3,4), (4,5), (4,6), (5,6), (6,7), (7,8),(8,9),(9,6)]
edges = [{'source' : str(s), 'target' : str(t)} for s, t in edgeInts]

cones={}
spheres={}


IDs = getIDs(edgeInts) #IDs are strings

#make spheres
for ID in IDs:
    spheres[ID] = sphere(color=color.orange)

def edgeUtil(edge): #eID for '1' -> '2' is '1.2'
    s,t = edge['source'], edge['target']
    return s,t, s+'.'+t

#make cones
for edge in edges:
    s,t,eID = edgeUtil(edge)
    cones[eID]= cone(pos=spheres[s].pos, axis=spheres[s].pos - spheres[t].pos)

def updateSpheres(nodes):
    for k,v in oItems(nodes):
        x,y,z = v['velocity']
        spheres[str(k)].pos = vector(x,y,z)

def updateSpheresAndCones(nodes):
     updateSpheres(nodes)
     for eID in oKeys(cones):
         s,t = eID.split('.')
         cones[eID].pos = spheres[s].pos
         cones[eID].axis= spheres[t].pos
     
    
    
# Generate nodes
params={'edges':edges,
        'iterations'    : 30,
        'updateNodes'   : updateSpheresAndCones,
        'is_3D'         : False,
        'force_strength': 5.0,
        'dampening'     : 0.01,
        'max_velocity'  : 2.0,
        'max_distance'  : 50}


nodes = run(params)
print(oKeys(cones))
