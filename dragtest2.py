
import traceback
def clickHandler(event): #experimental
    global hit
    hit=None
    drag=False
    target=None
    try:
        hitID = scene.mouse.pick.label.text
    except Exception as e:
       hitID='no_hit'
    if hitID:
         try:
            mousepos = scene.mouse.pos
            what = event.event
            #print(what, hit, mousepos)
            
            if what=='mousedown':
                drag=True
                target=spheres[hitID]
            if what=='mouseup'  :
                drag = False
                target = 'None'
            if what=='mousemove':
                spheres['1'].pos = mousepos
         except:
            traceback.print_exc()
scene.bind('mouseup mousedown mousemove click', clickHandler)

