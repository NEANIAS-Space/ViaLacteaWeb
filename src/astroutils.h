#ifndef ASTROUTILS_H
#define ASTROUTILS_H

#include <string>
#include "libwcs/wcs.h"

class AstroUtils
{
public:
    AstroUtils();
    //static bool sky2xy(std::string map,double ra, double dec,double* coord);
    static void xy2sky(std::string map, float x, float y, double *coord,  int wcs_type=WCS_ECLIPTIC);
  

private:
    static WorldCoor* GetWCSFITS (char *filename, int verbose);
    static char * GetFITShead (char * filename, int verbose);

};

#endif // ASTROUTILS_H
