#include "vtkFitsReader.h"

#include "vtkCommand.h"
#include "vtkInformation.h"
#include "vtkInformationVector.h"
#include "vtkObjectFactory.h"
#include "vtkStreamingDemandDrivenPipeline.h"
#include "vtkFloatArray.h"
#include <cmath>
#include "vtkPointData.h"
#include <iostream>     // std::cout
#include <sstream>
#include <algorithm>
#include "tinyxml2.h"
#include <curl/curl.h>

template <typename T>
T clamp(const T& n, const T& lower, const T& upper) {
  return std::max(lower, std::min(n, upper));
}


//vtkCxxRevisionMacro(vtkFitsReader, "$Revision: 1.1 $");
vtkStandardNewMacro(vtkFitsReader);

//----------------------------------------------------------------------------
vtkFitsReader::vtkFitsReader()
{
    this->filename[0]='\0';
    this->xStr[0]='\0';
    this->yStr[0]='\0';
    this->zStr[0]='\0';
    this->title[0]='\0';
    this->SetNumberOfInputPorts( 0 );
    this->SetNumberOfOutputPorts( 1 );
    //this->is3D=is3D;

    for (int i=0; i<3; i++)
    {
        crval[i]=0;
        cpix[i]=0;
        cdelt[i]=0;
        naxes[i]= 10;
    }
    
    this->is3D=false;
    m_fileToDownload="xml_to_parse.xml";
    m_fitsFile="temp.fits";
    m_tempPath="./";
    
    surveyData="";
    
    //m_fileToDownload=m_tempPath+m_fileToDownload;


}
void vtkFitsReader::DownloadSurveyDataCube(std::string str_u)
{
    
        DownloadXMLFromUrl(str_u.c_str());
        
        tinyxml2::XMLDocument doc2(true,tinyxml2::COLLAPSE_WHITESPACE);
        doc2.LoadFile( m_fileToDownload.c_str());
        const char* url2 = doc2.FirstChildElement( "results" )->FirstChildElement( "URL" )->GetText();
        
        //For some reason had to remove whitespace manually
        std::string str=std::string(url2);
        std::string::iterator end_pos = std::remove(str.begin(), str.end(), ' ');
        str.erase(end_pos, str.end());
        
        //fill datacube info data
        
        survey=doc2.FirstChildElement( "results" )->FirstChildElement( "input" )->FirstChildElement( "SurveyName" )->GetText();
        species=doc2.FirstChildElement( "results" )->FirstChildElement( "input" )->FirstChildElement( "Species" )->GetText();
        transition=doc2.FirstChildElement( "results" )->FirstChildElement( "input" )->FirstChildElement( "Transition" )->GetText();
        cut = doc2.FirstChildElement( "results" )->FirstChildElement( "CUT" )->GetText();       
       // <SurveyName>HOPS</SurveyName>
       // <Species>H2O</Species>
       // <Transition>6-1-6_5-2-3</Transition>
        //<CUT> HOPS/G357.3-003.9-H2O-cube.fits[457:481 51:75 1:2337] </CUT>
        
        m_dataCubeDesc="";
        m_dataCubeDesc+=survey;
        m_dataCubeDesc+=" \n";
        m_dataCubeDesc+=species;
        m_dataCubeDesc+=" \n";
        m_dataCubeDesc+=transition;
        m_dataCubeDesc+=" \n";
        m_dataCubeDesc+=cut;
        
        std::cout<<str.c_str()<<std::endl;
        
        DownloadFITSFromUrl(str);
}
//----------------------------------------------------------------------------
bool vtkFitsReader::GenerateVLKBUrl(std::string data) //point,std::string radius)
{
    std::vector<std::string> strings;
        std::istringstream fpoint(data);
        std::string s;
        float p[2];
        getline(fpoint, s, ',');
        p[0]=::atof(s.c_str()); //l_lineEdit
        p[0]=clamp<float>(p[0],-180.0,180.0);
        getline(fpoint, s, ',');
        p[1]=::atof(s.c_str()); //b_lineEdit
        p[1]=clamp<float>(p[1],-3.0,3.0);

           // ui->glatLineEdit->setText(QString::number( pieces[1].toDouble(), 'f', 4 ));
           // ui->glonLineEdit->setText(QString::number( pieces[0].toDouble(), 'f', 4 ));

        
        float r,dl,db;
        getline(fpoint, s, ',');
        r=::atof(s.c_str()); //dlLineEdit
        getline(fpoint, s, ',');
        dl=::atof(s.c_str()); //dbLineEdit
        getline(fpoint, s, ',');
        db=::atof(s.c_str()); //dbLineEdit
        //bool isRadius=false;
        r=clamp<float>(r,0.0,2.0);
        dl=clamp<float>(dl,0.0,2.0);
        db=clamp<float>(db,0.0,2.0);
        
        //r[1]=clamp<float>(r[1],0.0,4.0);


       //http://ia2-vialactea.oats.inaf.it:8080/libjnifitsdb-1.0.2p/vlkb_search?l=10&b=0&r=0.1 

        std::string vlkbUrl="http://ia2-vialactea.oats.inaf.it:8080/libjnifitsdb-1.0.2p/"; //I guess it should be different, with some fille added to it
        std::string urlString=vlkbUrl+"/vlkb_search?l="+std::to_string(p[0])+"&b="+std::to_string(p[1]);//+"&species="+species;
           /* if(isRadius)
            {
                //urlString+="&r="+ui->r_lineEdit->text();
            }
            else
                urlString+="&dl="+std::to_string(r[0])+"&db="+std::to_string(r[1]);

            urlString+="&vl=-500000&vu=500000";
*/
         if (r!=0.0) {
             urlString+="&r="+std::to_string(r);
         } else{
             urlString+="&dl="+std::to_string(dl);
             urlString+="&db="+std::to_string(db);
         }
        
        DownloadXMLFromUrl(urlString);
            std::cout<<"URL "<<urlString<<std::endl;
            
            //Start parsing xml from temp file m_fileToDownload
            tinyxml2::XMLDocument doc(true,tinyxml2::COLLAPSE_WHITESPACE);
           
            std::cout<<"we download "<<m_fileToDownload<<std::endl;
            tinyxml2::XMLError eResult = doc.LoadFile(m_fileToDownload.c_str());
            
            if (eResult != tinyxml2::XML_SUCCESS) 
                std::cout<<"XML not found"<<std::endl;
            else
                std::cout<<"XML downloaded"<<std::endl;
            //const char* species = doc.FirstChildElement( "results" )->FirstChildElement( "survey" )->FirstChildElement("Species")->GetText();;
            //const char* overlap = doc.FirstChildElement( "results" )->FirstChildElement( "survey" )->FirstChildElement("datacube")->FirstChildElement("overlap")->FirstChildElement("code")->GetText();;
            tinyxml2::XMLElement* pElement{ doc.FirstChildElement( "results" ) ->FirstChildElement( "survey" )};
             
             bool found=false;
             while (!found)
             {
                 const char* species =pElement->FirstChildElement("Species")->GetText();
                 std::string str_sp=std::string(species);
                        std::string::iterator end_pos = std::remove(str_sp.begin(), str_sp.end(), ' ');
                        str_sp.erase(end_pos, str_sp.end());
                 const char* overlap = pElement->FirstChildElement("datacube")->FirstChildElement("overlap")->FirstChildElement("code")->GetText();
             std::cout<<"species "<<species<<std::endl;
                  std::cout<<"overlap "<<overlap<<std::endl;
                  
                  int ov= ::atoi(overlap);
                  
                  
                  
                if(str_sp!="Continuum") //&&(ov==3))
                {
            	found=true;
            	std::cout<<"Proceed with downloading file"<<std::endl;
            	}
            	else
            	    pElement = pElement->NextSiblingElement();
            	
            	if (pElement == nullptr || NULL) {
            	    std::cout<<"No dataCube the old data would be kept"<<std::endl;
            	    	
            	    return false;
            	    }
            	}
            	
            	//if(!found) return;
            	
            const char* url = pElement->FirstChildElement("datacube")->FirstChildElement("Access")->FirstChildElement("URL")->GetText();;
            
            //Cleaning url
            
            std::string str_u=std::string(url);
            ///std::string::iterator end_pos_u = std::remove(str_u.begin(), str_u.end(), ' ');
            //str_u.erase(end_pos_u, str_u.end());
            //std::replace(str_u.begin(), str_u.end()," ","%20");
            //str_u.replace(s.find("$name"), sizeof("$name") - 1, "Somename");
            auto ps=str_u.find(" ");
            while(ps!=std::string::npos){
            str_u.replace(ps, 1, "%20");
            ps=str_u.find(" ");
        }
            ps=str_u.find("+");
                while(ps!=std::string::npos){
                str_u.replace(ps, 1, "%2B");
                ps=str_u.find("+");
            }
            
            
            std::cout<<str_u.c_str()<<std::endl;
            
        DownloadSurveyDataCube(str_u);
        
        
        
        //Proceed with forming the survey string
        //surveyData="";
        /*{
            "survey": 4,
            "overlap": "Sydney",
            "url": "lc",
            
          },
          {
            "survey": 4,
                      "overlap": "Sydney",
                      "url": "lc",
          }
        ]
        */
        surveyData="[\n";
        
        tinyxml2::XMLElement* element{ doc.FirstChildElement( "results" ) ->FirstChildElement( "survey" )};
        	while (element != nullptr || NULL)
        	    {
        const char* species =element->FirstChildElement("Species")->GetText();
             
               
                  
               
                //std::cout<<"overlap "<<overlap<<std::endl;
                     
                std::string str_sp=CleanString(species);
                std::string str2 ("Continuum");
                     
                     // different member versions of find in the same order as above:
                     std::size_t found = str_sp.find(str2);
                    
                     
                     
                     
                   if (found==std::string::npos) // if(str_sp!="Continuum") //&&(ov==3))
                   {
                       std::cout<<"species "<<species<<std::endl;
                       if(surveyData=="[\n") //first one
                       surveyData+="{\n";
                       else
                           surveyData+=",\n{\n";
                       
                       surveyData+="\"survey\":";
                       //fill surveyData
                       //Species
                       //overlap description
                       //overlap code
                       //access URL type="cutout"
                       const char* survey =element->FirstChildElement("Survey")->GetText();
                       str_sp+=" "+std::string(survey);
                       surveyData=surveyData+"\""+str_sp+"\"";
                       surveyData+=",\n";
                       const char* transition = element->FirstChildElement("Transition")->GetText();
                       
                       tinyxml2::XMLElement * datacube  = element->FirstChildElement("datacube");
                       
                     //  while (datacube != nullptr || NULL) {
                       //check several datacubes  mosaic type
                       const char* overlap_desc = datacube->FirstChildElement("overlap")->FirstChildElement("description")->GetText();
                       std::string str_desc=std::string(transition);
                       if(std::string(overlap_desc)=="The datacube Region is completely inside the input Region.")
                           str_desc+=" Full Overlap";
                           else
                           str_desc+=" Partial Overlap";
                       surveyData+="\"overlap\":";
                       surveyData=surveyData+"\""+str_desc+"\"";
                       surveyData+=",\n";
                       
                       std::string url_cutout="";
                       tinyxml2::XMLElement * node  = datacube->FirstChildElement("Access")->FirstChildElement("URL");
                       if (node->Attribute("type", "cutout"))
                       {
                                          //get url for xml
                           url_cutout=std::string(node->GetText());
                           auto ps=url_cutout.find(" ");
                                      while(ps!=std::string::npos){
                                      url_cutout.replace(ps, 1, "%20");
                                      ps=url_cutout.find(" ");
                                  }
                                      ps=url_cutout.find("+");
                                          while(ps!=std::string::npos){
                                          url_cutout.replace(ps, 1, "%2B");
                                          ps=url_cutout.find("+");
                                      }
                       }
                       //form the survey json
                       surveyData+="\"url\": ";
                       surveyData=surveyData+"\""+url_cutout+"\"";
                       surveyData+="\n }";
                       
                      // datacube = datacube->NextSiblingElement();
                      // }
                       // std::cout<<surveyData<<std::endl;
                       std::cout<<"filled data for "<<species<<std::endl;
                   }
                      element = element->NextSiblingElement();
                       	
                       
                   }
                   surveyData+="]";
                   //std::cout<<surveyData<<std::endl;
        
    return true;
}
void vtkFitsReader::DownloadXMLFromUrl(std::string url)
{
    
    DownloadFile(url,m_fileToDownload);
    //TODO: parseXML here


}

