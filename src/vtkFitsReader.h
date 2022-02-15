// .NAME vtkFitsReader - read structured points from FITS file.
// .SECTION Description
// vtkFitsReader is a source object that reads FITS data files
// .SECTION Caveats
// Uses CFITSIO v2.0 (http://heasarc.gsfc.nasa.gov/docs/software/fitsio)

#ifndef __vtkFitsReader_h
#define __vtkFitsReader_h

#include "vtkAlgorithm.h"
#include "vtkFloatArray.h"
#include "vtkStructuredPoints.h"

extern "C" {
#include "fitsio.h"
}

//class VTK_EXPORT vtkFitsReader : public vtkStructuredPointsSource
class VTK_EXPORT vtkFitsReader : public vtkAlgorithm {
public:
    //    vtkFitsReader();
    //  static vtkFitsReader *New() {return new vtkFitsReader;}

    static vtkFitsReader* New();
    vtkFitsReader();
    ~vtkFitsReader();

    //For downloading and parcing files

    void SetSessionToken(std::string token)
    {
        m_token = token;
    }
    /* For log out*/
    bool LogOut();
    void SetRefreshToken(std::string t){m_refreshToken=t;};

 
    bool GenerateVLKBUrl(std::string data);
    bool DownloadSurveyDataCube(std::string urlString);

    bool DownloadFile(std::string url, std::string outName);
    bool DownloadFITSFromUrl(std::string url);
    void DownloadXMLFromUrl(std::string url);

    void SetFileName(std::string name);
    std::string GetFileName() { return filename; }
    std::string GetDataCubeData() { return m_dataCubeDesc; }

    vtkTypeMacro(vtkFitsReader, vtkAlgorithm);
    void PrintSelf(ostream& os, vtkIndent indent);
    void PrintHeader(ostream& os, vtkIndent indent);
    void PrintTrailer(std::ostream& os, vtkIndent indent);
    double getInitSlice() { return initSlice; }

    bool is3D;
    void Set3D(bool s){is3D=s;};
    void CalculateRMS();
    void SetTempPath(std::string path)
    {
        m_tempPath = path + "/";
        std::cout << "Temporary path " << m_tempPath << std::endl;
        m_fileToDownload = m_tempPath + m_fileToDownload;
        m_fitsFile = m_tempPath + m_fitsFile;
        m_fitsFile_temp = m_tempPath + m_fitsFile_temp;
    }

    double GetSigma() { return sigma; }
    double GetRMS() { return rms; }
    double GetMedia() { return media; }
    long GetEntries() { return npix; }
    double* GetRangeSlice(int i);
    double GetRangeSliceMin(int i) { return minmaxslice[i][0]; };
    double GetRangeSliceMax(int i) { return minmaxslice[i][1]; };

    float GetMin() { return datamin; }
    float GetMax() { return datamax; }

    float GetCrval(int i)
    {
        if (i < 3)
            return crval[i];
        else
            return -1;
    }
    float GetCpix(int i)
    {
        if (i < 3)
            return cpix[i];
        else
            return -1;
    }
    float GetCdelt(int i)
    {
        if (i < 3)
            return cdelt[i];
        else
            return -1;
    }

    int GetNaxes(int i);

    vtkFloatArray* fitsScalars;

    // Description:
    // Get the output data object for a port on this algorithm.
    vtkStructuredPoints* GetOutput();
    vtkStructuredPoints* GetOutput(int);
    virtual void SetOutput(vtkDataObject* d);
    // Description:
    // see vtkAlgorithm for details
    virtual int ProcessRequest(vtkInformation*,
        vtkInformationVector**,
        vtkInformationVector*);

    std::string getSpecies() { return species; };
    std::string getTransition() { return transition; };
    std::string getSurvey() { return survey; };

    std::string GetSurveysData() { return surveyData; };

    void setSpecies(std::string s) { species = s; };
    void setTransition(std::string s) { transition = s; };
    void setSurvey(std::string s) { survey = s; };

protected:
    std::string survey;
    std::string species;
    std::string transition;
    std::string cut;

    std::string m_dataCubeDesc;

    float datamin;
    float datamax;
    float epoch; // Part of FITS Header file
    int* dimensions; // [x,y,z]
    int naxis;
    int points;
    double crval[3];
    double cpix[3];
    double cdelt[3];
    double sigma = 0;
    double media = 0;
    double rms = 0;
    long npix = 0;
    long naxes[3];

    double** minmaxslice;

    // Description:
    // This is called by the superclass.
    // This is the method you should override.
    virtual int RequestDataObject(
        vtkInformation* request,
        vtkInformationVector** inputVector,
        vtkInformationVector* outputVector);

    // convenience method
    virtual int RequestInformation(
        vtkInformation* request,
        vtkInformationVector** inputVector,
        vtkInformationVector* outputVector);

    // Description:
    // This is called by the superclass.
    // This is the method you should override.
    virtual int RequestData(
        vtkInformation* request,
        vtkInformationVector** inputVector,
        vtkInformationVector* outputVector);

    // Description:
    // This is called by the superclass.
    // This is the method you should override.
    virtual int RequestUpdateExtent(
        vtkInformation*,
        vtkInformationVector**,
        vtkInformationVector*);

    virtual int FillOutputPortInformation(int port, vtkInformation* info);

private:

    std::string filename;
    char title[80];
    char xStr[80];
    char yStr[80];
    char zStr[80];
    //    char cunit3[1][200];

    std::string m_token;
    std::string m_refreshToken;
    void ReadHeader();
    void printerror(int status); // from fitsio distribution
    double initSlice;
    std::string m_fileToDownload;
    std::string m_tempPath;
    std::string m_fitsFile;
    std::string m_fitsFile_temp;

    static size_t write_data(void* ptr, size_t size, size_t nmemb, FILE* stream);

    std::string surveyData;
    std::string CleanString(const char* species)
    {
        std::string str_sp = std::string(species);
        std::string::iterator end_pos = std::remove(str_sp.begin(), str_sp.end(), ' ');
        str_sp.erase(end_pos, str_sp.end());
        return str_sp;
    }
};

#endif
