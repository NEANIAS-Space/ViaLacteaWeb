import time

from vtk.web import protocols as vtk_protocols

from wslink import register as exportRpc

# import Twisted reactor for later callback
from twisted.internet import reactor

import vtk
import vtk.vtkVialactea
# -------------------------------------------------------------------------
# ViewManager
# -------------------------------------------------------------------------

class VtkCone(vtk_protocols.vtkWebProtocol):
    def __init__(self):
        self.cone = vtk.vtkMarchingCubes();
        self.fitsReader = vtk.vtkVialactea.vtkFitsReader();
        self.rms=0.0;
        self.min=0.0;
        self.max=0.0;
        self.path=" ";

    def SetPath(self,path):
        self.path=path;
        print(path);
    @exportRpc("vtk.initialize")
    def createVisualization(self):
        renderWindow = self.getView('-1')
        renderer = renderWindow.GetRenderers().GetFirstRenderer()
        
        
        fitsReader=self.fitsReader;
        fitsReader.SetTempPath(self.path)
        fitsReader.is3D=True;
        fitsReader.GenerateVLKBUrl("3, 0,0.1,0.1");
        # fitsReader.SetFileName("../../data/vlkb-merged_3D_2021-03-08_10-39-11_837561_16774-16805.fits");
        fitsReader.CalculateRMS();
        

        self.max=fitsReader.GetMax();
        self.min=fitsReader.GetMin();
        self.rms=fitsReader.GetRMS();

        shellE = self.cone
        shellE.SetInputData(fitsReader.GetOutput())
        shellE.ComputeNormalsOff();
        shellE.SetValue(0, 3*fitsReader.GetRMS())
        shellE.Update()
        print("cellsNum=", shellE.GetOutput().GetNumberOfCells())
        
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        mapper.SetInputConnection(shellE.GetOutputPort())
        actor.SetMapper(mapper)

        renderer.AddActor(actor)
        renderer.ResetCamera()
        renderWindow.Render()

        return self.resetCamera()


    @exportRpc("vtk.camera.reset")
    def resetCamera(self):
        renderWindow = self.getView('-1')
        renderWindow.GetRenderers().GetFirstRenderer().ResetCamera()
        renderWindow.Render()

        self.getApplication().InvalidateCache(renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')

        return -1
        
    @exportRpc("vtk.cone.url")
    def loadURL(self):
        print("FitsReader callse");
        self.fitsReader.GenerateVLKBUrl("9, 0,0.3,0.1");
        self.fitsReader.CalculateRMS();
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        renderer.ResetCamera()
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')
   
    @exportRpc("vtk.cone.urlfits")
    def loadXMLFITS(self,res):
        print("FitsReader call with ");
        # str_p=str(p1)+","+str(p2);
        # str_r=str(r1)+","+str(r2);
        print(res);
       
        
        result_success=self.fitsReader.GenerateVLKBUrl(res);
        result=self.fitsReader.GetSurveysData();
        self.fitsReader.CalculateRMS();
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        #renderer.ResetCamera()
        #renderWindow.Render()
        #self.getApplication().InvokeEvent('UpdateEvent')
        print(result_success); #just for binary success/failure
        return result;


    @exportRpc("vtk.cone.resolution.update")
    def updateResolution(self, resolution):
        self.cone.SetValue(0, resolution*self.rms)
        self.cone.Update()
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')


    @exportRpc("viewport.mouse.zoom.wheel")
    def updateZoomFromWheel(self, event):
      if 'Start' in event["type"]:
        self.getApplication().InvokeEvent('StartInteractionEvent')

      renderWindow = self.getView(event['view'])
      if renderWindow and 'spinY' in event:
        zoomFactor = 1.0 - event['spinY'] / 10.0

        camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
        fp = camera.GetFocalPoint()
        pos = camera.GetPosition()
        delta = [fp[i] - pos[i] for i in range(3)]
        camera.Zoom(zoomFactor)

        pos2 = camera.GetPosition()
        camera.SetFocalPoint([pos2[i] + delta[i] for i in range(3)])
        renderWindow.Modified()

      if 'End' in event["type"]:
        self.getApplication().InvokeEvent('EndInteractionEvent')