void vtkFitsReader::DownloadFITSFromUrl(std::string url)
{
   
    DownloadFile(url,m_fitsFile);
    SetFileName(m_fitsFile);


}
//----------------------------------------------------------------------------
size_t  vtkFitsReader::write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written = fwrite(ptr, size, nmemb, stream);
    return written;
}
//----------------------------------------------------------------------------
void vtkFitsReader::DownloadFile(std::string url,std::string outName)
{
CURL *curl;
    FILE *fp;
    CURLcode res;
    curl = curl_easy_init();
    if (curl) {
        fp = fopen(outName.c_str(),"wb");
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
        res = curl_easy_perform(curl);
        /* always cleanup */
        curl_easy_cleanup(curl);
        fclose(fp);
    }
}

//----------------------------------------------------------------------------
vtkFitsReader::~vtkFitsReader()
{
}

void vtkFitsReader::SetFileName(std::string name) {


    if (name.empty()) {
        vtkErrorMacro(<<"Null Datafile!");
        return;
    }


    filename= name;
    this->Modified();


}
//----------------------------------------------------------------------------
void vtkFitsReader::PrintSelf(ostream& os, vtkIndent indent)
{
    // this->Superclass::PrintSelf(os, indent);
}

void vtkFitsReader::PrintHeader(ostream& os, vtkIndent indent)
{
    // this->Superclass::PrintHeader(os, indent);

}

