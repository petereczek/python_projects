import time
from datetime import datetime as dt
import platform
#determine path to hosts file depending on OS
if platform.system() in ['Linux','Darwin']:
	hosts_path = "/etc/hosts"
elif platform.system() == 'Windows':
	hosts_path = 'C:\Windows\System32\Drivers\etc\hosts'	
local_ip= "127.0.0.1"
#Get domain names to block from user
info = str(input("Enter domain names to be blocked as a space separated list (fe. 'facebook.com twitter.com etc':\n\n")).split()
#Save values of blockstart, blockend, blockperiodstart, blockperiodend for reuse when rebooted in file saved.txt,
#import them and save them to those variables upon restart of the program
blockmode, blockstart, blockend, blockperiodstart, blockperiodend = '','','','',''
savedlist = []
i=0
with open('saved.txt','r+') as saved:
	periodlines = saved.readlines()
	#extract saved times from file and store them in 'savedlist'
	for line in periodlines:
		if i == 0:
			savedlist.insert(i,line[:-1])
		elif i in [1,2]:
			savedlist.insert(i,dt.strptime(line[:-1],'%Y/%m/%d %H:%M'))
		else:
			savedlist.insert(i,dt.strptime(line[:-1],'%H:%M').time())
		i+=1
	#For as many elements as there are in 'savedlist', assign them to the variables storing block info(very ugly solution)
	for j in range(5):
		if j<= i-1:
			print(type(savedlist[j]))
			if j == 0:
				blockmode = savedlist[j]
			elif j == 1:
				blockstart = savedlist[j]
			elif j == 2:
				blockend = savedlist[j]
			elif j == 3:
				blockperiodstart = savedlist[j]
			else:
				blockperiodend = savedlist[j]
		else:
			pass
		j+=1
	
	#If blockstart or blockend have no value after restart, get vals from user, otherwise pass
	if  blockmode!='s' and blockmode!='p':#not blockmode or not blockstart or  not blockend:

		#Get mode from user (block sites at a point in time or periodically, get overall start and end time, and if 			periodically, get period start and end times)
		blockmode = str(input("Choose a blocking mode: For a single block time type 's', for periodic blocking, type 'p':\n\n"))
		if blockmode != 's' and blockmode != 'p':
			print('Invalid input.'+'\n'+"Choose a blocking mode: For a single block time type 's', for daily periodic blocking, type 'p':\n\n") 
		else:
			#Seek to start of file, save values of blockstart, blockend, blockperiodstart, blockperiodend 
			#to 'saved.txt' file after formatting them to time format used in script
			saved.seek(0)
			blockstart = str(input("\nEnter overall block start time yyyy/mm/dd hh:mm, or 'now'(24hour format):\n\n"))
			blockend = dt.strptime(str(input("\nEnter overall block end time yyyy/mm/dd hh:mm:\n\n")),'%Y/%m/%d %H:%M')
			if blockstart == 'now':
				blockstart = dt(dt.now().year,dt.now().month, dt.now().day, dt.now().hour, dt.now().minute)
			else:
				blockstart = dt.strptime(blockstart,'%Y/%m/%d %H:%M')	
			#Convert overall blockstart and end time to text to be saved to 'saved.txt'
			forsave1 = blockstart.strftime('%Y/%m/%d %H:%M')
			forsave2 = blockend.strftime('%Y/%m/%d %H:%M')
			if blockmode == 'p':
				#Periodic blocking will start daily at the inserted start time, and end at the inserted end time
				blockperiodstart = str(input("\nEnter daily block period start time hh:mm, or 'now':\n\n"))
				#If I didn't add '.time()', dt would've auto assumed date is 1900-1-1				
				blockperiodend = dt.strptime(str(input("\nEnter daily block period end time hh:mm:\n\n"),'%H:%M')).time()
				if blockperiodstart == 'now':
					blockperiodstart = dt.now().time()
				else:
					
					blockperiodstart = dt.strptime(blockperiodstart,'%H:%M').time()
				#Convert overall blockstart and end time to text to be saved to 'saved.txt'
				forsave3 = blockperiodstart.strftime('%H:%M')
				forsave4 = blockperiodend.strftime('%H:%M')
				saved.write(blockmode+'\n'+forsave1+'\n'+forsave2+'\n'+forsave3+'\n'+forsave4)
			else:
				saved.write(blockmode+'\n'+forsave1+'\n'+forsave2+'\n')
				
	else:
		pass

