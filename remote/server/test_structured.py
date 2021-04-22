
#import to process args
import sys 
import os 
import random

#import vtk modules.
import vtk


import vtk.vtkVialactea
#== == == == == == == == == == == == == == == == == == == == == == == == == == \

#Create custom ServerProtocol class to handle clients requests
#== == == == == == == == == == == == == == == == == == == == == == == == == == \

def GetFPS(caller, ev):
    print(caller.GetClassName(), "Event Id:", ev)
    timeInSeconds = caller.GetLastRenderTimeInSeconds()
    fps = 1.0/timeInSeconds;
    print(fps, "fps ");

#VTK specific code
renderer = vtk.vtkRenderer() 
renderWindow =vtk.vtkRenderWindow() 
renderWindow.AddRenderer(renderer)

renderWindowInteractor =vtk.vtkRenderWindowInteractor() 
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

fitsReader = vtk.vtkVialactea.vtkFitsReader()
fitsReader.is3D=True;
fitsReader.GenerateVLKBUrl("10,0,0.1,6.1"); 
#fitsReader.SetFileName("../../data/vlkb-cutout_2021-02-18_12-33-05_516569_JCMT-HARP_COHRS_18p00_0p00_CUBE_REBIN_R1.fits");
fitsReader.CalculateRMS();

fitsReader.GenerateVLKBUrl("2,2,0.1,6.1"); #("10,0,0.4,6.1"); - loading of corrupted fits
#fitsReader.SetFileName("../../data/vlkb-cutout_2021-02-18_12-33-05_516569_JCMT-HARP_COHRS_18p00_0p00_CUBE_REBIN_R1.fits");
fitsReader.CalculateRMS();

max = fitsReader.GetMax();
min = fitsReader.GetMin();

shellE = vtk.vtkMarchingCubes();
shellE.SetInputData(fitsReader.GetOutput())
shellE.ComputeNormalsOff();
shellE.SetValue(0, 3*fitsReader.GetRMS())
shellE.Update()
print("cellsNum=", shellE.GetOutput().GetNumberOfCells())
poly = shellE.GetOutput();


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



renderWindowInteractor.Start()
