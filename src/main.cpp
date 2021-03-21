

#include "vtkFitsReader.h"
#include "vtkPolyDataMapper.h"
#include <vtkAutoInit.h>
#include <vtkCallbackCommand.h>
#include <vtkCamera.h>
#include <vtkColorTransferFunction.h>
#include <vtkFrustumSource.h>
#include <vtkGPUVolumeRayCastMapper.h>
#include <vtkImageMapToColors.h>
#include <vtkImageProperty.h>
#include <vtkImageShiftScale.h>
#include <vtkImageSlice.h>
#include <vtkImageSliceMapper.h>
#include <vtkImageStack.h>
#include <vtkInteractorObserver.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkLookupTable.h>
#include <vtkMarchingCubes.h>
#include <vtkMath.h>
#include <vtkOutlineFilter.h>
#include <vtkPiecewiseFunction.h>
#include <vtkPlanes.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkTimerLog.h>
#include <vtkTransform.h>
#include <vtkVolumeProperty.h>
#include <vtkPNGWriter.h>
#include <vtkWindowToImageFilter.h>

#include <string>
#include <iterator>
#include <iostream>
#include <algorithm>
#include <array>
#include <iostream>
#include <fstream>

VTK_MODULE_INIT(vtkRenderingOpenGL2);
VTK_MODULE_INIT(vtkInteractionStyle);

static std::ofstream myfile;

void CallbackFunction(vtkObject *caller, long unsigned int vtkNotUsed(eventId),
                      void *vtkNotUsed(clientData),
                      void *vtkNotUsed(callData)) {
  vtkRenderer *renderer = static_cast<vtkRenderer *>(caller);

  double timeInSeconds = renderer->GetLastRenderTimeInSeconds();
  double fps = double(1.0) / timeInSeconds;

}