void vtkFitsReader::PrintTrailer(std::ostream& os , vtkIndent indent)
{
    // this->Superclass::PrintTrailer(os, indent);
}

//----------------------------------------------------------------------------
vtkStructuredPoints* vtkFitsReader::GetOutput()
{
    return this->GetOutput(0);
}

//----------------------------------------------------------------------------
vtkStructuredPoints* vtkFitsReader::GetOutput(int port)
{
    return vtkStructuredPoints::SafeDownCast(this->GetOutputDataObject(port));
}

//----------------------------------------------------------------------------
void vtkFitsReader::SetOutput(vtkDataObject* d)
{
    this->GetExecutive()->SetOutputData(0, d);
}


//----------------------------------------------------------------------------
int vtkFitsReader::ProcessRequest(vtkInformation* request,
                                  vtkInformationVector** inputVector,
                                  vtkInformationVector* outputVector)
{
    // Create an output object of the correct type.
    if(request->Has(vtkDemandDrivenPipeline::REQUEST_DATA_OBJECT()))
    {
        return this->RequestDataObject(request, inputVector, outputVector);
    }
    // generate the data
    if(request->Has(vtkDemandDrivenPipeline::REQUEST_DATA()))
    {
        return this->RequestData(request, inputVector, outputVector);
    }

    if(request->Has(vtkStreamingDemandDrivenPipeline::REQUEST_UPDATE_EXTENT()))
    {
        return this->RequestUpdateExtent(request, inputVector, outputVector);
    }

    // execute information
    if(request->Has(vtkDemandDrivenPipeline::REQUEST_INFORMATION()))
    {
        return this->RequestInformation(request, inputVector, outputVector);
    }

    return this->Superclass::ProcessRequest(request, inputVector, outputVector);
}

