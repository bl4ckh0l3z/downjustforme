                       
                         \|/                          
                       `--+--'                        
                         /|\                          
                        ' | '                         
                          |                           
                          |                           
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'      
     ____                          _           _   _____          __  __      
    |  _ \  _____      ___ __     | |_   _ ___| |_|  ___|__  _ __|  \/  | ___ 
    | | | |/ _ \ \ /\ / / '_ \ _  | | | | / __| __| |_ / _ \| '__| |\/| |/ _ \
    | |_| | (_) \ V  V /| | | | |_| | |_| \__ \ |_|  _| (_) | |  | |  | |  __/
    |____/ \___/ \_/\_/ |_| |_|\___/ \__,_|___/\__|_|  \___/|_|  |_|  |_|\___|



# DownJustForMe

## What is it?

"DownJustForMe" is an open-source and multi-threaded python tool intended to serve 
as a framework for a simple and easy-to-manage monitoring of institutional websites.
It is able to detect if the web server (running the website) is under a Denial of
Service (DoS) attack or it is currently unable to handle the HTTP requests due to
a temporary overloading at the TCP or HTTP layer. In addition to this funcionality 
"DownJustForMe" is able to recognizes attacks on websites whereby nefarious individuals
attempt to change a website's content; the intent of defacement is usually to change
graphics, vandalize content or intercept information. "DownJustForMe" and its defacement
monitoring capability can prevent far reaching consequences and "pharming" of potential
customers (e.g. an active defacement monitor can debunk attempts at "pharming", where
legitimate customers are redirected to spoof or fake website that pose as the official one).

Scenarios of bandwidth saturation, network link attacks and defacement are detected
and notified by email providing also additional statistics for troubleshooting purpose.

This is an example of the additional data reported by email:

<pre>
[
    "20150904164006",
    {
        "http://www.google.it/": [
            {
                "status_code_keywords": "fails",
                "time_start": 1441377610.089319,
                "status_code_tcp": "ok",
                "status_code_http": 200,
                "time_end": 1441377614.308083,
                "time_elapsed": 0.07031273444493612
            },
            {
                "status_code_keywords": "fails",
                "time_start": 1441377622.316776,
                "status_code_tcp": "ok",
                "status_code_http": 200,
                "time_end": 1441377623.382139,
                "time_elapsed": 0.017756048838297525
            },
            {
                "status_code_keywords": "fails",
                "time_start": 1441377631.388044,
                "status_code_tcp": "ok",
                "status_code_http": 200,
                "time_end": 1441377632.447105,
                "time_elapsed": 0.01765101353327433
            },
            {
                "status_code_keywords": "fails",
                "time_start": 1441377640.455778,
                "status_code_tcp": "ok",
                "status_code_http": 200,
                "time_end": 1441377641.534069,
                "time_elapsed": 0.017971519629160562
            }
        ]
    }
]
</pre>



## Configuration and Installation

``$ sudo chmod 700 configure.sh``  
``$ configure.sh``


## Running

``$ sudo chmod 700 run_downjustforme.sh``  
``$ run_downjustforme.sh -h``  
``$ run_downjustforme.sh -t -p -k -b -e``


## Package composition

The package is composed by:  
  - **downjustforme**
      - **config**: *the components that configure the entire project through a configuration file;*
      - **configure.sh**: *the bash script which automatise the configuration;*
      - **logs**: *the log file that contains detailed information about the execution of this framework;*
      - **in**: *the input folder which the tool uses to store the data collected by the current iteration;*
      - **out**: *the output folder;*
      - **archive**: *the folder which stores the data collected by the current and the previous iterations;*
      - **requirements.txt**: *the list of requirements used to setup the virtual environment;*
      - **run.py**: *the main python script;*
      - **run_downjustforme.sh**: *the bash script which automatise the execution of the
                            framework inside the virtual environment;*
      - **downjustforme.env**: *the python virtual environment dedicated to this project;*
      - **downjustforme.sh**: *the bash script which implements the typosquatting mechanisms.*


## Todo-list

Please see the TODO tag disseminated in the source code;
some grep will help you! :)


## Licensing

Please see the file called LICENSE.


## Contacts

bl4ckh0l3  
*bl4ckh0l3z at gmail.com*
