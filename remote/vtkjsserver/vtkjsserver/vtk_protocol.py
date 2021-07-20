import time
import math 

from vtk.web import protocols as vtk_protocols

from wslink import register as exportRpc

# import Twisted reactor for later callback
from twisted.internet import reactor

import vtk
import vtk.vtkVialactea
# -------------------------------------------------------------------------
# Basic VLW procedures
# -------------------------------------------------------------------------

class vlwBase(vtk_protocols.vtkWebProtocol):
    def __init__(self):
        #initialisation of main variables
        self.cone = vtk.vtkMarchingCubes();
        self.fitsReader = vtk.vtkVialactea.vtkFitsReader();
        self.rms=0.0;
        self.min=0.0;
        self.max=0.0;
        self.imageViewer = vtk.vtkImageViewer2();
        #GetWindowLevel ()
        #SetColorWindow (double s)
        #SetColorLevel (double s)
        self.viewer  =vtk.vtkResliceImageViewer();
        self.sliceA = vtk.vtkActor();
        self.sliceE= vtk.vtkPlanes();
        self.frustumSource = vtk.vtkFrustumSource();
        self.fp = [0.0 for i in range(3)]
        self.pos = [0.0 for i in range(3)]
        self.zoom=1.0;
        self.cam_init_pos=[0.0 for i in range(3)];
        self.cam_init_foc=[0.0 for i in range(3)];
        self.rotateX=False;
        
        self.textActor = vtk.vtkTextActor()
        #self.textActor.VisibilityOff()
        self.textActor.PickableOff()
        
        #contours
        self.currentContourActor = vtk.vtkLODActor();
        self.currentContourActorForMainWindow = vtk.vtkLODActor();
        
        self.x1=-1000000
        self.y1=-1000000
        self.MotionFactor = 10.0;
        self.winScale=100;
        
        #window level
        self.WindowLevelStartPosition=[0.0 for i in range(2)]
        

        self.WindowLevelCurrentPosition=[0.0 for i in range(2)]
        
        self.WindowLevelInitial =[0.0 for i in range(2)]

        self.WindowLevelInitial[0] = 1.0; # Window
        self.WindowLevelInitial[1] = 0.5; # Level
        
    def updateScene(self, renderer, renWin):
      renderer.ResetCamera();
      renWin.GetInteractor().Render();


    @exportRpc("vtk.initialize")
    def createVisualization(self):
        #Get renwin and renderers
        renderWindow = self.getView('-1')
        self.renderWindow=renderWindow;
        rends=renderWindow.GetRenderers()
        it=rends.NewIterator()
        renderer = rends.GetItemAsObject(0)
        renderer2 = rends.GetItemAsObject(1)	
        renderer2.SetBackground(0.21,0.23,0.25);
        self.Ren1=renderer;
        self.Ren2=renderer2;
        
         #Entry point to entire vis logic:
        #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L1328
        
        
        
        #First pipeline as described in 
        #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L1386
        
        
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

        
        # slice L1406
        fits=fitsReader.GetOutput();
        bounds=fits.GetBounds()
        
        self.sliceE.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], 0, 1);
       
        self.frustumSource.ShowLinesOff();
        self.frustumSource.SetPlanes(self.sliceE);
        self.frustumSource.Update();
        
        
        mapper2 = vtk.vtkPolyDataMapper();
        mapper2.SetInputData(self.frustumSource.GetOutput());
       
        self.sliceA.SetMapper(mapper2);
        
        
       
        
        
        renderer.AddActor(self.sliceA)
        renderer.AddActor(shellA)
        renderer.AddActor(outlineA)
        
        # axes and coords L1420
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
        renderer.AddActor(legendScaleActor3d);
        
        
           #add label
        tprop = vtk.vtkTextProperty()
        tprop.SetFontFamilyToArial()
        tprop.SetFontSize(10)
        tprop.BoldOff()
        tprop.ShadowOff()
        tprop.SetColor(1, 1, 1)
        #self.textActor.SetDisplayPosition(205, 205)
        #self.textActor.SetTextProperty(tprop);
        self.textActor.SetInput(fitsReader.GetDataCubeData())
        renderer.AddActor(self.textActor);
        print("Test was set")
        
        #Set coordinates for reset camera 
        # all actors where added to renderer for first pipeline above
        self.cam_init_pos=renderer.GetActiveCamera( ).GetPosition();
        self.cam_init_foc=renderer.GetActiveCamera( ).GetFocalPoint();
       
        print(self.cam_init_pos)
        
        #getInteractorStyle info to check
       
        print("Interactor type") 
        name=self.renderWindow.GetInteractor().GetInteractorStyle().GetClassName()
        print(name)
        
     
        
        #Second pipeline
        
        rMin=fitsReader.GetRangeSliceMin(0)
        rMax=fitsReader.GetRangeSliceMax(0)
        #print(rMin,rMax)
        lut = vtk.vtkLookupTable();
        lut.SetTableRange(rMin,rMax) 
        lut.SetHueRange (0., 0.);
        lut.SetSaturationRange (0., 0.);
        lut.SetValueRange(0., 1.);
        
        lut.Build()
        
        #setVtkInteractorStyleImageContour(); L1473 - the setting of  vtk.vtkInteractorStyleImage()
        #As described in https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L3173
        #Left Mouse button triggers window level events
        #CTRL Left Mouse spins the camera around its view plane normal
        #SHIFT Left Mouse pans the camera
        #CTRL SHIFT Left Mouse dollys (a positional zoom) the camera
        #Middle mouse button pans the camera
        #Right mouse button dollys the camera.
        #SHIFT Right Mouse triggers pick events
    
        
        self.viewer.SetRenderer(renderer2);
        self.viewer.SetRenderWindow(renderWindow);
        self.viewer.SetupInteractor(renderWindow.GetInteractor());
        self.viewer.SetInputData(fits);
        self.viewer.GetWindowLevel().SetOutputFormatToRGB();
        self.viewer.GetWindowLevel().SetLookupTable(lut);
        self.viewer.GetImageActor().InterpolateOff();
        
        
        
        self.viewer.SetSlice(1)
        self.viewer.SetSlice(0)
        
        self.viewer.GetRenderer().ResetCamera()
        
        print("Interactor type2") 
        name=self.renderWindow.GetInteractor().GetInteractorStyle().GetClassName()
        print(name)
        
        #istyle = vtk.vtkInteractorStyleTrackballCamera()
        #self.renderWindow.GetInteractor().SetInteractorStyle(istyle)
        #print("Interactor replaced with") 
        #name=self.renderWindow.GetInteractor().GetInteractorStyle().GetClassName()
        #print(name)
         
        legendScaleActorImage =  vtk.vtkLegendScaleActor();
        legendScaleActorImage.LegendVisibilityOff();
        #legendScaleActorImage.setFitsFile(myfits);
        renderer2.AddActor(legendScaleActorImage);
        
        #updateScene();
        
        self.renderWindow.Render()
       
         
       
        camera = self.Ren1.GetActiveCamera()
        camera.SetViewUp( 0, 1, 0 )

        
        
        renderer.ResetCamera()
        renderer2.ResetCamera()
        
        renderWindow.Render()
        
        


        return self.resetCamera()
        
    def removeContour(self):
        print("to impleent")
        #m_Ren2->RemoveActor2D(currentContourActor);
    
        #myParentVtkWindow->m_Ren1->RemoveActor2D(currentContourActorForMainWindow);
        #myParentVtkWindow->ui->qVTK1->update();
        #myParentVtkWindow->ui->qVTK1->renderWindow()->GetInteractor()->Render();
       
    
    
    def goContour(self):
        self.removeContour();
        plane = vtk.vtkPlane();
        plane.SetOrigin(0,0, self.viewer.GetSlice());
        plane.SetNormal(0,0,1);

        cutter = vtk.vtkCutter();
        cutter.SetCutFunction(plane);
        cutter.SetInputData(self.self.fitsReader.GetOutput());
        cutter.Update();

        cutterMapper = vtk.vtkPolyDataMapper();
        cutterMapper.SetInputConnection( cutter.GetOutputPort());

        polyData = vtk.vtkPolyData();
        contoursFilter = vtk.vtkContourFilter();
        polyData = cutter.GetOutput();

        contoursFilter.GenerateValues(0, 0.5, 1);
        contoursFilter.SetInputConnection(cutter.GetOutputPort());

        contourLineMapperer = vtk.vtkPolyDataMapper();
        contourLineMapperer.SetInputConnection(contoursFilter.GetOutputPort());
        ##contourLineMapperer.SetScalarRange(ui->lowerBoundLineEdit->text().toDouble(), ui->upperBoundLineEdit->text().toDouble());
        contourLineMapperer.ScalarVisibilityOn();
        contourLineMapperer.SetScalarModeToUsePointData();
        contourLineMapperer.SetColorModeToMapScalars();


        self.currentContourActor.SetMapper(contourLineMapperer);
        self.currentContourActor.GetProperty().SetLineWidth(1);

        self.renderWindow.GetFirstRenderer().AddActor2D(currentContourActor);
        self.renderWindow().GetInteractor().Render();


    def ResetCam():
        renderWindow = self.getView('-1')
        rends=renderWindow.GetRenderers()
        
        renderer = rends.GetItemAsObject(0)
        renderer2 = rends.GetItemAsObject(1)	
        renderer.ResetCamera()
        renderer2.ResetCamera()
        renderWindow.Render()

    @exportRpc("vtk.cone.fits.update")
    def updateFits(self,url):
        
        self.fitsReader.DownloadSurveyDataCube(url);
        result= self.fitsReader.CalculateRMS();
        
        fits=self.fitsReader.GetOutput();
        bounds=fits.GetBounds()
        
        self.textActor.SetInput(self.fitsReader.GetDataCubeData())
        self.textActor.Modified();
        self.textActor.GetMapper().Update()
        
        self.sliceE.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], 0, 1);
        self.frustumSource.Update()
        #print("Slice updated")
        #self.ResetCamera()
        #print("Slice updated")


    @exportRpc("vtk.camera.reset")
    def resetCamera(self):
        renderWindow = self.getView('-1')
        renderWindow.GetRenderers().GetFirstRenderer().ResetCamera()
        renderWindow.Render()
        #renderWindow.GetRenderers().GetFirstRenderer().SetViewUp( 0, 1, 0 );
        renderWindow.GetRenderers().GetFirstRenderer().SetFocalPoint( self.cam_init_foc );
        renderWindow.GetRenderers().GetFirstRenderer().SetPosition( self.cam_init_pos);

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
        print("FitsReader update call with ");
        # str_p=str(p1)+","+str(p2);
        # str_r=str(r1)+","+str(r2);
        print(res);
       
        
        self.fitsReader.GenerateVLKBUrl(res);
        result= self.fitsReader.CalculateRMS();
        res_str=self.fitsReader.GetSurveysData();
        self.textActor.SetInput(self.fitsReader.GetDataCubeData())
        self.textActor.Modified();
        self.textActor.GetMapper().Update()
        
        #renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        #renderer.ResetCamera()
        #renderWindow.Render()
        #self.getApplication().InvokeEvent('UpdateEvent')
        # return self.resetCamera()
        
        fits=self.fitsReader.GetOutput();
        bounds=fits.GetBounds()
        #print("Bounds updated ");
        self.sliceE.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], 0, 1);
        self.frustumSource.Update()
        
        #TODO reset camera
        print("Pos updated ");
        #self.resetCamera()
        self.Ren1.ResetCamera()
        camera = self.Ren1.GetActiveCamera()
        camera.SetViewUp( 0, 1, 0 )
        self.cam_init_pos=self.Ren1.GetActiveCamera( ).GetPosition();
        self.cam_init_foc=self.Ren1.GetActiveCamera( ).GetFocalPoint();
        print("Bounds updated ");
        #self.Ren1.Render();
        return res_str;


    @exportRpc("vtk.cone.resolution.update")
    def updateResolution(self, resolution):
        self.cone.SetValue(0, resolution*self.rms)
        self.cone.Update()
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')
    
    @exportRpc("vtk.cone.planes.update")
    def updatePlanes(self, planes):
        #print("FitsReader planes with ");
        #setSliceDatacube(planes-1);
        
        #update lut
        rMin=self.fitsReader.GetRangeSliceMin(planes-1)
        rMax=self.fitsReader.GetRangeSliceMax(planes-1)
        #print(rMin,rMax)
        lut = vtk.vtkLookupTable();
        #lut.SetScaleToLog10();
        lut.SetTableRange(rMin,rMax) #fitsReader.GetRangeSlice(0)[0], fitsReader.GetRangeSlice(0)[1] );
        lut.SetHueRange (0., 0.);
        lut.SetSaturationRange (0., 0.);
        lut.SetValueRange(0., 1.);
        #SelectLookTable("Gray",lut);
        lut.Build()
        
        self.viewer.GetWindowLevel().SetOutputFormatToRGB();
        self.viewer.GetWindowLevel().SetLookupTable(lut);
        self.viewer.GetImageActor().InterpolateOff();
        self.viewer.SetSlice(planes-1);
        
        #goContour();

        #ui->minSliceLineEdit->setText(QString::number(myfits->GetRangeSlice(i)[0]));
        #ui->maxSliceLineEdit->setText(QString::number(myfits->GetRangeSlice(i)[1]));
        
        self.viewer.GetRenderer().ResetCamera();
        self.viewer.Render();

        
        self.sliceA.SetPosition (0,0,planes);
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')