int test_structured(const char* filename) {

double time_before=0;
double fps_avarage=0;
double s_min=0;
double s_max=0;
int num_of_cells=0;
int screen_res=1600;

// measuring the pipeline performance
 vtkSmartPointer<vtkTimerLog> clock = vtkSmartPointer<vtkTimerLog>::New();
  clock->StartTimer();
  
  vtkSmartPointer<vtkFitsReader> fitsReader =
      vtkSmartPointer<vtkFitsReader>::New();
  fitsReader->is3D = true;
  fitsReader->SetFileName(filename);
  // fitsReader->Update();

  vtkStructuredPoints *myfits = fitsReader->GetOutput();


  vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();

  fitsReader->CalculateRMS();


  // isosurface
  vtkMarchingCubes *shellE = vtkMarchingCubes::New();
  shellE->SetInputData(fitsReader->GetOutput());
  shellE->ComputeNormalsOn();

  shellE->SetValue(0, 3 * fitsReader->GetRMS());

  shellE->Update();
  num_of_cells=shellE->GetOutput()->GetNumberOfCells();
  
  std::cout << "Cells number " << num_of_cells
            << std::endl;
            
            
  vtkPolyDataMapper *shellM = vtkPolyDataMapper::New();
  shellM->SetInputConnection(shellE->GetOutputPort());
  shellM->ScalarVisibilityOff();

  vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
  actor->SetMapper(shellM);

  renderer->AddActor(actor);

  vtkRenderWindow *renderWindow = vtkRenderWindow::New();
  renderWindow->AddRenderer(renderer);

  renderWindow->SetSize(screen_res, screen_res);

  vtkRenderWindowInteractor *renderWindowInteractor =
      vtkRenderWindowInteractor::New();
  renderWindowInteractor->SetRenderWindow(renderWindow);

  vtkSmartPointer<vtkInteractorStyleTrackballCamera> style =
      vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New(); // like
                                                                 // paraview

  renderWindowInteractor->SetInteractorStyle(style);

  vtkSmartPointer<vtkCallbackCommand> callback =
      vtkSmartPointer<vtkCallbackCommand>::New();

  callback->SetCallback(CallbackFunction);
  renderer->AddObserver(vtkCommand::EndEvent, callback);

  renderer->SetBackground(.3, .6, .3); // Background color green



  double bounds[6];
  shellE->GetOutput()->GetBounds(bounds);
  
  clock->StopTimer();
  time_before= clock->GetElapsedTime();
  std::cout << "Time up to Rendering: " << time_before << " sec" << std::endl;

  renderer->ResetCamera();
  auto cam = renderer->GetActiveCamera();
  double pos[3];

  double time = 0;
  int endCount = 120;
  std::cout << "Renderer class: " << renderer->GetClassName() << std::endl;
  
  
  
  for (int i = 0; i < endCount; i++) {

    double max[3] = {bounds[1] + vtkMath::Random(0, 10),
                     bounds[3] + vtkMath::Random(0, 10),
                     bounds[5] + vtkMath::Random(0, 10)};
    double min[3] = {bounds[0] + vtkMath::Random(0, 10),
                     bounds[2] + vtkMath::Random(0, 10),
                     bounds[4] + vtkMath::Random(0, 10)};

    renderer->ResetCamera(min[0], max[0], min[1], max[1], min[2], max[2]);
    renderWindow->Render();
    double sec = renderer->GetLastRenderTimeInSeconds();
    time += sec;
    if(i==0) {
    s_min=sec;
    s_max=sec;
    }
    s_min=std::min(sec,s_min);
    s_max=std::max(sec,s_max);
    std::cout << "seconds " << sec << std::endl;
  }
  fps_avarage=double(endCount) / time;
  std::cout << "Total FPS: " << fps_avarage << std::endl;
 

  myfile << num_of_cells<<","<<time_before <<","<< fps_avarage<<"\n"; //<<","<< s_min<<","<< s_max<<"\n";

  endCount=2;
  
  //If run in headless mode, check the screenshots
  vtkSmartPointer<vtkWindowToImageFilter> windowToImageFilter = 
    vtkSmartPointer<vtkWindowToImageFilter>::New();
  windowToImageFilter->SetInput(renderWindow);
  windowToImageFilter->SetInputBufferTypeToRGBA(); //also record the alpha (transparency) channel
  windowToImageFilter->ReadFrontBufferOff(); // read from the back buffer
  windowToImageFilter->Update();
  
  vtkSmartPointer<vtkPNGWriter> writer = 
    vtkSmartPointer<vtkPNGWriter>::New();
  
  writer->SetInputConnection(windowToImageFilter->GetOutputPort());
  
  for (int i = 0; i < endCount; i++) {
    double max[3] = {bounds[1] + vtkMath::Random(0, 10),
                     bounds[3] + vtkMath::Random(0, 10),
                     bounds[5] + vtkMath::Random(0, 10)};
    double min[3] = {bounds[0] + vtkMath::Random(0, 10),
                     bounds[2] + vtkMath::Random(0, 10),
                     bounds[4] + vtkMath::Random(0, 10)};

    renderer->ResetCamera(min[0], max[0], min[1], max[1], min[2], max[2]);
    renderWindow->Render();
    windowToImageFilter->Update();
    std::string name="screenshot"+std::to_string(i)+".png";
    writer->SetFileName(name.c_str() );
    writer->Write();
  }
  

  renderWindowInteractor->Start(); // this is if launched with windows
  
  
 
}


int main(int argc, char *argv[]) {

std::array<std::pair<std::string,float>,4> names={ {
std::pair<std::string,float>("vlkb-cutout_2021-02-18_12-33-05_516569_JCMT-HARP_COHRS_18p00_0p00_CUBE_REBIN_R1.fits", 55),
std::pair<std::string,float>("vlkb-merged_3D_2021-02-18_12-34-13_309675_16774-16806.fits",157.6),
std::pair<std::string,float>("vlkb-merged_3D_2021-03-08_10-39-11_837561_16774-16805.fits",535.7),
std::pair<std::string,float>("vlkb-merged_3D_2021-02-18_12-36-07_979531_16774-16806.fits",1100)
} }; 


      myfile.open ("report.csv");
      myfile << "Structured grid visualisation performance\n";
      myfile << "File name, File size, Output cells Number, Time for pipeline(seconds), Avarage FPS"<<std::endl; //, Min time (seconds), Max time (seconds)\n";


for (auto it=names.begin() ;it !=names.end(); ++it)
{
std::string filename="../../data/"+(*it).first;
myfile << (*it).first<<","<< (*it).second<<",";
test_structured(filename.c_str());
}

 myfile.close();
      return 0;

}

