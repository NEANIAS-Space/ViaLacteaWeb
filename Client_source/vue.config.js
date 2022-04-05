const vtkChainWebpack = require('vtk.js/Utilities/config/chainWebpack');
//const fs = require('fs');
const PATH = require('path');
const dirTree = require('directory-tree');
//const someFileContents = fs.readFileSync('/home/evgeniya/Documents/GitHub/files');

module.exports = {
  chainWebpack: (config) => {
    
     
    // Add project name as alias
    config.resolve.alias.set('vlw-base', __dirname);
    publicPath: process.env.PUBLIC_URL || "/",
    

    // Add vtk.js rules
    vtkChainWebpack(config);
  },
};
