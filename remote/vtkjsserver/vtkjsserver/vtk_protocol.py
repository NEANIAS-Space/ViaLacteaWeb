import time
import math 
import os

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
        self.fitsReader2 = vtk.vtkVialactea.vtkFitsReader();
        
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
        self.currentContourActor = vtk.vtkLODActor();#vtk.vtkActor2D();#
        #self.currentContourActorForMainWindow = vtk.vtkLODActor();
        
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
        
        self.useContours=False;
        self.path=""
        self.sessionID="session_id_test"
        self.token=""
        self.fitsWasRead=False;
        self.istwoD=False;
        self.istwoDLoaded=False;
        self.istreeDLoaded=False;
        #folder to scan local files
        self.m_path = '/home/pvw-user/files'
        #self.m_path = '/home/evgeniya/Documents/GitHub/files'
        self.m_desc=''
        self.imageStack = vtk.vtkImageStack();
        self.isTwoDim=False;
        

    def updateScene(self, renderer, renWin):
        renderer.ResetCamera();
        renWin.GetInteractor().Render();
    def SetPath(self, path):
        self.path=path
        print(self.path)

    def removeContour(self):
        
        self.Ren2.RemoveActor2D(self.currentContourActor);
    
        #myParentVtkWindow->m_Ren1->RemoveActor2D(currentContourActorForMainWindow);
        #myParentVtkWindow->ui->qVTK1->update();
        #myParentVtkWindow->ui->qVTK1->renderWindow()->GetInteractor()->Render();
        #print("to impleent")
       
    
    def SetSession(self,s):
        self.sessionID=s;

    def goContour(self):
        self.removeContour();
        
        plane = vtk.vtkPlane();
        plane.SetOrigin(0,0, self.viewer.GetSlice());
        plane.SetNormal(0,0,1);
      

        cutter = vtk.vtkCutter();
        cutter.SetCutFunction(plane);
        cutter.SetInputData(self.fitsReader.GetOutput());
        cutter.Update();

        cutterMapper = vtk.vtkPolyDataMapper();
        cutterMapper.SetInputConnection( cutter.GetOutputPort());

        polyData = vtk.vtkPolyData();
        contoursFilter = vtk.vtkContourFilter();
        polyData = cutter.GetOutput();
        maxv=self.fitsReader.GetMax();
        minv=self.fitsReader.GetMin();
        rms=self.fitsReader.GetRMS();

        contoursFilter.GenerateValues(1, 3*rms,maxv );
        contoursFilter.SetInputConnection(cutter.GetOutputPort());
        contoursFilter.SetOutputPointsPrecision(1)
        contoursFilter.GenerateTrianglesOn ()

        contourLineMapperer = vtk.vtkPolyDataMapper();
        #print("Precis ",contoursFilter.GetOutputPointsPrecision())
        contourLineMapperer.SetInputConnection(contoursFilter.GetOutputPort());
       
        
       
        contourLineMapperer.SetScalarRange(3*rms, maxv);
        contourLineMapperer.ScalarVisibilityOn();
        contourLineMapperer.SetScalarModeToUsePointData();
        contourLineMapperer.SetColorModeToMapScalars();
        


        self.currentContourActor.SetMapper(contourLineMapperer);
        self.currentContourActor.GetProperty().SetLineWidth(1);
        
        

        self.Ren2.AddActor2D(self.currentContourActor);
        #self.renderWindow.GetInteractor().Render();
        self.renderWindow.Render()
        #print("contours are set");


    @exportRpc("vtk.getsession")
    def getSessionID(self):
        print("Session is")
        print(self.sessionID);
        return self.sessionID;
       
        
    @exportRpc("vtk.initialize.token")
    def setToken(self,token):
        self.token=token;
        print(self.token);

    @exportRpc("vtk.initialize.fits")
    def createVisualizationFits(self,token):
        print("start")
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
        
        self.token=token;
        print(token)
        fitsReader=self.fitsReader;
        
        #uncoment for multiuser
        fitsReader.SetTempPath(self.path)
        fitsReader.SetSessionToken(self.token)
        
        fitsReader.is3D=True;
        #fitsReader.GenerateVLKBUrl("40, 0,0.3,0.1");
        fitsReader.SetFileName("../../data/vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits");
        fitsReader.CalculateRMS();
            

        self.max=self.fitsReader.GetMax();
        self.min=self.fitsReader.GetMin();
        self.rms=self.fitsReader.GetRMS();
        print("Max_min read");
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
        legendScaleActor3d =  vtk.vtkVialactea.vtkLegendScaleActor2();
        legendScaleActor3d.LegendVisibilityOff();
        legendScaleActor3d.SetFitsFileName(fitsReader.GetFileName());
       
        
        renderer.AddActor(legendScaleActor3d);
        #print("legend scale fits was set")
       
        
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
         
         #NOTE: no need to allocate another one and read fits again
        #legendScaleActorImage =  vtk.vtkVialactea.vtkLegendScaleActor2();
        #legendScaleActorImage.LegendVisibilityOff();
        #legendScaleActor3d.SetFitsFileName(fitsReader.GetFileName());
        #legendScaleActorImage.setFitsFile(myfits);
        renderer2.AddActor(legendScaleActor3d);
        
        #updateScene();
        
        self.renderWindow.Render()
       
         
       
        camera = self.Ren1.GetActiveCamera()
        camera.SetViewUp( 0, 1, 0 )
        
        if self.useContours:
           self.goContour();

        
        
        renderer.ResetCamera()
        renderer2.ResetCamera()
        
        #Set coordinates for reset camera 
        # all actors where added to renderer for first pipeline above
        self.cam_init_pos=renderer.GetActiveCamera( ).GetPosition();
        self.cam_init_foc=renderer.GetActiveCamera( ).GetFocalPoint();
        
        renderWindow.Render()
        
        
        self.resetCamera();  

        return -1; #self.resetCamera()
        
    def init2DPipe(self):
        
        self.setFits2D()
        self.Set2DPipeWindowActors()
        self.istwoDLoaded=True;
        print("2D is set")
        
        
    def setFits2D(self):
        #fitsReader=self.fitsReader;
        
        #uncoment for multiuser
        self.fitsReader2.SetTempPath(self.path)
        self.fitsReader2.SetSessionToken(self.token)
        
        
        self.fitsReader2.is3D=False;
        #fitsReader.GenerateVLKBUrl("40, 0,0.3,0.1");
        self.fitsReader2.SetFileName("../../data/vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits");
        self.fitsReader2.Set3D(False);
        self.fitsReader2.CalculateRMS();
            

        self.max2=self.fitsReader2.GetMax();
        self.min2=self.fitsReader2.GetMin();
        self.rms2=self.fitsReader2.GetRMS();
        
        self.fitsWasRead2=True;
        
    def Set2DPipeWindowActors(self):         
        #Second pipeline
        #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/fce9cd964fa311afdf27353f0b6bc21918e5e603/Code/src/vtkwindow_new.cpp#L1178
        renderer3=self.Ren3;
        
        #rMin=self.fitsReader.GetRangeSliceMin(0)
        #rMax=self.fitsReader.GetRangeSliceMax(0)
        #print(rMin,rMax)
        min=self.fitsReader.GetMin();
        max=self.fitsReader.GetMax();
        delta=0;
        
        if min<=0:
          delta=1-min;
          min=1
          max=max+delta;
          
        resultScale = vtk.vtkImageShiftScale();
        resultScale.SetShift(delta)
        resultScale.SetOutputScalarTypeToFloat();
        resultScale.SetInputData( self.fitsReader.GetOutput() );

        resultScale.Update();

       
       

        
        
        lut = self.fitsReader.CreateLookTable("Gray");
        lut.SetTableRange( min, max );
        lut.SetScaleToLog10()
        
        lut.Build()
        print("Lut was build")
        #SelectLookTable("Gray",lut);
        #imageObject->setLutScale("Log");
        #imageObject->setLutType("Gray");
        
        fits=resultScale.GetOutput();
        self.fits_list=[fits];
        self.min_max=[[min,max,delta]]
        print("Fits list")
        
        colors =  vtk.vtkImageMapToColors();
        colors.SetInputData(resultScale.GetOutput());
        colors.SetLookupTable(lut);
        colors.Update();
        

        imageSliceMapperBase = vtk.vtkImageSliceMapper();

        imageSliceMapperBase.SetInputData(colors.GetOutput());
        

        imageSliceBase = vtk.vtkImageSlice();
        
        imageSliceBase.SetMapper(imageSliceMapperBase);
        print("11")
        imageSliceBase.GetProperty().SetInterpolationTypeToNearest();
        
        imageSliceBase.GetProperty().SetLayerNumber(0);

        print("12")

        # Stack
        #self.imageStack = vtk.vtkImageStack();
        self.imageStack.AddImage(imageSliceBase);


        self.legendScaleActor3d2 =  vtk.vtkVialactea.vtkLegendScaleActor2();
        self.legendScaleActor3d2.LegendVisibilityOff();
        self.legendScaleActor3d2.SetFitsFileName(self.fitsReader.GetFileName());
        print("13")
        renderer3.AddActor(self.legendScaleActor3d2);
        renderer3.AddViewProp(self.imageStack);
        renderer3.ResetCamera();

        #addLayer(imageObject);
        
        
       
        
        self.renderWindow.Render()
        print("Done rendeing 2D"); 
        
        
    def setRenderersToken(self,token,t):
        print("start")
        #Get renwin and renderers
        
        #rends=self.renderWindow.GetRenderers()
        #it=rends.NewIterator()
        #renderer = rends.GetItemAsObject(0)
        #renderer2 = rends.GetItemAsObject(1)	
        #renderer2.SetBackground(0.21,0.23,0.25);
        
        renderer = vtk.vtkRenderer()
        renderer2 = vtk.vtkRenderer()
        renderer3 = vtk.vtkRenderer()
        self.Ren1=renderer;
        self.Ren2=renderer2;
        self.Ren3=renderer3;
        
        if t==0:
           self.renderWindow.AddRenderer(renderer)
           self.renderWindow.AddRenderer(renderer2)
         
           renderer.SetViewport(0,0,0.5,1)
           renderer2.SetViewport(0.5,0,1,1)
           renderer2.SetBackground(0.21,0.23,0.25);
        
           #Entry point to entire vis logic:
           #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L1328
        
        
        
           #First pipeline as described in 
           #https://github.com/NEANIAS-Space/ViaLacteaVisualAnalytics/blob/master/Code/src/vtkwindow_new.cpp#L1386
        else:
           self.renderWindow.AddRenderer(renderer3)
           renderer3.SetBackground(0.21,0.23,0.25);
           print("2D is set");
           
        self.token=token;
        print(token);
        
        
    def setFits(self):
        #fitsReader=self.fitsReader;
        
        #uncoment for multiuser
        self.fitsReader.SetTempPath(self.path)
        self.fitsReader.SetSessionToken(self.token)
        
        self.fitsReader.is3D=True;
        #fitsReader.GenerateVLKBUrl("40, 0,0.3,0.1");
        self.fitsReader.SetFileName("../../data/vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits");
        self.fitsReader.CalculateRMS();
            

        self.max=self.fitsReader.GetMax();
        self.min=self.fitsReader.GetMin();
        self.rms=self.fitsReader.GetRMS();
        
        self.fitsWasRead=True;
        
    def SetLeftWindowActors(self): 
        
        renderer=self.Ren1;
        #outline
        
        outlineF = vtk.vtkOutlineFilter();
        outlineF.SetInputData(self.fitsReader.GetOutput());
        
        
        outlineM = vtk.vtkPolyDataMapper();
        outlineM.SetInputConnection(outlineF.GetOutputPort());
        outlineM.ScalarVisibilityOff();

        outlineA = vtk.vtkActor();
        outlineA.SetMapper(outlineM);

	#isosurface itself Marching cubes
        shellE = self.cone
        shellE.SetInputData(self.fitsReader.GetOutput())
        shellE.ComputeNormalsOff();
        shellE.SetValue(0, 3*self.fitsReader.GetRMS())
        shellE.Update()
        print("cellsNum=", shellE.GetOutput().GetNumberOfCells())
        
        shellM = vtk.vtkPolyDataMapper()
        shellM.ScalarVisibilityOff();
        shellA = vtk.vtkActor()

        shellM.SetInputConnection(shellE.GetOutputPort())
        shellA.SetMapper(shellM)
        
        shellA.GetProperty().SetColor(1.0, 0.5, 0.5);

        
        # slice L1406
        
        bounds=self.fitsReader.GetOutput().GetBounds()
        
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
        vtkAxesWidget.SetInteractor(self.renderWindow.GetInteractor());

        vtkAxesWidget.SetOrientationMarker(axes);

        vtkAxesWidget.SetOutlineColor( 0.9300, 0.5700, 0.1300 );
        vtkAxesWidget.SetViewport( 0.0, 0.0, 0.2, 0.2 );
        vtkAxesWidget.SetEnabled(1);
        vtkAxesWidget.InteractiveOff();
        
                
        #TODO import custom legend
        self.legendScaleActor3d =  vtk.vtkVialactea.vtkLegendScaleActor2();
        self.legendScaleActor3d.LegendVisibilityOff();
        self.legendScaleActor3d.SetFitsFileName(self.fitsReader.GetFileName());
       
        
        renderer.AddActor(self.legendScaleActor3d);
        print("legend scale fits was set")
       
        
        #add label
        tprop = vtk.vtkTextProperty()
        tprop.SetFontFamilyToArial()
        tprop.SetFontSize(10)
        tprop.BoldOff()
        tprop.ShadowOff()
        tprop.SetColor(1, 1, 1)
        #self.textActor.SetDisplayPosition(205, 205)
        #self.textActor.SetTextProperty(tprop);
        self.textActor.SetInput(self.fitsReader.GetDataCubeData())
        renderer.AddActor(self.textActor);
        print("Text actor was set")
        
        
    def SetRightWindowActors(self):         
        #Second pipeline
        renderer2=self.Ren2;
        
        rMin=self.fitsReader.GetRangeSliceMin(0)
        rMax=self.fitsReader.GetRangeSliceMax(0)
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
    
        print("lutBuild") 
        self.viewer.SetRenderer(renderer2);
        self.viewer.SetRenderWindow(self.renderWindow);
        self.viewer.SetupInteractor(self.renderWindow.GetInteractor());
        self.viewer.SetInputData(self.fitsReader.GetOutput());
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
         
         #NOTE: no need to allocate another one and read fits again
        #legendScaleActorImage =  vtk.vtkVialactea.vtkLegendScaleActor2();
        #legendScaleActorImage.LegendVisibilityOff();
        #legendScaleActor3d.SetFitsFileName(fitsReader.GetFileName());
        #legendScaleActorImage.setFitsFile(myfits);
        renderer2.AddActor(self.legendScaleActor3d);
        
        #updateScene();
        
        self.renderWindow.Render()
       
         
       
        camera = self.Ren1.GetActiveCamera()
        camera.SetViewUp( 0, 1, 0 )
        
        if self.useContours:
           self.goContour();

        
        
       
        
    def createScene3D(self):
        #self.setFits();
        
        
        self.SetLeftWindowActors();
        self.SetRightWindowActors();
        print("Done") 
      
        self.Ren1.ResetCamera()
        self.Ren2.ResetCamera()
        
        #Set coordinates for reset camera 
        # all actors where added to renderer for first pipeline above
        self.cam_init_pos=self.Ren1.GetActiveCamera( ).GetPosition();
        self.cam_init_foc=self.Ren1.GetActiveCamera( ).GetFocalPoint();
        
       
        print(self.cam_init_pos)
        
        #getInteractorStyle info to check
       
        print("Interactor type final check") 
        name=self.renderWindow.GetInteractor().GetInteractorStyle().GetClassName()
        print(name)
        
     
        
        
        self.renderWindow.Render()
        
        
        self.resetCamera();  
        #currently is setted this one
        self.fitsWasRead=True;
        self.istreeDLoaded=True;
        print("3D scene created");
        
            
        
    def scantree(self, path):
       l=len(os.listdir(path))
       i=0;
       for entry in os.scandir(path):
         if entry.is_dir(follow_symlinks=False):
            self.m_desc=self.m_desc+'{\n'
            self.m_desc=self.m_desc+'"path": "';
            self.m_desc=self.m_desc+path;
            self.m_desc=self.m_desc+'",\n';
            self.m_desc=self.m_desc+'"name": "';
            self.m_desc=self.m_desc+entry.name;
            self.m_desc=self.m_desc+'",\n';
            self.m_desc=self.m_desc+'"type": "directory",\n';
            self.m_desc=self.m_desc+'"children": [\n'
            yield from self.scantree(entry.path)  
            self.m_desc=self.m_desc+']\n'
            i=i+1;
            if i==l:
              self.m_desc=self.m_desc+'}\n'
            else:
              self.m_desc=self.m_desc+'},\n'
         else:
            self.m_desc=self.m_desc+'{\n'
            self.m_desc=self.m_desc+'"path": "';
            self.m_desc=self.m_desc+path;
            self.m_desc=self.m_desc+'",\n'
            self.m_desc=self.m_desc+'"name": "';
            self.m_desc=self.m_desc+entry.name;
            self.m_desc=self.m_desc+'",\n'
            self.m_desc=self.m_desc+'"type": "file"\n';
            i=i+1;
            if i==l:
              self.m_desc=self.m_desc+'}\n'
            else:
              self.m_desc=self.m_desc+'},\n'
            yield entry


    @exportRpc("vtk.image.initialize")
    def createImageVisualization(self,token):
        renderWindow = self.getView('-1')
        self.renderWindow=renderWindow;
        print("Local files scanning")
        self.m_desc=self.m_desc+'[\n'#{\n'
        
        for entry in self.scantree(self.m_path):
          print(entry)
        self.m_desc=self.m_desc+']\n'
        
        print (self.m_desc)


        # Set Renderers and Token
        print("Setting 2D ")
        self.setRenderersToken(token,1);
        #self.setFits();
        
        if self.fitsWasRead:
          self.Set2DPipeWindowActors();
          #self.SetLeftWindowActors();
          #self.SetRightWindowActors();
        
      
        self.Ren3.ResetCamera()
          
  
        
        self.renderWindow.Render()
        
        self.istreeDLoaded=True;
        print("2D rendered");
        return self.m_desc; #-1; #self.resetCamera()
 
    def createImageStack(self):
        #self.setFits();
        
        self.isTwoDim=True;
        self.Set2DPipeWindowActors()
        #self.SetLeftWindowActors();
        #self.SetRightWindowActors();
        #print("Done") 
      
        #self.Ren1.ResetCamera()
        #self.Ren2.ResetCamera()
        
        #Set coordinates for reset camera 
        # all actors where added to renderer for first pipeline above
        #self.cam_init_pos=self.Ren1.GetActiveCamera( ).GetPosition();
        #self.cam_init_foc=self.Ren1.GetActiveCamera( ).GetFocalPoint();
        
       
        #print(self.cam_init_pos)
        
        #getInteractorStyle info to check
       
        #print("Interactor type final check") 
        #name=self.renderWindow.GetInteractor().GetInteractorStyle().GetClassName()
        #print(name)
        
     
        
        
        self.renderWindow.Render()
        
        
        self.fitsWasRead=True;
        
  
                               

    @exportRpc("vtk.cone.changeopacity")
    def changeOpacity(self,res):
        print ("Opacity Change2")  
        p=res.split(",");
        objN=int(p[0])
        opacity=float(p[1])
        
        print("object at {:d},".format(objN));
        print(opacity)
        
        slice=self.imageStack.GetImages().GetItemAsObject(objN);
        my_slice = vtk.vtkImageSlice().SafeDownCast(slice)
        #my_slice.ShallowCopy(slice)
        my_slice.Modified()
        my_slice.GetProperty().SetOpacity(opacity/ 100.0);
        my_slice.Modified()
        self.renderWindow.Render()
        self.getApplication().InvalidateCache(self.renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')           
        
        
    @exportRpc("vtk.cone.changevisibility")
    def changeVisibility(self,res):
        print ("Visitility Change")  
        p=res.split(",");
        objN=int(p[0]) #hack - change later
        status=(p[1])
        
        print("object at {:d}, visibility {:s}".format(objN, status));
        slice=self.imageStack.GetImages().GetItemAsObject(objN);
        my_slice = vtk.vtkImageSlice().SafeDownCast(slice)
        #my_slice.ShallowCopy(slice)
        my_slice.Modified()
        #help(my_slice)
        if status=="true":
          
          my_slice.VisibilityOn();
        else:
          my_slice.VisibilityOff();
          
        self.renderWindow.Render() 
        self.getApplication().InvalidateCache(self.renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')           
        
    @exportRpc("vtk.cone.changepalette")
    def changePalette(self,res):
        #num in imageStack, palette, scale
        
        print ("Rescaling image")  
        p=res.split(",");
        objN=int(p[0])
        objId=int(p[1])
        palete=str(p[2])
        myscale =str(p[3])
        #int sourceStart, int sourceEnd,  int destinationRow
        print("object at {:d}, num {:d}, palette {:s}, scale {:s}".format(objN, objId, palete, myscale));
        
        #vtkImageSlice
        slice=self.imageStack.GetImages().GetItemAsObject(objN);
        my_slice = vtk.vtkImageSlice().SafeDownCast(slice)
        my_slice.Modified()
        #map=slice.GetMapper();
        input=self.fits_list[objId]
        m_r=self.min_max[objId];#.append([min,max,delta])
        
        #min and max of fits should be saved before
        #min = imgLayerList.at(pos)->getFits()->GetMin();
        #if (min < 0)
        #min = 0;
        #float max = imgLayerList.at(pos)->getFits()->GetMax();
        
        lut = self.fitsReader.CreateLookTable(palete);

        
        
    

        lut.SetTableRange(m_r[0],m_r[1]);
       
        if myscale == "Linear":
           lut.SetScaleToLinear();
        else:
           lut.SetScaleToLog10();
        
        print("Lut updated")
        #SelectLookTable(palette.c_str(), lut);
        
        colors = vtk.vtkImageMapToColors();
        # We have to store both list of images and imageStack
        colors.SetInputData(input); #get from stack
        colors.SetLookupTable(lut);
        colors.Update();
        
        print("Fits updated")

        imageSliceMapperLutModified =vtk.vtkImageSliceMapper();
        imageSliceMapperLutModified.SetInputData(colors.GetOutput());
        
        my_slice.SetMapper(imageSliceMapperLutModified);
        my_slice.Modified()
        print("Palette applied")
        self.renderWindow.Render()
        self.getApplication().InvalidateCache(self.renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')  

        
                
    @exportRpc("vtk.cone.load.image")
    def loadImage(self,url):

        print ("Load 2D image")
        if self.fitsWasRead==False: #not loaded as far
           #uncoment for multiuser
           self.fitsReader.SetTempPath(self.path)
           self.fitsReader.SetSessionToken(self.token)

        #loading 2D image
        self.fitsReader.is3D=False;
        print("Start downloading from");
        print(url)
        self.fitsReader.Set3D(False);
        print("Downloaded");
        #result=self.fitsReader.DownloadSurveyDataCube(url);
        self.fitsReader.SetFileName("../../data/vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits");
        if self.imageStack.GetImages().GetNumberOfItems()==1:
           self.fitsReader.SetFileName("../../data/vlkb-cutout_2021-02-18_12-33-05_516569_JCMT-HARP_COHRS_18p00_0p00_CUBE_REBIN_R1.fits");
        print("stat 2D");
        self.fitsReader.CalculateRMS();
        print("success 2D");
           
        self.max=self.fitsReader.GetMax();
        self.min=self.fitsReader.GetMin();
        #self.rms=self.fitsReader.GetRMS();
        
        
        
        if self.fitsWasRead==False:
              #self.createScene3D();
              self.createImageStack();
              print("First image was added")
        else:
              self.addLayerImage()
              print("Secondary image was added")
        print("Pos updated ");
        
        
        
        
        return 1;
        
    @exportRpc("vtk.initialize")
    def createVisualization(self,token):
        renderWindow = self.getView('-1')
        self.renderWindow=renderWindow;
        print("Scanning start")
        self.m_desc=self.m_desc+'[\n'#{\n'
        
        for entry in self.scantree(self.m_path):
          print(entry)
        self.m_desc=self.m_desc+']\n'
        
        print (self.m_desc)


        # Set Renderers and Token
        self.setRenderersToken(token,0);
        #self.setFits();
        
        if self.fitsWasRead:
          self.SetLeftWindowActors();
          self.SetRightWindowActors();
        
      
          self.Ren1.ResetCamera()
          self.Ren2.ResetCamera()
        
          #Set coordinates for reset camera 
          # all actors where added to renderer for first pipeline above
          self.cam_init_pos=self.Ren1.GetActiveCamera( ).GetPosition();
          self.cam_init_foc=self.Ren1.GetActiveCamera( ).GetFocalPoint();
        
       
        
        
        
        
       
          print(self.cam_init_pos)
        
        
     
        
        
          self.renderWindow.Render()
        
        
          self.resetCamera();  
          #currently is setted this one
          self.istreeDLoaded=True;

        return self.m_desc; #-1; #self.resetCamera()
        
        

    def ResetCam():
        renderWindow = self.getView('-1')
        
        rends=renderWindow.GetRenderers()
        
        renderer = rends.GetItemAsObject(0)
        renderer2 = rends.GetItemAsObject(1)	
        renderer.ResetCamera()
        renderer2.ResetCamera()
        renderWindow.Render()

    @exportRpc("vtk.cone.movedlayersrow")           
    def movedLayersRow(self, res):
        print ("Moving image")  
        p=res.split(",");
        sourceStart=int(p[0])
        sourceEnd=int(p[1])
        destinationRow =int(p[2])
        #int sourceStart, int sourceEnd,  int destinationRow
        print("sourceStart {:d}, sourceEnd {:d}, destinationRow {:d}".format(sourceStart, sourceEnd, destinationRow));
        
        #curl_easy_perform() failed: Couldn't connect to server

    
   
        if sourceStart>destinationRow:
             #down
             print("Move down ")
             sliceB=self.imageStack.GetImages().GetItemAsObject(sourceStart);
             my_sliceB = vtk.vtkImageSlice().SafeDownCast(sliceB)
             my_sliceB.Modified()
             
             for i in range(sourceStart-1,destinationRow-1,-1):
                
                slice=self.imageStack.GetImages().GetItemAsObject(i);
                my_slice = vtk.vtkImageSlice().SafeDownCast(slice)
                my_slice.Modified()
                print(my_slice.GetProperty().GetLayerNumber())
                print(i+1)
                my_slice.GetProperty().SetLayerNumber(i+1)
                my_slice.Modified()
                #base_image.GetProperty().SetLayerNumber(0)
                #top_image.GetProperty().SetLayerNumber(1)
                #stack.SetActiveLayer(0)
                
                #vtkImageSlice::SafeDownCast(imageStack->GetImages()->GetItemAsObject(i))->GetProperty()->SetLayerNumber(i+1);
                #imgLayerList.swapItemsAt(i,i+1);
 
             
             print(my_sliceB.GetProperty().GetLayerNumber())
             print(destinationRow)
             my_sliceB.GetProperty().SetLayerNumber(destinationRow)
             my_sliceB.Modified()
             #vtkImageSlice::SafeDownCast(imageStack->GetImages()->GetItemAsObject(sourceStart))->GetProperty()->SetLayerNumber(destinationRow);

        else:
             #up
             print("Move up")
             for i in range(sourceStart+1,destinationRow+1,1):
                print(i)
                slice=self.imageStack.GetImages().GetItemAsObject(i);
                my_slice = vtk.vtkImageSlice().SafeDownCast(slice)
                my_slice.Modified()
                my_slice.GetProperty().SetLayerNumber(i-1)
                my_slice.Modified()
                
                #vtkImageSlice::SafeDownCast(imageStack->GetImages()->GetItemAsObject(i))->GetProperty()->SetLayerNumber(i-1);
                #imgLayerList.swapItemsAt(i,i-1);

             sliceB=self.imageStack.GetImages().GetItemAsObject(sourceStart);
             my_sliceB = vtk.vtkImageSlice().SafeDownCast(sliceB)
             my_sliceB.Modified()
             my_sliceB.GetProperty().SetLayerNumber(destinationRow)
             my_sliceB.Modified()
             print(destinationRow)
            
             #vtkImageSlice::SafeDownCast(imageStack->GetImages()->GetItemAsObject(sourceStart))->GetProperty()->SetLayerNumber(destinationRow-1);
        self.renderWindow.Render()
        self.getApplication().InvalidateCache(self.renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')
    

    @exportRpc("vtk.cone.addlayerimage")   
    def addLayerImage(self):
        print ("Adding layer image")
        min=self.fitsReader.GetMin();
        max=self.fitsReader.GetMax();
        delta=0;
        
        if min<=0:
          delta=1-min;
          min=1
          max=max+delta;
          
        resultScale = vtk.vtkImageShiftScale();
        resultScale.SetShift(delta)
        resultScale.SetOutputScalarTypeToFloat();
        resultScale.SetInputData( self.fitsReader.GetOutput() )
        resultScale.Update();
        
        lut = self.fitsReader.CreateLookTable("Gray");

        

        lut.SetTableRange(min,max);

        lut.SetScaleToLog10();
        print("Lut is set")
        self.fits_list.append(resultScale.GetOutput())
        self.min_max.append([min,max,delta])
        print("Fits is updated")
        #SelectLookTable("Gray",lut);

        colors =  vtk.vtkImageMapToColors();
        colors.SetInputData(resultScale.GetOutput());
        colors.SetLookupTable(lut);
        colors.Update();

        imageSliceMapperLayer = vtk.vtkImageSliceMapper();
        imageSliceMapperLayer.SetInputData(colors.GetOutput());

        imageSliceLayer = vtk.vtkImageSlice();
        imageSliceLayer.SetMapper(imageSliceMapperLayer);
        imageSliceLayer.GetProperty().SetOpacity(0.5);
        imageSliceLayer.GetProperty().SetInterpolationTypeToNearest();
        
        #double angle  = 0;

        #double x1=coord[0];
        #double y1=coord[1];

        #..

       
        transform = vtk.vtkTransform()
  
        bounds=self.fitsReader.GetOutput().GetBounds()
       
        # TODO: angle should be calculated above
        angle=0.0;
        # Rotate about the origin point (world coordinates)
        transform.Translate(bounds[0], bounds[2], bounds[4]);
        transform.RotateWXYZ(angle, 0, 0, 1);
        transform.Translate(-bounds[0], -bounds[2], -bounds[4]);
        imageSliceLayer.SetUserTransform(transform);
       
        imageSliceLayer.GetProperty().SetLayerNumber(self.imageStack.GetImages().GetNumberOfItems());

        self.imageStack.AddImage(imageSliceLayer);

        #addLayer(img);

        #if(rectangleActor!=0){
        # m_Ren1->RemoveActor(rectangleActor);
        #}

        
    
    @exportRpc("vtk.cone.fits.update")
    def updateFits(self,url):

        print ("check scene2")
        if self.fitsWasRead==False: #not loaded as far
           #uncoment for multiuser
           self.fitsReader.SetTempPath(self.path)
           self.fitsReader.SetSessionToken(self.token)

        self.fitsReader.is3D=True;
        print("Start downloading from");
        print(url)

        result=self.fitsReader.DownloadSurveyDataCube(url);
        if result:
           print("stat updating2");
           self.fitsReader.Set3D(True);
           self.fitsReader.CalculateRMS();
           
           self.max=self.fitsReader.GetMax();
           self.min=self.fitsReader.GetMin();
           self.rms=self.fitsReader.GetRMS();
           
           #udate scene
           if self.fitsWasRead==False:
             self.createScene3D();
           
        
           fits=self.fitsReader.GetOutput();
           bounds=fits.GetBounds()
        
           self.textActor.SetInput(self.fitsReader.GetDataCubeData())
           self.textActor.Modified();
           self.textActor.GetMapper().Update()
        
           self.sliceE.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], 0, 1);
           self.frustumSource.Update()
           print("Cube loaded")
        #self.ResetCamera()
        return result;


    @exportRpc("vtk.cone.fits.localupdate")
    def updateFitslocal(self,fits):
           

        print ("check scene2 local")
        if self.fitsWasRead==False: #not loaded as far
           #uncoment for multiuser
           #self.fitsReader.SetTempPath('')
           self.fitsReader.SetSessionToken(self.token)
        self.fitsReader.Set3D(True);
        self.fitsReader.is3D=True;
        print("Start downloading from");
        print(fits)
        #result=self.fitsReader.DownloadSurveyDataCube(url);
        self.fitsReader.SetFileName(fits);
        #SetFileName("../../data/vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits");
        
        print("Downloaded");
        # uncomment
        #self.fitsReader.Set3D(True);
        result=self.fitsReader.CalculateRMS();
        print("RMS calc");  
        self.max=self.fitsReader.GetMax();
        self.min=self.fitsReader.GetMin();
        self.rms=self.fitsReader.GetRMS();
        print("stat updating3");
        
        
        if self.fitsWasRead==False:
             self.createScene3D();
        
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
        self.resetCamera();  
        print("3D Fits updated");
        
        
        
        return result;





    @exportRpc("vtk.camera.reset")
    def resetCamera(self):
        renderWindow = self.getView('-1')
       
        
        renderWindow.GetRenderers().GetFirstRenderer().ResetCamera()
        renderWindow.Render()
        
        camera = renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera();
        renderer=renderWindow.GetRenderers().GetFirstRenderer()
        
        #camera.SetFocalPoint( self.cam_init_foc );
        #camera.SetPosition( self.cam_init_pos);
        
        #renderWindow.GetRenderers().GetFirstRenderer().SetViewUp( 0, 1, 0 );
        #renderWindow.GetRenderers().GetFirstRenderer().SetFocalPoint( self.cam_init_foc );
        #renderWindow.GetRenderers().GetFirstRenderer().SetPosition( self.cam_init_pos);

        self.getApplication().InvalidateCache(renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')

         #Set coordinates for reset camera 
        # all actors where added to renderer for first pipeline above
        #self.cam_init_pos=camera.GetPosition();
        #self.cam_init_foc=camera.GetFocalPoint();
        return -1
        
    @exportRpc("vtk.cone.url")
    def loadURL(self):
        print("FitsReader callse");
        self.fitsReader.SetSessionToken(self.token)

        self.fitsReader.is3D=True;
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
        
        if self.fitsWasRead==False: #not loaded as far
           #uncoment for multiuser
           self.fitsReader.SetTempPath(self.path)
           #self.fitsReader.SetSessionToken(self.token)
        
           #self.fitsReader.is3D=True;
           
           
           
           
        self.fitsReader.SetSessionToken(self.token)

        self.fitsReader.is3D=True;
        print(self.token);
        
        self.fitsReader.GenerateVLKBUrl(res);
        self.fitsReader.Set3D(True);
        result= self.fitsReader.CalculateRMS();
        print ("Get to Max");
        self.max=self.fitsReader.GetMax();
        self.min=self.fitsReader.GetMin();
        self.rms=self.fitsReader.GetRMS();
        
        if self.fitsWasRead==False:
           self.createScene3D();
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
        
    @exportRpc("vtk.cone.loadcubedata")
    def getDataCubeData(self):
        #print("calling GETFITSDATA");
        tmin=self.fitsReader.GetMin()
        tmax=self.fitsReader.GetMax()
        rms=self.fitsReader.GetRMS()
        tmin/=rms;
        tmax/=rms;
        pmin=1
        pmax=self.fitsReader.GetNaxes(2)
        return [tmin,tmax,1,pmax];


    @exportRpc("vtk.cone.resolution.update")
    def updateResolution(self, resolution):
        self.cone.SetValue(0, resolution*self.rms)
        self.cone.Update()
        renderWindow = self.getView('-1')
        # renderWindow.Modified() # either modified or render
        renderWindow.Render()
        self.getApplication().InvokeEvent('UpdateEvent')
    
    @exportRpc("vtk.cone.contours.update")
    def updateContours(self,contours):
        
        print("FitsReader contours");
        self.useContours=contours;
        if self.useContours:
           self.goContour()
        else :
           self.removeContour()
        self.renderWindow.Render()
        #self.renderWindow.GetInteractor().Render();
        self.getApplication().InvalidateCache(self.renderWindow)
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
        #print("Start contours");
        if self.useContours:
           self.goContour();

        

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
                     #self.getApplication().InvokeEvent('StartInteractionEvent')
                   if self.isTwoDim==False:
                     
                     if x<0.5:
                 
                        
                     
                        dx=self.x1-x
                        dy=self.y1-y
                        #print(x,y)
                        #x,y are normalised from 0 to 1
                        size=self.renderWindow.GetSize();
                        delta_elevation = self.winScale*80.0 / size[1];
                        delta_azimuth = self.winScale*160.0 / size[0];
                     
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
                      
                        self.renderWindow.Modified()


                        
                   else: #self.isTwoDim:   
                     #print("2D window scale")
                     size=self.renderWindow.GetSize();
                     delta_y = self.winScale*80.0 / size[1];
                     delta_x = self.winScale*160.0 / size[0];
                     window = self.imageStack.GetProperty().GetColorWindow()
                     level = self.imageStack.GetProperty().GetColorLevel()
                     dx=(self.x1-x)*delta_x;
                     dy=(self.y1-y)*delta_y;
                      
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
                        

                     if window < 0.0:
                         dx = -1 * dx;
                     if level < 0.0:
                         dy = -1 * dy;
                     newWindow = dx + window;
                     newLevel = level - dy;

                     if newWindow < 0.01:
                          newWindow = 0.01;
                     self.imageStack.GetProperty().SetColorWindow(newWindow)
                     self.imageStack.GetProperty().SetColorLevel(newLevel);
                      

                                          
                   self.renderWindow.Modified()
                     
                 
                 else:
                    self.getApplication().InvokeEvent('StartInteractionEvent')
                    #print("Start")
                 self.x1=x
                 self.y1=y
             if event['shiftKey']==1:
                 #vtkInteractorStyleImage
                 #https://github.com/Kitware/VTK/blob/master/Interaction/Style/vtkInteractorStyleImage.cxx
                 
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
                     #self.getApplication().InvokeEvent('StartInteractionEvent')
                     print("pan")
                     camera = self.renderWindow.GetRenderers().GetFirstRenderer().GetActiveCamera()
                     viewFocus=camera.GetFocalPoint();
                     print(viewFocus[0],viewFocus[1],viewFocus[2])
                     viewFocus=self.ComputeWorldToDisplay(viewFocus[0], viewFocus[1], viewFocus[2]);
                     focalDepth = viewFocus[2];
                     print(viewFocus[0],viewFocus[1],viewFocus[2])
                     newPickPoint=self.ComputeDisplayToWorld(x,y,focalDepth);
                     print(newPickPoint[0],newPickPoint[1],newPickPoint[2])

                     # Has to recalc old mouse point since the viewport has moved,
                     # so can't move it outside the loop

                     oldPickPoint=self.ComputeDisplayToWorld(self.x1,self.y1,focalDepth)
                     
                     #Camera motion is reversed
                     
                        
                     motionVector=[0,0,0]
                     motionVector[0] = self.winScale*(oldPickPoint[0] - newPickPoint[0]);
                     motionVector[1] = self.winScale*(oldPickPoint[1] - newPickPoint[1]);
                     motionVector[2] = self.winScale*(oldPickPoint[2] - newPickPoint[2]);
                     print("Motion ",motionVector[0],motionVector[1],motionVector[2])

                     viewFocus=camera.GetFocalPoint();
                     viewPoint=camera.GetPosition();
                     camera.SetFocalPoint(motionVector[0] + viewFocus[0], motionVector[1] + viewFocus[1], motionVector[2] + viewFocus[2]);

                     camera.SetPosition(motionVector[0] + viewPoint[0], motionVector[1] + viewPoint[1], motionVector[2] + viewPoint[2]);
                     self.renderWindow.Modified()
                     self.getApplication().InvalidateCache(self.renderWindow)
                     self.getApplication().InvokeEvent('UpdateEvent')
                     print("Panning done")
                 else:
                    self.getApplication().InvokeEvent('StartInteractionEvent')
                    #print("Start")
                 self.x1=x
                 self.y1=y

         
         if event['action']=='up': #end of interaction
             self.x1=-1000000
             self.y1=-1000000   
             self.getApplication().InvokeEvent('EndInteractionEvent') 
             #print("End") 
                 
                 
             
    def ComputeWorldToDisplay(self,x,y,z):
       renderer=self.renderWindow.GetRenderers().GetFirstRenderer()
       renderer.SetWorldPoint(x, y, z, 1.0);
       renderer.WorldToDisplay();
       displayPt=renderer.GetDisplayPoint();
       return displayPt;
       
    def ComputeDisplayToWorld(self,x, y, z):
       renderer=self.renderWindow.GetRenderers().GetFirstRenderer()
       renderer.SetDisplayPoint(x, y, z);
       renderer.DisplayToWorld();
     
       worldPt=renderer.GetWorldPoint();
       pt=[0.0,0.0,0.0,0.0]
       if worldPt[3]!=0:
         
          pt[0]= float(worldPt[0])/float(worldPt[3])
         
          pt[1]= worldPt[1]/worldPt[3]
          pt[2]= worldPt[2]/worldPt[3]
          
          pt[3] = 1.0;
        
       return pt;
       
    @exportRpc("vtk.cone.changeselected")
    def changeSelected(self, res):
       print("Active layer ",res);
       self.imageStack.SetActiveLayer(int(res));
       self.renderWindow.Render();
    
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
        self.getApplication().InvalidateCache(self.renderWindow)
        self.getApplication().InvokeEvent('UpdateEvent')
        print("done")
    
    @exportRpc("vtk.cone.rotate.update")
    def updateRotateAxis(self, v):
        print("update rot")
        self.rotateX=v;
        print(self.rotateX)
        
    @exportRpc("vtk.cone.dim.update")
    def updateDim(self, v):
        prev=self.istwoD;
        if self.istwoD!=v:
           self.istwoD=v;
           if self.istwoD==0:
               
               self.renderWindow.RemoveRenderer (self.Ren1)
               self.renderWindow.RemoveRenderer (self.Ren2)
               if self.istwoDLoaded==False:
                  #initialize 2D pipeline
                  self.init2DPipe()
                  
               if prev!=2:
                   self.renderWindow.AddRenderer(self.Ren3)
               self.Ren3.SetViewport(0.0,0,1,1)
               self.Ren3.SetBackground(0.81,0.13,0.15);
               print("2d");
           else:
            if self.istwoD==1:
              self.renderWindow.RemoveRenderer (self.Ren3)
              if prev==2:
                   self.renderWindow.RemoveRenderer (self.Ren1)
                   self.renderWindow.RemoveRenderer (self.Ren2)
                   
              self.renderWindow.AddRenderer(self.Ren1)
              self.renderWindow.AddRenderer(self.Ren2)
         
              self.Ren1.SetViewport(0,0,0.5,1)
              self.Ren2.SetViewport(0.5,0,1,1)
              print("3d");
            else:
              if prev==1:
                   self.renderWindow.RemoveRenderer (self.Ren1)
                   self.renderWindow.RemoveRenderer (self.Ren2)
              else: 
                   self.renderWindow.RemoveRenderer (self.Ren3)
                   
              
              
              self.renderWindow.AddRenderer(self.Ren1)
              self.renderWindow.AddRenderer(self.Ren2)
              self.renderWindow.AddRenderer(self.Ren3)
              self.Ren3.SetBackground(0.81,0.13,0.15);
              self.Ren1.SetViewport(0,0,0.35,1)
              self.Ren2.SetViewport(0.35,0,0.7,1)
              self.Ren3.SetViewport(0.7,0,1,1)
               
              print("Mixed");
        self.renderWindow.Render()
        
        
        self.resetCamera();  

        print("Done");
        

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
        