//----------------------------------------------------------------------------
int vtkFitsReader::FillOutputPortInformation(
        int vtkNotUsed(port), vtkInformation* info)
{
    // now add our info
    info->Set(vtkDataObject::DATA_TYPE_NAME(), "vtkStructuredPoints");
    return 1;
}


//----------------------------------------------------------------------------
int vtkFitsReader::RequestDataObject(
        vtkInformation* vtkNotUsed(request),
        vtkInformationVector** vtkNotUsed(inputVector),
        vtkInformationVector* outputVector )
{
//Preparation step


    for ( int i = 0; i < this->GetNumberOfOutputPorts(); ++i )
    {
        

        fitsfile *fptr;
        int status = 0, nfound = 0, anynull = 0;
        long  fpixel, nbuffer, npixels, ii;
        const int buffsize = 1000;

        float nullval, buffer[buffsize];
        vtkFloatArray *scalars = vtkFloatArray::New();

         vtkInformation* outInfo = outputVector->GetInformationObject( i );
        vtkStructuredPoints* output = vtkStructuredPoints::SafeDownCast(
                    outInfo->Get( vtkDataObject::DATA_OBJECT() ) );
        if ( ! output )
        {
            output = vtkStructuredPoints::New();
            outInfo->Set( vtkDataObject::DATA_OBJECT(), output );
            output->FastDelete();

            //FITS READER CORE

            char *fn=new char[filename.length() + 1];;
            strcpy(fn, filename.c_str());

            if ( fits_open_file(&fptr, fn, READONLY, &status) )
                printerror( status );

            delete []fn;


            if(! (this->is3D) )
            {
                 ReadHeader(); //for 3d was read in separate line


                /* read the NAXIS1 and NAXIS2 keyword to get image size */
                // if ( fits_read_keys_lng(fptr, "NAXIS", 1, 3, naxes, &nfound, &status) )
                if ( fits_read_keys_lng(fptr, "NAXIS", 1, 2, naxes, &nfound, &status) )
                    printerror( status );

                npixels  = naxes[0] * naxes[1]; /* num of pixels in the image */
                fpixel   = 1;
                nullval  = 0;                /* don't check for null values in the image */
                datamin  = 1.0E30;
                datamax  = -1.0E30;

                output->SetDimensions(naxes[0], naxes[1],1);

                // output->SetOrigin(0.0, 0.0, 0.0);
                output->SetOrigin(1.0, 1.0, 0.0);

                scalars->Allocate(npixels);

                while (npixels > 0) {

                    nbuffer = npixels;
                    if (npixels > buffsize)
                        nbuffer = buffsize;

                    if ( fits_read_img(fptr, TFLOAT, fpixel, nbuffer, &nullval,
                                       buffer, &anynull, &status) )
                        printerror( status );

                    for (ii = 0; ii < nbuffer; ii++)
                    {

                        // if (isnanf(buffer[ii])) buffer[ii] = -1000000.0; // hack for now
                        if (std::isnan(buffer[ii])) buffer[ii] = -1000000.0; // hack for now

                        scalars->InsertNextValue(buffer[ii]);


                        if ( buffer[ii] < datamin  &&  buffer[ii]!=-1000000.0)
                            datamin = buffer[ii];
                        if ( buffer[ii] > datamax  &&  buffer[ii]!=-1000000.0 )
                            datamax = buffer[ii];
                    }

                    npixels -= nbuffer;    /* increment remaining number of pixels */
                    fpixel  += nbuffer;    /* next pixel to be read in image */
                }
            }
            else
            {
                //should be already done
                this->CalculateRMS();



            }
            
        }


        // cerr << "min: " << datamin << " max: " << datamax << endl;

        if ( fits_close_file(fptr, &status) )
            printerror( status );

        output->GetPointData()->SetScalars(scalars);

        //END FITS READ CORE
        this->GetOutputPortInformation( i )->Set(vtkDataObject::DATA_EXTENT_TYPE(), output->GetExtentType() );


    }

    return 1;
}

