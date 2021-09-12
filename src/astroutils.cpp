#include "astroutils.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <math.h>
#include "libwcs/wcs.h"
#include "libwcs/fitsfile.h"
#include "libwcs/wcscat.h"
#include "libwcs/lwcs.h"

#include <iostream>
#include <vector>
#include <string>




extern void setsys();

std::string trim(const std::string &s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && isspace(*it))
        it++;

    std::string::const_reverse_iterator rit = s.rbegin();
    while (rit.base() != it && isspace(*rit))
        rit++;

    return std::string(it, rit.base());
}


AstroUtils::AstroUtils()
{
}

void AstroUtils::xy2sky(std::string map, float x, float y, double* coord, int wcs_type)
{
    struct WorldCoor *wcs; //wcs
    char *fn = new char[map.length() + 1];
    static char coorsys[16];
    char wcstring[64];
    char lstr = 64;
    *coorsys = 0;

    strcpy(fn, map.c_str());
    wcs = GetWCSFITS(fn, 0);
    wcs->sysout = wcs_type;
    // force the set of wcs in degree
    setwcsdeg(wcs,1); //wcs

    if (wcs_type == WCS_GALACTIC)
    {
        wcs->eqout = 2000.0;
    }

    if (pix2wcst(wcs, x, y, wcstring, lstr))
    {
        std::string str(wcstring);
        std::vector<std::string> tokens;
        //TODO uncomment
        std::string s=trim(str); //remove spaces at beginning and end
        //split(tokens, str, is_any_of(" "), boost::token_compress_on); //gets all tokens splitted by space
        char delimiter = ' ';
        //std::cout<<str<<std::endl;
        //std::cout<<s<<std::endl;
        size_t pos = 0;
        std::string token;
        while ((pos = s.find(delimiter)) != std::string::npos) {
            std::string sub=s.substr(0, pos);
            if(sub!="") //check that empty string is not pushed
               tokens.push_back(sub);
            s.erase(0, pos + 1);
        }
        
        coord[0] = atof(tokens[0].c_str());
        coord[1] = atof(tokens[1].c_str());
        //std::cout<<coord[0]<<" , "<<coord[1]<<std::endl;
        
    }

    delete [] fn;
    wcsfree(wcs);
}

WorldCoor * AstroUtils::GetWCSFITS(char *filename, int verbose)
{
    char *header;		    /* FITS header */
    struct WorldCoor *wcs;	/* World coordinate system structure */
    char *cwcs;			    /* Multiple wcs string (name or character) */

    /* Read the FITS or IRAF image file header */
    header = GetFITShead (filename, verbose);
    if (header == NULL)
        return (NULL);

    verbose=true;

    /* Set the world coordinate system from the image header */
    cwcs = strchr (filename, '%');
    if (cwcs != NULL)
        cwcs++;
    wcs = wcsinitn (header, cwcs);
    if (wcs == NULL) {
        setwcsfile (filename);
        if (verbose)
            wcserr ();
    }
    free (header);

    return (wcs);
}

char * AstroUtils::GetFITShead(char * filename, int verbose)
{
    char *header;		/* FITS header */
    int lhead;			/* Maximum number of bytes in FITS header */
    char *irafheader;   /* IRAF image header */
    int nbiraf, nbfits;

    /* Open IRAF image if .imh extension is present */
    if (isiraf (filename)) {
        if ((irafheader = irafrhead (filename, &nbiraf)) != NULL) {
            if ((header = iraf2fits (filename, irafheader, nbiraf, &lhead)) == NULL) {
                if (verbose)
                    fprintf (stderr, "Cannot translate IRAF header %s\n",filename);
                free (irafheader);
                irafheader = NULL;
                return (NULL);
            }
            free (irafheader);
            irafheader = NULL;
        }
        else {
            if (verbose)
                fprintf (stderr, "Cannot read IRAF header file %s\n", filename);
            return (NULL);
        }
    }
    else if (istiff (filename) || isgif (filename) || isjpeg (filename)) {
        if ((header = fitsrtail (filename, &lhead, &nbfits)) == NULL) {
            if (verbose)
                fprintf (stderr, "TIFF file %s has no appended header\n", filename);
            return (NULL);
        }
    }

    /* Open FITS file if .imh extension is not present */
    else {
        if ((header = fitsrhead (filename, &lhead, &nbfits)) == NULL) {
            if (verbose)
                /* fprintf (stderr, "Cannot read FITS file %s\n", filename); */
                fitserr ();
            return (NULL);
        }
    }

    return (header);
}