#Copy content of info to blocklist
blocklist = info[::]

#Adding duplicating all addresses with 'www.' if they don't have it and without it if they do to cover different possible domain names
for i in info:
	
	if 'www.' in i:
		blocklist.append(i[4:])
		
	elif 'www.' not in i:
		blocklist.append('www.'+i)

blocklist = list(set(blocklist))

while True:
	#If in single blocking mode compare given block times with current time:
	if blockstart <= dt(dt.now().year,dt.now().month, dt.now().day, dt.now().hour, dt.now().minute) < blockend:
		print("\noverall blocking is on\n")
		if blockmode == 's':	
			try:
				with open(hosts_path, 'r+') as file:
					content = file.read()
					for website in blocklist:
						if website in content:
							pass
						else:
							file.write(local_ip + ' ' + website + '\n')
					print(content)
			except:
				print('Host file could not be located or user does not have root or admin permissions. Make sure your hosts file can be found at /etc/hosts on Mac or Linux, or at C:\Windows\System32\Drivers\etc\hosts on Windows, and that you are running this script as root on Mac or Linux or sysadmin on Windows.')
				break
	#If in periodic blocking mode compare given periodic block times with current time, provided current 
	#time is within range of overall start and end times:
		elif blockmode == 'p':
			if blockperiodstart <= dt.now().time() < blockperiodend:
				# If blocking is on, check if websites for blocking are contained in 'hosts' file, 
				#and if not, redirect their domains to local_ip
				print("\nblocking period is on\n")
				try:
					with open(hosts_path, 'r+') as file:
						content = file.read()
						for website in blocklist:
							if website in content:								
								pass
							else:
								file.write('\n'+local_ip + ' ' + website + '\n')	
						print(content)
				except:
					print('Host file could not be located or user does not have root or admin permissions. Make sure your hosts file can be found at /etc/hosts on Mac or Linux, or at C:\Windows\System32\Drivers\etc\hosts on Windows, and that you are running this script as root on Mac or Linux or sysadmin on Windows.')
				break
			else:
				#If blocking is off, for each line of 'hosts' file, check if any of the websites are
				#contained in it, and if not, overwrite the file line with itself. Otherwise, do nothing.
				#Next, seek to the beginning of the file, so the website free lines get written at top of file	
				#Finally, use the truncate method to delete all iterations of content that were pasted into file 
				try:
					with open(hosts_path, 'r+') as file:
						content = file.readlines()
						file.seek(0)
						for line in content:
							if not any(website in line for website in blocklist):	
								file.write(line)
						file.truncate()
						print("\nblocking period is off\n")						
				except:
					print('Host file could not be located or user does not have root or admin permissions. Make sure your hosts file can be found at /etc/hosts on Mac or Linux, or at C:\Windows\System32\Drivers\etc\hosts on Windows, and that you are running this script as root on Mac or Linux or sysadmin on Windows.')		
					break
	else:
		try:
			with open(hosts_path, 'r+') as file:
				content = file.readlines()
				file.seek(0)
				for line in content:
					if not any(website in line for website in blocklist):
						file.write(line)
				file.truncate()
				print("overall blocking is off, hosts file cleared of domains.")
		except:
			print('Host file could not be located or user does not have root or admin permissions. Make sure your hosts file can be found at /etc/hosts on Mac or Linux, or at C:\Windows\System32\Drivers\etc\hosts on Windows, and that you are running this script as root on Mac or Linux or sysadmin on Windows.')
			break						
		with open('saved.txt', 'r+') as savemodeinfo:
					savemodeinfo.seek(0)
					savemodeinfo.truncate()
					print("savemodeinfo cleared")					
						
	time.sleep(5)














	
