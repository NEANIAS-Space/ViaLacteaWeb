/* eslint-disable arrow-body-style */
export default function createMethods(session) {
  return {
    createVisualization: () => session.call('vtk.initialize', []),
    loadURL: () => session.call('vtk.cone.url', []),
    resetCamera: () => session.call('vtk.camera.reset', []),
    updateResolution: (resolution) =>
      session.call('vtk.cone.resolution.update', [resolution]),

    loadXMLFITS: (res) =>
                 session.call('vtk.cone.urlfits', [res]),
      };
}
