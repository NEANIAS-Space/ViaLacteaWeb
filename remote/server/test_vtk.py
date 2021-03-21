#!/usr/bin/env python

# This simple example shows how to do basic rendering and pipeline
# creation.

import vtk
import sys
import os
import random

def GetFPS(caller, ev):
    
    # Just do this to demonstrate who called callback and the event that triggered it.
    print(caller.GetClassName(), "Event Id:", ev)
    timeInSeconds = caller.GetLastRenderTimeInSeconds()
    fps = 1.0/timeInSeconds;
    print( fps ,"fps ");

# VTK specific code
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

reader = vtk.vtkPLYReader()
reader.SetFileName("testFile.ply")
reader.Update()
poly=reader.GetOutput()


bounds=poly.GetBounds()



mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()

mapper.SetInputData(reader.GetOutput())
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.SetSize(1600,1600);


  
#renderer.AddObserver('EndEvent', GetFPS)

endCount=20
time=0.0

for i in range(endCount):
   max = [0 for i in range(3)]
   min = [0 for i in range(3)]
   max[0]=bounds[1]+random.uniform(0,40)
   max[1]=bounds[3]+random.uniform(0,40)
   max[2]=bounds[5]+random.uniform(0,40)
   
   min[0]=bounds[0]+random.uniform(0,40)
   min[1]=bounds[2]+random.uniform(0,40)
   min[2]=bounds[4]+random.uniform(0,40)
   
   renderer.ResetCamera(min[0],max[0],min[1],max[1],min[2],max[2]);
   renderWindow.Render();
   sec=renderer.GetLastRenderTimeInSeconds()
   print("seconds per frame ", sec)
   time+=1.0/(sec)

print("Total FPS: ",time/endCount)


clock =vtk.vtkTimerLog()
clock.StartTimer();
startPoint = [0 for i in range(3)]
for i in range(endCount):
   max = [0 for i in range(3)]
   min = [0 for i in range(3)]
   max[0]=bounds[1]+random.uniform(0,40)
   max[1]=bounds[3]+random.uniform(0,40)
   max[2]=bounds[5]+random.uniform(0,40)
   
   min[0]=bounds[0]+random.uniform(0,40)
   min[1]=bounds[2]+random.uniform(0,40)
   min[2]=bounds[4]+random.uniform(0,40)
   renderer.ResetCamera(min[0],max[0],min[1],max[1],min[2],max[2])
   renderWindow.Render();

clock.StopTimer()
frameRate = float(endCount) / clock.GetElapsedTime();
print("AVERAGE FRAME RATE: ", frameRate)

renderWindowInteractor.Start()