//----------------------------------------------------------------------------
int vtkFitsReader::RequestInformation(
        vtkInformation* vtkNotUsed(request),
        vtkInformationVector** vtkNotUsed(inputVector),
        vtkInformationVector* vtkNotUsed(outputVector))
{
    // do nothing let subclasses handle it
    return 1;
}

//----------------------------------------------------------------------------
int vtkFitsReader::RequestUpdateExtent(
        vtkInformation* vtkNotUsed(request),
        vtkInformationVector** inputVector,
        vtkInformationVector* vtkNotUsed(outputVector))
{
    //qDebug()<<" \t \t **RequestUpdateExtent.vtkFitsReader";
    int numInputPorts = this->GetNumberOfInputPorts();
    for (int i=0; i<numInputPorts; i++)
    {
        int numInputConnections = this->GetNumberOfInputConnections(i);
        for (int j=0; j<numInputConnections; j++)
        {
            vtkInformation* inputInfo = inputVector[i]->GetInformationObject(j);
            inputInfo->Set(vtkStreamingDemandDrivenPipeline::EXACT_EXTENT(), 1);
        }
    }
    return 1;
}

//----------------------------------------------------------------------------
// This is the superclasses style of Execute method.  Convert it into
// an imaging style Execute method.
int vtkFitsReader::RequestData(
        vtkInformation* vtkNotUsed(request),
        vtkInformationVector** vtkNotUsed( inputVector ),
        vtkInformationVector* vtkNotUsed(outputVector) )
{
   // qDebug()<<"\t\t *** RequestData.vtkFitsReader";

    // do nothing let subclasses handle it
    return 1;
}

