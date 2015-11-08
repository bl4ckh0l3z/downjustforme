# DownJustForMe - Changelog


## 1.4 (Nov 08, 2015)

###Features

  - Added logrotate installation and config 


## 1.3 (Nov 06, 2015)

###Fixes

  - Fixed checks on http redirections 
  - Fixed logging for each thread


## 1.2 (Sep 14, 2015)

###Features

  - Checks are executed using a multi-threading approach
  - Added mutex/semaphore/concurrency check against parallel execution


## 1.1 (Sep 05, 2015)

###Features

  - Added the support for the Selenium project, in order to support web-pages
    accompagnied by javascript code.

###Fixes

  - Fixed the methods used to verify the defacement of monitored websites.


## 1.0 (Apr 1, 2015)

###Features

  - Detects if the web server (running the website) is under a Denial of Service
    (DoS) attack.
  - Detects if the web server (running the website) is currently unable to handle
    the HTTP requests due to a temporary overloading at the TCP or HTTP layer. 
  - Recognizes attacks on websites whereby nefarious individuals attempt to change a 
    website's content (i.e. defacement).
  - Calculates statistical data describing the scenarios of bandwidth saturation,
    network link attacks and defacement.
  - Saves results of the current and previous iterations respectively in the in and
    out folders.
  - Notifies anomalies by email. 
