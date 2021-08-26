# About

This is the working-repository for a research project conducted by Elias Ladenburger during his internship at the AIT.

## Goal

The purpose of this research project was to develop a software application, with which strategic cybersecurity awareness games (SCAG) can be created and conducted. 
SCAGs are targeted towards the management and senior management of an organization.
The SCAG itself will follow a collaborative, scenario-based approach, wherein a group of participants are confronted with a description of realistic situations and must discuss the best course of action in such situations.

## File Structure

- artefacts
    - _all tangible artefacts related to the research project._
    - requirements
      - _Anything related to the conceptual functionality of the system. Use case descriptions and diagrams, requirements documentation, etc._
      - ideation
        - _loose collection of ideas related to the project._
      - stakeholder requirements
        - _original set of requirements made by Dr. Maria Leitner._
    - dynamic view
      - _a number of sequence diagrams that describe the inner workings of this system. These were created with websequencediagrams.com._
    - static view
      - _a number of *class diagrams* that describe the architecture of this system. These were created with draw.io._
    - project level
        - _artefacts that impact the entire project._
- source
    - _the source code for any and all files necessary for running the prototype._
- licenses
  - _licenses for all of the software modules used in this project._
- README.md (you are here)


## How to use
### Requirements
This code was written with Python 3.8, but has successfully been tested with python3.7. 
All other requirements are listed in the requirements.txt file. 
This code was developed on a Microsoft Windows, although any platform capable of running Python should in principle be able to run this code. 

### Installation
#### Manual Installation
Clone this repository with
  
    git clone {link-to-this-repository}
    
Move into the newly created directory

    cd {project-name}

Set up your virtual environment:
    
    python3 -m venv my-venv
    # Windows
    # my-venv\Scripts\activate.bat 
    #
    # Unix (MacOS, Linux)
    # source my-venv/bin/activate
    
In your venv environment run:

    python3 -m pip install -r requirements.txt
    
You are now set to run this code.

NOTE: Windows users occasionally run into trouble with python wheels. 
If this is the case, you may need to download and install the wheels manually, as described [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

#### With PyCharm
This code has been developed and successfully tested with the PyCharm student edition.
Setup with PyCharm works reliable and quite easy.

Here's how to setup the project in PyCharm (as of 2021):
1. Open PyCharm
2. EITHER
    1. Close the current project OR
    2. Navigate to the _VCS_ tab (VCS == version control system)
4. Select _Get from Version Control_
5. Select _https_ and enter the link to this repository.
6. Click _Clone_ - The project should set up now.
7. Navigate to the _File_ tab
8. Select _Settings_ > _Project: scag-platform_ (or whatever name you selected when importing this project)
9. Select _Project Interpreter_
10. Click the _gear_ icon in the top right-hand corner
11. Click _add_
12. Select _virtualenvironment_ > _new environment_
13. Select _Create_
14. Your project should now be setup successfully

### Setup and Configuration

The configuration for this platform can be found in [source > config.yml](/source/config.yml). 
Make sure to update the database connections, server name and other relevant information in this file, before actual deployment.

### Running the program
#### Starting the server

To run the production server, simply navigate to the web-project that we have setup alongside the main project.
    
    cd source/presentation_layer

Then run the flask-app:

    python production_server.py
    
You are now able to access the web interface [here](https://127.0.0.1:5000).

### Testing
Tests are located in the [source > tests](/source/tests) subdirectory. They can be run by executing 

    python -m unittest
    
## Future Work
### Known Bugs

This project has been put into an almost usable state. However, a few bugs and inconveniences remain:
- The form for **inject choices** is still very cumbersome and unintuitive to use:
  - after adding a page, the entire page must be refreshed before a new choice can be added 
  (_can likely be solved with a simple Javascript function that appends fields based on a template_).
  - To delete a choice, the "label" of the choice must be cleared
    (_can likely be solved with a simple Javascript function that automatically removes fields, if the choice is to be deleted_).
  - It is currently not possible to add a "variable change" to a choice
    (_There are two obstacles here: one is that the subform for variable changes has the same two issues as the choices form mentioned above._
  _The other issue is that the form currently does not actually connect to the "Variable Change" object - here some (minor) code changes may still be necessary_).

### Known Change-Requests
There are also some known change requests that I have so far not been able to implement.
These include:
- Allowing the trainer of a game to change the type of diagram that is shown to participants after each inject.
- Allowing the trainer of a game to set _breakpoints_ at specific injects, beyond which participants are not allowed to advance, until the trainer allows so.
- Allowing participants to change a previously given answer.
- Allowing different types of inject (such as text input or multi-select).

## Licenses

For fast prototyping, this project has used available (open-source) code, without much regard for licensing.
If this project is to be deployed in productive use, some or all of the modules listed below may need to be exchanged 
for software that allows propietary distribution.

All licenses can be found at [licenses](/licenses).

|       Module  |        License |
|   ----------  |        ------- |
| JQuery        | MIT            |
| Bootstrap     | MIT            |
| QRious        | GPL 3          |
| CanvasJS.com  | Unclear (may need to be switched out)  |
| VisJS network | Apache (or MIT, dual licensed) |
| Flask         | Flask License  |
| Pydantic      | MIT            |
| MongoDB       |   SSPL (Server Side Public License) |
| Waitress Server | ZPL (Zope Public License) |