void vtkFitsReader::ReadHeader() {



    fitsfile *fptr;       /* pointer to the FITS file, defined in fitsio.h */

    int status, nkeys, keypos, hdutype, ii, jj;
    char card[FLEN_CARD];   /* standard string lengths defined in fitsioc.h */
    
    
    char crval1[80];
    char crval2[80];
    char crval3[80];
    char crpix1[80];
    char crpix2[80];
    char crpix3[80];
    char cdelt1[80];
    char cdelt2[80];
    char cdelt3[80];
    char naxis1[80];
    char naxis2[80];
    char naxis3[80];
    
    
    crval1[0] ='\0';
    crval2[0] ='\0';
    crval3[0] ='\0';
    crpix1[0] ='\0';
    crpix2[0] ='\0';
    crpix3[0] ='\0';
    cdelt1[0] ='\0';
    cdelt2[0] ='\0';
    cdelt3[0] ='\0';
    
    std::string val1, val2, val3, pix1,pix2, pix3, delt1, delt2, delt3, nax1, nax2, nax3;

    status = 0;


    char *fn=new char[filename.length() + 1];;
    strcpy(fn, filename.c_str());

    if ( fits_open_file(&fptr, fn, READONLY, &status) )
        printerror( status );
    delete []fn;

    /* attempt to move to next HDU, until we get an EOF error */
    for (ii = 1; !(fits_movabs_hdu(fptr, ii, &hdutype, &status) ); ii++)
    {

        /* get no. of keywords */
        if (fits_get_hdrpos(fptr, &nkeys, &keypos, &status) )
            printerror( status );

        for (jj = 1; jj <= nkeys; jj++)  {

            if ( fits_read_record(fptr, jj, card, &status) )
                printerror( status );

            if (!strncmp(card, "CTYPE", 5)) {
                // cerr << card << endl;
                char *first = strchr(card, '\'');
                char *last = strrchr(card, '\'');

                *last = '\0';
                if (card[5] == '1')
                    strcpy(xStr, first+1);
                if (card[5] == '2')
                    strcpy(yStr, first+1);
                if (card[5] == '3')
                    strcpy(zStr, first+1);

                        }

            if (!strncmp(card, "OBJECT", 6)) {
                cerr << card << endl;
                char *first = strchr(card, '\'');
                char *last = strrchr(card, '\'');
                *last = '\0';
                strcpy(title, first+1);
            }

            if (!strncmp(card, "CRVAL", 5)) {
                char *first = strchr(card, '=');
                char *last = strrchr(card, '=');
                *last = '\0';

                // char *last = strrchr(card, '/');
                //*last = '\0';

                if (card[5] == '1')
                {
                    strcpy(crval1, first+1);
                    char *pch = strtok (crval1," ,");
                    strcpy(crval1, pch);
                    
                }
                
                if (card[5] == '2')
                {
                    strcpy(crval2, first+1);
                    char *pch = strtok (crval2," ,");
                    strcpy(crval2, pch);

                }
                
                if (card[5] == '3')
                {
                    strcpy(crval3, first+1);
                    char *pch = strtok (crval3," ,");
                    strcpy(crval3, pch);

                }
            }

            if (!strncmp(card, "CRPIX", 5)) {
                char *first = strchr(card, '=');
                char *last = strrchr(card, '=');
                *last = '\0';
                
                
                if (card[5] == '1')
                {
                    strcpy(crpix1, first+1);

                    char *pch = strtok (crpix1," ,");
                    strcpy(crpix1, pch);
                }
                
                if (card[5] == '2')
                {
                    strcpy(crpix2, first+1);

                    char *pch = strtok (crpix2," ,");
                    strcpy(crpix2, pch);
                }
                if (card[5] == '3')
                {
                    strcpy(crpix3, first+1);

                    char *pch = strtok (crpix3," ,");
                    strcpy(crpix3, pch);
                }
            }

            if (!strncmp(card, "CDELT", 5)) {
                char *first = strchr(card, '=');
                char *last = strrchr(card, '=');
                *last = '\0';
                
                if (card[5] == '1')
                {
                    strcpy(cdelt1, first+1);
                    char *pch = strtok (cdelt1," ,");
                    strcpy(cdelt1, pch);
                    
                }
                
                if (card[5] == '2')
                {
                    strcpy(cdelt2, first+1);
                    char *pch = strtok (cdelt2," ,");
                    strcpy(cdelt2, pch);
                }
                
                if (card[5] == '3')
                {
                    strcpy(cdelt3, first+1);
                    char *pch = strtok (cdelt3," ,");
                    strcpy(cdelt3, pch);
                }
            }
            
            

        }
    }


    val1=crval1;
    val2=crval2;
    val3=crval3;
    pix1=crpix1;
    pix2=crpix2;
    pix3=crpix3;
    delt1=cdelt1;
    delt2=cdelt2;
    delt3=cdelt3;


    
    crval[0]=::atof(val1.c_str());//val1.toDouble(); //problema
    crval[1]=::atof(val2.c_str());//val2.toDouble();
    crval[2]=::atof(val3.c_str());//val3.toDouble();
    cpix[0]=::atof(pix1.c_str());//pix1.toDouble();
    cpix[1]=::atof(pix2.c_str());//pix2.toDouble();
    cpix[2]=::atof(pix3.c_str());//pix3.toDouble();
    cdelt[0]=::atof(delt1.c_str());//delt1.toDouble();
    cdelt[1]=::atof(delt1.c_str());//delt2.toDouble();
    cdelt[2]=::atof(delt1.c_str());//delt3.toDouble();

    initSlice=crval[2]-(cdelt[2]*(cpix[2]-1));
    
    

    

    
}

