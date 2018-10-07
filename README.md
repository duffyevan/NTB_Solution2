# NTB WPZ EMail Auto-Downloader
This program is designed to automate the collection of data files from PLC modules in the field collecting data on Heat 
Pump Systems. 


# Installation
This section will walk you through the installation process of the software. __If you are on hostpoint you can skip to 
step 3.__


### 1. Installing Python
If python is not already installed, please follow these instructions:

The program is written for python 3, specifically 3.6 and above. 
1. Go To [The Python Install Page](https://www.python.org/downloads/) and chose the most recent version of python3 
(currently 3.7)
2. Run the installer that is downloaded, and follow the steps for a default installation (if asked, make sure you add
python to PATH and associate .py files with the python launcher, these should be done by default) 
    1. If prompted, make sure you chose to install `pip` as well. 
3. Open up CMD and make sure python is in the path by running python (or python3 if that doesn't work). If a prompt
comes up, then python is installed correctly. Type `exit()` to close python.


### 2. Installing Required Python Packages
1. In a command prompt, naviage to the `ntb-mail-downloader` folder
2. Run the command `python -m pip -r requirements.txt` to install the required packages.
    1. You may need to have admin privileges to run this command. If so, reopen CMD in administrator mode (or use sudo 
if on a unix based machine)


### 3. Configuring The Program
One quick configuration step is required. 
1. Create a file in the `ntb-mail-downloader` folder called `login.csv`.
2. Three sets of login credentials are needed in the format as follows
```
<SMTP server to download mail from>,<user email for that server>,<password for that user>
https://cloud.ntb.ch,<your ntb username>,<your ntb password>
<IMAP server to send alert emails from>,<IMAP port>,<alert email user email>,<alert email user password>
```
For example:
```
imap.mail.hostpoint.ch,datain@wp-feldmessung.ch,PASSWORD
https://cloud.ntb.ch,c-duffy,PASSWORD
asmtp.mail.hostpoint.ch,587,datain@wp-feldmessung.ch,PASSWORD
```
This information is used to receive attachments, back them up to NTB's cloud, and send alert emails if a PLC does not
 email in on a given day (respectively)

### 4. Running The Program
The program can be run manually from the command line by navigating to the `ntb-mail-downloader` folder and running:
```
python3 main.py <destination folder>
```
This will cache the files to a local directory, determine which ones are new, copy them to the destination folder, 
and back them up to a folder on NTB's cloud


### 5. Setting Up A Cron Job
To make the program run every night, or on some schedule, a cron job can be used. A cron job can be added by running 
`crontab -e` from the command line in a unix based system. The cron job currently set up on HostPoint looks like this:
```
0 3 * * * cd /home/wpfeldme/test/ntb-mail-downloader/; python3 /home/wpfeldme/test/ntb-mail-downloader/main.py /home/wpfeldme/www/auto.wp-feldmessung.ch/file_content/new >> /home/wpfeldme/test/ntb-mail-downloader/cron.log 2>&1
```

This will run the program every evening at 3:00 AM. The command is broken down into a few parts:
- The `cd` part changes the directory into the directory where the program is stored
- The next part runs the program main.py with the argument being the destination folder for data processing
- The part after `>>` is to redirect any program output to a file called `cron.log` in the same folder. Most output 
goes to `log.txt` but if there is some unhandled error and the program crashes, the output will be in `cron.log`