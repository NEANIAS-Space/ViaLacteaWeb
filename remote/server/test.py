
#import to process args
import sys import os import random

#import vtk modules.
    import vtk

    try : import argparse

    except ImportError:
#since Python 2.6 and earlier don't have argparse, we simply provide
#the source for the same as _argparse and we use it instead.
    from vtk.util import _argparse as argparse

import vtk.vtkVialactea
#== == == == == == == == == == == == == == == == == == == == == == == == == == \
    == == == == == == == == == == == == =
#Create custom ServerProtocol class to handle clients requests
#== == == == == == == == == == == == == == == == == == == == == == == == == == \
    == == == == == == == == == == == == =
def GetFPS(caller, ev):

#Just do this to demonstrate who called callback and the event that triggered  \
    it.
    print(caller.GetClassName(), "Event Id:", ev)
    timeInSeconds = caller.GetLastRenderTimeInSeconds()
    fps = 1.0/timeInSeconds;
print(fps, "fps ");

#VTK specific code
renderer = vtk.vtkRenderer() renderWindow =
    vtk.vtkRenderWindow() renderWindow.AddRenderer(renderer)

        renderWindowInteractor =
        vtk.vtkRenderWindowInteractor() renderWindowInteractor
            .SetRenderWindow(renderWindow)
                renderWindowInteractor.GetInteractorStyle()
            .SetCurrentStyleToTrackballCamera()

                fitsReader =
            vtk.vtkVialactea.vtkFitsUnstructuredReader() fitsReader.is3D = True;
fitsReader.SetFileName(
    "vlkb-merged_3D_2021-03-08_10-39-11_837561_16774-16805.fits");
#fitsReader.GenerateVLKBUrl("0,0", "2,2");
fitsReader.Update();

max = fitsReader.GetMax();
min = fitsReader.GetMin();

polydata = fitsReader.GetOutput();

popSplatter =
    vtk.vtkGaussianSplatter() popSplatter.SetInputData(polydata)
        popSplatter.SetSampleDimensions(170, 170, 170)
            popSplatter.SetRadius(0.0078)
                popSplatter.ScalarWarpingOff() popSplatter.Update()

                    shellE = vtk.vtkMarchingCubes();
shellE.SetInputData(popSplatter.GetOutput()) shellE.ComputeNormalsOff();
shellE.SetValue(0, 0.01)#3*fitsReader.GetRMS())


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
   sec = renderer.GetLastRenderTimeInSeconds() print("seconds per frame ", sec)
   time += 1.0 / (sec)

                            print("Total FPS: ", time / endCount)

                                clock = vtk.vtkTimerLog() clock.StartTimer();
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

clock.StopTimer() frameRate = float(endCount) / clock.GetElapsedTime();
print("AVERAGE FRAME RATE: ", frameRate)

    plyWriter =
        vtk.vtkPLYWriter() plyWriter.SetFileName("testFile.ply") plyWriter
            .SetInputData(polydata) plyWriter
            .Write()

                renderWindowInteractor.Start()
