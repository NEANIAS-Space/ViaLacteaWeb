/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: (token) => session.call('vtk.initialize', [token]),
    loadURL: () => session.call('vtk.cone.url', []),
    resetCamera: () => session.call('vtk.camera.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),
    updatePlanes: (planes) =>
      session.call('vtk.cone.planes.update', [planes]),
    updateContours: (contours) =>
      session.call('vtk.cone.contours.update', [contours]),
    
    updateFits: (url) =>
      session.call('vtk.cone.fits.update', [url]),
    updateCamView: (v) =>
      session.call('vtk.cone.camview.update', [v]),
    updateRotateAxis: (v) =>
      session.call('vtk.cone.rotate.update', [v]),
      
    loadXMLFITS: (res) =>
                 session.call('vtk.cone.urlfits', [res]),
                 
    getDataCubeData:() => session.call('vtk.cone.loadcubedata', []),
    
    setToken: (t) =>
      session.call('vtk.initialize.token', [t]),
      };
}
