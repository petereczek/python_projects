Interactive Python Program that blocks websites chosen by user at specific dates and times or daily at specific times. It does so by accessing and adding domain names to be blocked to the 'hosts' system file. Program must be run as root (superuser) because it modifies this system file.
In Linux and Mac, open terminal window, and enter 'sudo python website_blocker.py', and enter your password to run. 
In Windows, navigate to the 'website_blocker.py' file location, right click on it, and choose "Run as administrator" and enter password if prompted to run the program.

If you do not run this program as root or admin, it will not work.
In order for the program to block periodically even after the machine is restarted, download the 'saved.txt' file and place it in the same folder as the 'website_blocker.py' script.

To allow 'website_blocker' to run periodically at scheduled times without being interrupted by system startup and shutdown, set the program to start automatically during system startup.

In Mac and Linux, you can use crontab to schedule program boot at startup. To do this, open your terminal, and type:    

			crontab -e

The crontab file will open in vi editor. To allow 'website_blocker' to start at system boot, scroll down to the last line of the crontab file, and on a new line, enter:

			@reboot python /path/to/web/blocker

entering the location path of the 'website_blocker' script instead of '/path/to/web/blocker'.
To prevent 'website_blocker' from running at boot again, simply remove the last line that you entered in the crontab file.

