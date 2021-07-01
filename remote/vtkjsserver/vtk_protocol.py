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
        self.imageViewer = vtk.vtkImageViewer2();
        self.viewer  =vtk.vtkResliceImageViewer();
        
    def updateScene(self, renderer, renWin):
      renderer.ResetCamera();
      renWin.GetInteractor().Render();


    @exportRpc("vtk.initialize")
    def createVisualization(self):
        renderWindow = self.getView('-1')
        rends=renderWindow.GetRenderers()
        it=rends.NewIterator()
        renderer = rends.GetItemAsObject(0)
        renderer2 = rends.GetItemAsObject(1)	
        renderer2.SetBackground(0.21,0.23,0.25);
        
        
        fitsReader=self.fitsReader;
        
        fitsReader.is3D=True;
        fitsReader.GenerateVLKBUrl("0, 0,0.1,0.1");
        # fitsReader.SetFileName("../../data/vlkb-merged_3D_2021-03-08_10-39-11_837561_16774-16805.fits");
        fitsReader.CalculateRMS();
            

        self.max=fitsReader.GetMax();
        self.min=fitsReader.GetMin();
        self.rms=fitsReader.GetRMS();
        
        #outline
        outlineF = vtk.vtkOutlineFilter();
        outlineF.SetInputData(fitsReader.GetOutput());
        
        
        outlineM = vtk.vtkPolyDataMapper();
        outlineM.SetInputConnection(outlineF.GetOutputPort());
        outlineM.ScalarVisibilityOff();

        outlineA = vtk.vtkActor();
        outlineA.SetMapper(outlineM);

	#isosurface itself Marching cubes
        shellE = self.cone
        shellE.SetInputData(fitsReader.GetOutput())
        shellE.ComputeNormalsOff();
        shellE.SetValue(0, 3*fitsReader.GetRMS())
        shellE.Update()
        print("cellsNum=", shellE.GetOutput().GetNumberOfCells())
        
        shellM = vtk.vtkPolyDataMapper()
        shellM.ScalarVisibilityOff();
        shellA = vtk.vtkActor()

        shellM.SetInputConnection(shellE.GetOutputPort())
        shellA.SetMapper(shellM)
        
        shellA.GetProperty().SetColor(1.0, 0.5, 0.5);

        

        
        
        #first pipeline
        #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L1428
        sliceE= vtk.vtkPlanes();
        fits=fitsReader.GetOutput();
        bounds=fits.GetBounds()
        
        sliceE.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], 0, 1);
        frustumSource = vtk.vtkFrustumSource();
        frustumSource.ShowLinesOff();
        frustumSource.SetPlanes(sliceE);
        frustumSource.Update();
        frustum = frustumSource.GetOutput();
        
        mapper2 = vtk.vtkPolyDataMapper();
        mapper2.SetInputData(frustum);
        sliceA = vtk.vtkActor();
        sliceA.SetMapper(mapper2);
        
        
       
        
        
        renderer.AddActor(sliceA)
        renderer.AddActor(shellA)
        renderer.AddActor(outlineA)
        
        #axis
        axes=vtk.vtkAxesActor()
        


        vtkAxesWidget = vtk.vtkOrientationMarkerWidget();
        vtkAxesWidget.SetInteractor(renderWindow.GetInteractor());

        vtkAxesWidget.SetOrientationMarker(axes);

        vtkAxesWidget.SetOutlineColor( 0.9300, 0.5700, 0.1300 );
        vtkAxesWidget.SetViewport( 0.0, 0.0, 0.2, 0.2 );
        vtkAxesWidget.SetEnabled(1);
        vtkAxesWidget.InteractiveOff();
        
        
        
        #TODO import custom legend
        legendScaleActor3d =  vtk.vtkLegendScaleActor();
        legendScaleActor3d.LegendVisibilityOff();
        #legendScaleActor3d.setFitsFile(myfits);
        renderer.AddActor(legendScaleActor3d)
        
        #TODO save coodrdinates in camera
        #m_Ren1->GetActiveCamera()->GetPosition(cam_init_pos);
        #m_Ren1->GetActiveCamera()->GetFocalPoint(cam_init_foc);
        
        #second pipeline
        
        #// A yellow-to-blue colormap defined by individually setting all values
        #vtkSmartPointer<vtkLookupTable> lutSlice = vtkSmartPointer<vtkLookupTable>::New();
        #lutSlice->SetTableRange( myfits->GetRangeSlice(0)[0], myfits->GetRangeSlice(0)[1] );
        #SelectLookTable("Gray",lutSlice);

        #setVtkInteractorStyleImageContour();
        
        range = fits.GetScalarRange();
        rMin=fitsReader.GetRangeSliceMin(0)
        rMax=fitsReader.GetRangeSliceMax(0)
        #print(rMin,rMax)
        lut = vtk.vtkLookupTable();
        #lut.SetScaleToLog10();
        lut.SetTableRange(rMin,rMax) #fitsReader.GetRangeSlice(0)[0], fitsReader.GetRangeSlice(0)[1] );
        lut.SetHueRange (0., 0.);
        lut.SetSaturationRange (0., 0.);
        lut.SetValueRange(0., 1.);
        #SelectLookTable("Gray",lut);
        lut.Build()
        
        self.viewer.SetRenderer(renderer2);
        self.viewer.SetRenderWindow(renderWindow);
        self.viewer.SetupInteractor(renderWindow.GetInteractor());
        self.viewer.SetInputData(fits);
        self.viewer.GetWindowLevel().SetOutputFormatToRGB();
        self.viewer.GetWindowLevel().SetLookupTable(lut);
        self.viewer.GetImageActor().InterpolateOff();
        
        #setSliceDatacube(1);
        #setSliceDatacube(0); #includes goContour
        
        self.viewer.SetSlice(1)
        self.viewer.SetSlice(0)
        
        self.viewer.GetRenderer().ResetCamera()
        
        legendScaleActorImage =  vtk.vtkLegendScaleActor();
        legendScaleActorImage.LegendVisibilityOff();
        #legendScaleActorImage.setFitsFile(myfits);
        renderer2.AddActor(legendScaleActorImage);
        

       



	#second window pipeline??
        #vtkSmartPointer<CustomVtkLegendScaleActor> legendScaleActorImage =  vtkSmartPointer<CustomVtkLegendScaleActor>::New();

        #legendScaleActorImage->LegendVisibilityOff();
        #legendScaleActorImage->setFitsFile(myfits);

        #m_Ren2->AddActor(legendScaleActorImage);
        

        # double *pos=m_Ren1->GetActiveCamera()->GetPosition();
        # cam_init_pos[0]=pos[0];
        # cam_init_pos[1]=pos[1];
        # cam_init_pos[2]=pos[2];



        #imageActor = self.viewer.GetImageActor();
        #renderer2.AddActor(imageActor);
        
        
        #style = vtk.vtkInteractorStyleImage()
        style=vtk.vtkInteractorStyleMultiTouchCamera()
        renderWindow.SetInteractorStyle(style);
        #renderWindow.SetCurrentStyleToTrackballCamera()
        #vtkInteractorStyleTrackballCamera 
        renderWindow.Render()


         
        #renderer.SetViewUp( 0, 1, 0 )
        # m_Ren1->GetActiveCamera()->SetFocalPoint( cam_init_foc );
        # m_Ren1->GetActiveCamera()->SetPosition( cam_init_pos);
    
        renderer.ResetCamera()
        renderer2.ResetCamera()
        
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
        self.fitsReader.GenerateVLKBUrl("10, 0,0.3,0.2");
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
       
        
        self.fitsReader.GenerateVLKBUrl(res);
        result= self.fitsReader.CalculateRMS();
        res_str=self.fitsReader.GetSurveysData();
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        #renderer.ResetCamera()
        #renderWindow.Render()
        #self.getApplication().InvokeEvent('UpdateEvent')
        # return self.resetCamera()
        return res_str;


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