#REMOTE MOUSE PROCEDURES
#https://kitware.github.io/vtk-js/api/Interaction_Style_InteractorStyleRemoteMouse.html

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

    @exportRpc("viewport.mouse.move")
    def updateMouseMove(self, event):
         #print("mouse move")
         if event['action']=='down':
             
             if event['shiftKey']==0:
                 #https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleTrackballCamera.cxx#L248
                 angle  = 0;
                 x=event['x']
                 y=event['y']
                 #print("Got rotate call")
                 #print(dist)
                 #check if outside of port
                 if x-0.01<=0.0 or y-0.01<=0.0 or x+0.01>1.0 or y+0.01>1.0:
                    self.getApplication().InvokeEvent('EndInteractionEvent')
                    self.x1=-1000000
                    self.y1=-1000000   
                    #print("Outside screen")
                 if self.x1>-1000000 and self.y1>-1000000 :  #dist>0.0: Second point
                     self.getApplication().InvokeEvent('StartInteractionEvent')
                     if x<0.5:
                 
                        
                     
                        dx=self.x1-x
                        dy=self.y1-y
                        #print(x,y)
                        #x,y are normalised from 0 to 1
                        size=self.renderWindow.GetSize();
                        delta_elevation = self.winScale*20.0 / size[1];
                        delta_azimuth = self.winScale*40.0 / size[0];
                     
                        #dist=math.sqrt((self.x1-x)*(self.x1-x)+(self.y1-y)*(self.y1-y))
                        rxf = dx * delta_azimuth * self.MotionFactor;
                        ryf = dy * delta_elevation * self.MotionFactor;
                     
                        #angX=(x-self.x1)*180/math.pi
                        #angY=(y-self.y1)*180/math.pi
                        camera = self.renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
                     
                        camera.Azimuth(rxf)
                        camera.Elevation(ryf)
                        camera.OrthogonalizeViewUp();
                        #self.Ren1.ResetCameraClippingRange();
                     
                        #print("Rotation done")
                     else : #window scale
                        #https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleImage.cxx#L180
                        size=self.renderWindow.GetSize();
                        delta_y = self.winScale*80.0 / size[1];
                        delta_x = self.winScale*160.0 / size[0];
                        
                        #self.WindowLevelInitial[0]=self.viewer.GetColorWindow()
                        #self.WindowLevelInitial[1]=self.viewer.GetColorLevel()
                        
                        window = self.viewer.GetColorWindow()
                        level = self.viewer.GetColorLevel()
                        #print("initial", window,level);
                        
                        dx=(self.x1-x)*delta_x;
                        dy=(self.y1-y)*delta_y;
                        
                        
                        # Scale by current values
                        d_w=0.01
                        if window < 0:
                            d_w=-0.01
                        d_l=0.01
                        if level < 0:
                            d_l=-0.01

                        if math.fabs(window) > 0.01:
                            dx = dx * window;
                        else:
                            dx = dx * d_w
                        if math.fabs(level) > 0.01:
                            dy = dy * level;
                        else:
                            dy = dy * d_l;
                        
                        # Abs so that direction does not flip

                        if window < 0.0:
                            dx = -1 * dx;
                        if level < 0.0:
                            dy = -1 * dy;
                        # Compute new window level

                        newWindow = dx + window;
                        newLevel = level - dy;

                        if newWindow < 0.01:
                             newWindow = 0.01;
                        self.viewer.SetColorWindow(newWindow)
                        self.viewer.SetColorLevel(newLevel);
                        self.viewer.Modified()
                        self.viewer.Render()
                        self.WindowLevelInitial[0]=newWindow;
                        self.WindowLevelInitial[1]=newLevel;
                        
                        self.Ren2.Render()
                        self.renderWindow.GetInteractor().Render();
                        print(newWindow,newLevel);


                        
                     
                     
                     self.renderWindow.Render()
                     #print(angle)
                     self.getApplication().InvokeEvent('EndInteractionEvent')
                 self.x1=x
                 self.y1=y
             if event['shiftKey']==1:
                 #vtkInteractorStyleImage
                 #https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleImage.cxx
                 print("other")
         
         if event['action']=='up': #end of interaction
             self.x1=-1000000
             self.y1=-1000000   
             self.getApplication().InvokeEvent('EndInteractionEvent')  
                 
                 
             
           
    @exportRpc("vtk.cone.camview.update")
    def updateCamView(self, v):
        camera = self.renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera();
        renderer=self.renderWindow.GetRenderers().GetFirstRenderer()
        renderer.ResetCamera()
        print(self.cam_init_foc)
        print(self.cam_init_pos)
        camera.SetFocalPoint( self.cam_init_foc );
        camera.SetPosition( self.cam_init_pos);
        #self.renderWindow.GetRenderers().GetFirstRenderer().SetViewUp( 0, 1, 0 );
        #self.renderWindow.Render()
        print("done")
        
        #if  v==1:
            #setCameraAzimuth(-180);
        #    camera.Azimuth(-180);
        #elif v== 2:
            #setCameraElevation(90);
        #    camera.Elevation(90);
        #elif v==  3:
            #setCameraAzimuth(-90);
        #    camera.Azimuth(-90);
        #elif v==  4:
            #setCameraAzimuth(90);
        #    camera.Azimuth(90);
           
        self.renderWindow.Render()
    
    @exportRpc("vtk.cone.rotate.update")
    def updateRotateAxis(self, v):
        print("update rot")
        self.rotateX=v;
        print(self.rotateX)
        


    @exportRpc("viewport.gesture")
    def updateGesture(self, event):
             
      if 'StartPinch' in event["type"]:
        self.getApplication().InvokeEvent('StartInteractionEvent')
        renderWindow = self.getView(event['view'])
        print("StartPinch")
        camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
        self.fp = camera.GetFocalPoint()
        self.pos = camera.GetPosition()
        self.zoom=0.0;
        
      if 'Pinch' in event["type"]:
        renderWindow = self.getView(event['view'])
        
        
        if renderWindow and 'scale' in event:
           scaleF=1.0
           zoomFactor = (event['scale']-self.zoom)/scaleF;
           #self.zoom=event['scale'];

           camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
           
           #delta = [self.fp[i] - self.pos[i] for i in range(3)]
           camera.Zoom(zoomFactor)

           #pos2 = camera.GetPosition()
           #camera.SetFocalPoint([pos2[i] + delta[i] for i in range(3)])
           renderWindow.Modified()

      if 'EndPinch' in event["type"]:
        self.getApplication().InvokeEvent('EndInteractionEvent')

      if 'StartPan' in event["type"]:
        self.getApplication().InvokeEvent('StartInteractionEvent')
        
        self.translate=[0.0,0.0];
        
      if 'Pan' in event["type"]:
        #print("pan")
        renderWindow = self.getView(event['view'])
        
        if renderWindow and 'translation' in event:
          
           print(event['translation'])
           rotateFactor = [event['translation'][i]-self.translate[i] for i in range(2)];
           self.translate[0] =event['translation'][0]
           self.translate[1] =event['translation'][1]

           camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
           
           
           camera.Elevation(rotateFactor[1]/20)
           camera.Azimuth(rotateFactor[0]/20)

           
           renderWindow.Modified()
       
      
      if 'StartRotate' in event["type"]:
        print("StartRotate")
      if 'Rotate' in event["type"]:
        print("Rotate") 
        renderWindow = self.getView(event['view'])
        
        if renderWindow and 'rotation' in event:
           print(event['rotation'])
           rotateFactor = event['rotation'];
           camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
           
                      
           if self.rotateX:
             camera.Azimuth(rotateFactor/10)
           else:
             camera.Elevation(rotateFactor/10)
           

           
           renderWindow.Modified()
        
     

      if 'End' in event["type"]:
        print("End")
        