// Note: from cookbook.c in fitsio distribution.
void vtkFitsReader::printerror(int status) {

    cerr << "vtkFitsReader ERROR.";
    if (status) {
        fits_report_error(stderr, status); /* print error report */
        exit( status );    /* terminate the program, returning error status */
    }
    return;
}


// Note: This function adapted from readimage() from cookbook.c in
// fitsio distribution.
void vtkFitsReader::CalculateRMS() {
    

    ReadHeader();
    
    vtkStructuredPoints *output = (vtkStructuredPoints *) this->GetOutput();
    fitsfile *fptr;
    int status = 0, nfound = 0, anynull = 0;
    long fpixel, nbuffer, npixels, ii, n=0;
    double meansquare=0;
    const int buffsize = 1000;
    
    
    float nullval, buffer[buffsize];
    char *fn=new char[filename.length() + 1];
    strcpy(fn, filename.c_str());
    
    if ( fits_open_file(&fptr, fn, READONLY, &status) )
        printerror( status );
    
    delete []fn;
    vtkFloatArray *scalars = vtkFloatArray::New();
    if ( fits_read_keys_lng(fptr, "NAXIS", 1, 3, naxes, &nfound, &status) )
        printerror( status );
    
    npixels  = naxes[0] * naxes[1] * naxes[2];
    n=npixels;
    
    fpixel   = 1;
    nullval  = 0;
    datamin  = 1.0E30;
    datamax  = -1.0E30;
    /*
    cerr << "\nvtkFitsReader: calculating the RMS" << this->filename << endl;
    cerr << "Dim: " << naxes[0] << " " << naxes[1] << " " << naxes[2] << endl;
    cerr << "points: " << npixels << endl;
    cerr << "creating vtk structured points dataset" << endl;
   */
    output->SetDimensions(naxes[0], naxes[1], naxes[2]);
    output->SetOrigin(0.0, 0.0, 0.0);
    
    scalars->Allocate(npixels);
    int bad=0;
    int slice;
    int num=0;



    minmaxslice=new double*[naxes[2]];
    for(int i=0;i< naxes[2];i++)
    {

        minmaxslice[i] = new double[2];

        minmaxslice[i][0]= 1.0E30;
        minmaxslice[i][1]= -1.0E30;

    }

    //For every pixel
    while (npixels > 0) {




        nbuffer = npixels;
        if (npixels > buffsize)
            nbuffer = buffsize;
        
        if ( fits_read_img(fptr, TFLOAT, fpixel, nbuffer, &nullval,
                           buffer, &anynull, &status) )
            printerror( status );


        for (ii = 0; ii < nbuffer; ii++)  {
            // slice= (num/(naxes[0]*naxes[1]))%(naxes[0]*naxes[1]);
            slice= (num/ (naxes[0]*naxes[1]) );
            num++;

            // qDebug()<<"npixel: "<<num <<" è sulla slice "<< slice <<" x: "<<naxes[0]<<" y: "<<naxes[1]<<" z: "<<naxes[2];

            if (std::isnan(buffer[ii]))
                buffer[ii] = -1000000.0;
            scalars->InsertNextValue(buffer[ii]);

            if ( buffer[ii]!=-1000000.0)
            {
                if ( buffer[ii] < datamin )
                    datamin = buffer[ii];
                if ( buffer[ii] > datamax   )
                    datamax = buffer[ii];

                //qDebug()<<"poreeeee "<<slice;
                if ( buffer[ii] < minmaxslice[slice][0] )
                    minmaxslice[slice][0] = buffer[ii];
                if ( buffer[ii] > minmaxslice[slice][1]   )
                    minmaxslice[slice][1] = buffer[ii];

                //meansquare+=buffer[ii]*buffer[ii];
                //  media+=buffer[ii];
                meansquare+=buffer[ii]*buffer[ii];

            }
            else
                bad++;
        }
        
        npixels -= nbuffer;
        fpixel  += nbuffer;
    }
    /*
    media=media/n;
    float diff;
    for(ii=0; ii<n; ii++)
    {
        if (scalars->GetValue(ii)!=-1000000.0)
        {
            meansquare+=scalars->GetValue(ii)*scalars->GetValue(ii);
            diff=scalars->GetValue(ii)-media;
            sigma+=qPow(diff, 2);
        }
        else
            bad++;
    }

*/
    n=n-bad;
    double means=meansquare/n;
    rms=sqrt(means);
    // sigma=qSqrt(sigma/n);

    if ( fits_close_file(fptr, &status) )
        printerror( status );
    
    output->GetPointData()->SetScalars(scalars);
    std::cout<<minmaxslice[0][0] <<minmaxslice[0][1]<<std::endl;
    return;
}
int vtkFitsReader::GetNaxes(int i)
{

    return naxes[i];

}
double* vtkFitsReader::GetRangeSlice(int i)
{

    return minmaxslice[i];

}
