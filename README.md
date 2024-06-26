# IDS-SYSTEM
AN ASYNCHRONOUS IDS SYSTEM THAT CAN CATEGORIZE THE INCOMING REQUEST IS A NORMAL REQUEST, U2R, R2L, PROBE, DOS.

DATA SET: a network whose incoming and outgoing requests are observed.
parameters: 81 parameters (label is an addition parameter added)


In this IDS system, we have used the asynchronous IDS method, anomaly-based detection.
 the code is divided into 3 parts where 
 1. app.py (python file)
 2. appdb.py (python file)
 3. mailer.py( python file)

    the model used is an ADAboost model, which uses feature selection, and feature extraction for the detection and classification of the incoming request.
    the steps to run the program is simple.
    1. run the app.py which will generate a link.
    2. paste the link on your browser and enter.
    3. this will bring you to the interface of our project.
    4. nd you can paste your test scenarios and enter and get it detected. 
