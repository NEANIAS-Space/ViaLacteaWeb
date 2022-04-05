


# Create the main library
set(LIB_NAME vtkVialactea)
  

# Sources in the current directory (library sources only!)
set(LIB_SRCS
  vtkFitsReader.cxx 
  vtkFitsUnstructuredReader.cxx
  vtkLegendScaleActor.cxx

)


# Third party library dependencies

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/INSTALL/CFITSIO/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/INSTALL/include)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/INSTALL/CFITSIO/lib)


# Sources that are not vtkObjects
set(LIB_SPECIAL
    xml_procs.cpp
    tinyxml2.cpp
    astroutils.cpp
    luthelper.cpp
    color.cpp
    libwcs/fitsfile.c
    libwcs/imgetwcs.c
    libwcs/wcs.c
    libwcs/wcslib.c
    libwcs/platepos.c
     libwcs/hget.c  
     libwcs/fileutil.c  
     libwcs/fitswcs.c  
     libwcs/distort.c  
     libwcs/hput.c  
     libwcs/iget.c  
     libwcs/imio.c  
     libwcs/imhfile.c  
     libwcs/dateutil.c  
     libwcs/wcsinit.c  
     libwcs/dsspos.c  
     
     libwcs/wcstrig.c  
     libwcs/wcscon.c  
     libwcs/lin.c  
     
     libwcs/tnxpos.c  
     
     libwcs/cel.c  
     libwcs/proj.c  
     libwcs/sph.c  
     libwcs/worldpos.c  
    
    
   
)

# Headers without a matching .cxx file are listed here
set(LIB_HDRS
vtkFitsReader.h
vtkFitsUnstructuredReader.h
vtkLegendScaleActor.h
)


set_source_files_properties(${LIB_HDRS} ${LIB_SPECIAL}
  PROPERTIES WRAP_EXCLUDE ON)






# Create the library


  # When building as a module for VTK 8.90 or later
   set(LIB_SRC_HDRS)
   foreach(_src ${LIB_SRCS})
     get_filename_component(_base ${_src} NAME_WE)
     list(APPEND LIB_SRC_HDRS ${_base}.h)
   endforeach()


  vtk_module_add_module(VTK::VIALACTEA
     SOURCES ${LIB_SRCS} ${LIB_SPECIAL}
     HEADERS ${LIB_SRC_HDRS} ${LIB_HDRS})
   vtk_module_link(VTK::VIALACTEA
     PRIVATE ${cfitsio} -lcurl )# ${curl} )
     
 # Add our test executables.
vtk_module_add_executable(TimingTests
  NO_INSTALL
  main.cpp)
target_link_libraries(TimingTests
 PRIVATE 
    VTK::VIALACTEA 
    VTK::CommonDataModel 
    VTK::CommonCore
    VTK::RenderingCore
    VTK::InteractionStyle 
    VTK::RenderingCore 
    VTK::FiltersSources 
    VTK::CommonMisc
    VTK::CommonSystem
    VTK::RenderingOpenGL2
    ${cfitsio} -lcurl) 


 # Add our test executables.
vtk_module_add_executable(StandardTest
  DEVELOPMENT
  vtk_standard.cpp)
target_link_libraries(StandardTest
 PRIVATE 
     VTK::CommonCore
    VTK::RenderingCore
    VTK::InteractionStyle 
    VTK::FiltersSources 
   ) 


