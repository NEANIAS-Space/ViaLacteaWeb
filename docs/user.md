# User documentation

Release Version: 1.0

Designed by: Evgeniya Malikova ([evgeniya.malikova@port.ac.uk](mailto:evgeniya.malikova@port.ac.uk))

26/10/2021

**Contents**

[Introduction](#_2e4adhj8bp1)

[Access to the VLKB service](#_yxqmzovmjunh)

[User Interface](#_j8busrl1cvl3)

[Loading DataCube surveys](#_rfyshmcaq7qz)

[Datacube interactive Visualization](#_33u1ujb5vg7j)

[2D and 3D interaction](#_fiwuuro9xggg)

[Tools bar](#_y1v1y5r81kbj)

## Introduction

Space missions and ground-based facilities collect increasingly huge amounts of data that demand novel approaches to data processing, storage, visualization and analysis.

The [ViaLactea project](https://www.neanias.eu/index.php/dissemination-open-access/articles/432-neanias-space-vialactea)is an ecosystem that offers the Astrophysics and Planetary communities highly interactive visual analytic interfaces enabling effective exploitation of multi-wavelength observations of the Milky Way Galactic Plane, ranging from the near infrared to the radio spectrum. ViaLactea strongly promotes FAIR data and Open Science practices and is integrated within the European Open Science Cloud (EOSC).

As a part of this research, the ViaLactea Web (VLW) solution is developed as a collaborative web solutions for multi-user support underpinned by efficient remote server CPU and GPU rendering, and support of mobile and desktop devices. All underlying data is managed by a dedicated data service, namely the ViaLactea Knowledge Base, that provides object catalogs and Spectral Energy Distribution model outputs to carry out correlation analysis workflows for studying the star formation process in our Galaxy. The overall performance experiences is defined by remote GPU and CPU visualisation server performance.

The NEANIAS ViaLactea Web is available at

[https://visivo-server.oact.inaf.it](https://visivo-server.oact.inaf.it/).

The main requirements are:

- Internet Access and Firefox Web browser
- Microsoft or Google account for authentication
- Access to the VLKB service through the NEANIAS Service Management System (SMS) (see [section 1](#_yxqmzovmjunh))

The service demo video is available at [https://youtu.be/F6Q4xiMbHqg](https://youtu.be/F6Q4xiMbHqg)


## Access to the VLKB service

To receive an access to VLKB service, follow the steps below:

1) Open the NEANIAS SMS page using this [link] https://sms.neanias.eu/projects/neanias-sms/issues/new?issue[tracker\_id]=13&amp;issue[subject]=Access+request+for+ViaLactea

2) Login with NEANIAS SSO using a Microsoft or Google account.

3) Fill and submit the access request form. You will access all public surveys by default. If you want to ask for access to private surveys you can select the surveys by selecting the checkboxes in the ViaLactea surveys field. There are four private surveys currently available. The &quot;AllPrivate&quot; option includes all of them.

4) You will receive email notifications by the NEANIAS SMS about the processing of your access request. When the request is taken care of, the status will change to &quot;Under development&quot;. Once the status is set to &quot;Resolved&quot;, you can access the service.


## User Interface

After successful login the user is redirected to VLW web page with application main interface. The Web UI is designed as similar as possible to the UI of [ViaLactea desktop version](https://docs.neanias.eu/projects/s1-service/en/latest/services/vialactea.html). The UI components are inspired by the desktop version of ViaLactea but adapted for use within browser and different versions of screen Desktop/Tablet/Mobile. The current interface layout that covers a 3D DataCube visualisation aspects is presented in Fig. 1

![](im1.png)

Figure 1: The ViaLactea Web UI


## Loading DataCube surveys

To access DataCube surveys data, open a right panel by clicking on a Search icon ![](RackMultipart20211026-4-18pcllq_html_5c82c1ad47592e2.png) and enter galactic coordinates (see Fig.2)

![](im2.png)

Figure 2: Right panel

Confirm a VLKB query by clicking on the Query button (see Fig.2). Wait till query will be executed and the datacube is loaded.

The first available DataCube data would be loaded and available fo user interaction in 2D and 3D views. All set of datacubes for current VLKB query is available for selection from right panel (see Fig.3).

![](im3.png)

Figure 3: The list of available DataCube surveys




## Datacube interactive Visualization

As DataCube is loaded, the user can interactively explore data in 2D and 3D projections and via set of available operations in tools bar on top (Fig.4).

![](im4.png)

Figure 4: Tools bar to interact with DataCube data

### 2D and 3D interaction

The following types of user interaction are available:

- Adjust the 2D the image scale with mouse while holding down a right button.
- Rotate in 3D with mouse while holding down a right button.
- Zoom in/out in 3D with mouse wheel

### Tools bar

The following operations are available in navigation bar on top (Fig.4):

- The slider on the Cutting plane panel to select various 2D projections
- The checkbox on the Contours panel to display contours in 2D projections
- The slider on the Threshold panel to adjust the 3D isocontour value for DataCube.