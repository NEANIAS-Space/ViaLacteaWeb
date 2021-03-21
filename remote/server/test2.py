

# import to process args
import sys
import os
import random

# import vtk modules.
import vtk

import vtk.vtkVialactea
# =============================================================================
# Create custom ServerProtocol class to handle clients requests
# =============================================================================
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


fitsReader = vtk.vtkVialactea.vtkFitsUnstructuredReader()
fitsReader.is3D=True;
fitsReader.SetFileName("vlkb-merged_3D_2021-03-08_10-39-11_837561_16774-16805.fits");
# fitsReader.GenerateVLKBUrl("0,0","2,2");
fitsReader.Update();

max=fitsReader.GetMax();
min=fitsReader.GetMin();

polydata=fitsReader.GetOutput();



popSplatter = vtk.vtkGaussianSplatter()
popSplatter.SetInputData(polydata)
popSplatter.SetSampleDimensions(170, 170, 170)
popSplatter.SetRadius(0.0078)
popSplatter.ScalarWarpingOff()
popSplatter.Update()


shellE = vtk.vtkMarchingCubes();
shellE.SetInputData(popSplatter.GetOutput())
shellE.ComputeNormalsOff();
shellE.SetValue(0, 0.001)#3*fitsReader.GetRMS())


shellE.Update()
poly=shellE.GetOutput()


bounds=poly.GetBounds()


mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()

mapper.SetInputConnection(shellE.GetOutputPort())
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()
renderWindow.SetSize(1600,1600);


  
  
#renderer.AddObserver('EndEvent', GetFPS)



endCount=20
time=0.0
renderer.ResetCamera()
for i in range(endCount):
   max = [0 for i in range(3)]
   min = [0 for i in range(3)]
   #max[0]=bounds[1]+random.uniform(0,10)
   #max[1]=bounds[3]+random.uniform(0,10)
   #max[2]=bounds[5]+random.uniform(0,10)
   
   #min[0]=bounds[0]+random.uniform(0,10)
   #min[1]=bounds[2]+random.uniform(0,10)
   #min[2]=bounds[4]+random.uniform(0,10)
   
   #renderer.ResetCamera(min[0],max[0],min[1],max[1],min[2],max[2]);
   renderer.Render()
   fps=renderer.GetLastRenderTimeInSeconds()
   print("fps ", fps)
   time+=1.0/(fps)

print("Total FPS: ",time/endCount)

#Other approach
clock =vtk.vtkTimerLog()
clock.StartTimer();

for i in range(endCount):
   max = [0 for i in range(3)]
   min = [0 for i in range(3)]
   #max[0]=bounds[1]+random.uniform(0,10)
   #max[1]=bounds[3]+random.uniform(0,10)
   #max[2]=bounds[5]+random.uniform(0,10)
   
   #min[0]=bounds[0]+random.uniform(0,10)
   #min[1]=bounds[2]+random.uniform(0,10)
   #min[2]=bounds[4]+random.uniform(0,10)
   
   #renderer.ResetCamera(min[0],max[0],min[1],max[1],min[2],max[2]);
   renderer.Render();
  
clock.StopTimer()
frameRate = endCount / clock.GetElapsedTime()
print("AVERAGE FRAME RATE: ", frameRate)

  
#renderer.AddObserver('EndEvent', GetFPS)

renderWindowInteractor.Start()

