#!/usr/bin/env python
import os
import os.path
import sys
from crontab import CronTab
import datetime
import time
from pathlib import Path
import shutil
import getpass
import pwd



cron = CronTab(user=True)  
m=1
global ip
ip = 0 
d = datetime.date.today()
t = time.strftime("%H:%M:%S")
h = int(time.strftime("%H"))
m = int(time.strftime("%M"))
m = m+2
dt = d.day
mo = d.month
usr = "pavan"
RED = "\033[0;31;48m"
DEFT = "\033[0;37;48m"
Green = "\033[0;32;48m"



def fun_scan_status():
	i=0
	while i < len(Nmap_list):
		with open(dir_crt+"/"+Nmap_list1[0+i]+"_"+ip+".nmap", 'r') as searchfile:
 			for line in searchfile:
  				if "Nmap done" in line:
  					{}
  				i += 1

def save_ips(ip):
	saveFile = open("ips.txt","a")
	# saveFile.write("\n")
	saveFile.write("ip:"+ip)
	saveFile.close()



print(Green+"=========Nmap schedule Scans========="+DEFT)

########### checking for File_path.txt is available or not ################################
if os.path.exists("File_path.txt"): 
	with open('File_path.txt', 'r') as searchfile:
	 	for line in searchfile:
 			if "Daful_folder" in line:
 				dnk = line
 		a, Def_dir = map(str, dnk.split(" "))
 		Def_dir = Def_dir.strip()
 		print("Default path found: "+RED+Def_dir+RED)
 		print(DEFT)
else:
	
	Def_dir = input("Enter the Default directory location: ")
	########### store default location path to file_path.txt ################################
	saveFile = open("File_path.txt","w")
	saveFile.write("Daful_folder "+Def_dir)
	saveFile.write("\n")
	saveFile.close()


# ########### Creating folder in specified location #######################################
App_name = input("Enter the Application name: ")
dir_crt = os.path.join(Def_dir, App_name)
if os.path.exists(dir_crt):
	print("Application name already exixts: " +RED+dir_crt+DEFT)
	# print(DEFT)
	
else:
	
	os.makedirs(dir_crt)
	shutil.chown(dir_crt, user=usr, group=None)
	saveFile = open("File_path.txt","a")
	saveFile.write("\n")
	saveFile.write(Def_dir+"/"+App_name)
	saveFile.close()
	# Correct = True


Nmap_list=[" -sT -p 1-65535"," -sU -p 1-65535 ","--script=discovery", "--script=http-auth.nse", "--script=default"]
Nmap_list1=["TCP_all_ports","UDP_all_ports","Discovery", "Auth", "Default"]
choice1 = 0

while int(choice1) not in range(1,4):
	choice1 = input('''
	1. Nmap
	2. Status
	Enter your choice: ''')

choice1 = int(choice1)


####### For Nmap Scheduling ##########
if choice1 == 1:
	i=0
	ip_lst = ""
	chce = input("\033[0;31;48m \t Do you want to scan a list(Y/N):  \033[0;31;48m")
	print("\033[0;37;48m \033[0;37;48m")
	if chce.upper() == "Y" :
		ip_lst = input("Enter the IP list file name(without extension): ")
		save_ips(ip_lst)
		sch_scn_y = input(" Do you want to schedule Namp scan now(Y or N): ")
		if sch_scn_y.upper() != "Y":
			sch_scn = input("Enter month day and time(HH:MM:Date:Month): ")
			h, m, dt, mo = map(str, sch_scn.split(":"))
		while i < len(Nmap_list):
			NML = "nmap -sV -sC -Pn "+Nmap_list[i]+" -iL "+ip_lst+".txt"+" -oA "+dir_crt+"/"+Nmap_list1[0+i]+"_"+ip_lst
			job = cron.new(NML)
			job.minute.on(m)
			job.hour.on(h)
			job.day.on(dt)
			job.month.on(mo)
			cron.write()
			print("Nmap "+Nmap_list1[i]+" scan scheduled on "+str(d.day)+"-"+str(d.month)+" at "+str(h)+":"+str(m))
			m += 15
			if m>=59:
				h +=1
				if h>=24:
					h=0
				m=0
			i += 1
	else:

		ip = input("Enter the IP Address: ")
		save_ips(ip)
		sch_scn_y = input(" Do you want to schedule Namp scan now(Y or N): ")
		if sch_scn_y.upper() != "Y":
			sch_scn = input("Enter month day and time(HH:MM:Date:Month): ")
			h, m, dt, mo = map(int, sch_scn.split(":"))
		while i < len(Nmap_list):
			NML = "nmap -sV -sC -Pn "+Nmap_list[i]+" "+ip+" -oA "+dir_crt+"/"+Nmap_list1[0+i]+"_"+ip
			job = cron.new(NML)
			job.minute.on(m)
			job.hour.on(h)
			job.day.on(d.day)
			job.month.on(d.month)
			cron.write()
			print("Nmap "+Nmap_list1[i]+" scan scheduled on "+str(d.day)+"-"+str(d.month)+" at "+str(h)+":"+str(m))
			m += 15
			if m>=59:
				h +=1
				if h>=24:
					h=0
				m=0
			i += 1
	print("Nmap Scans run untill "+str(h)+" hours "+str(m)+" Munites ")

elif choice1 == 2:
	i=0
	print("Nmap Scan Status")
	with open('ips.txt', 'r') as searchfile:
	 	for line in searchfile:
 			if "ip" in line:
 				a, ip = map(str, line.split(":"))
 				print(ip)
 			while i < len(Nmap_list):
 				if os.path.exists(dir_crt+"/"+Nmap_list1[0+i]+"_"+str(ip)+".nmap"):
 					print(Nmap_list1[0+i]+" Scan started")
 					fun_scan_status()
 					print(Nmap_list1[0+i]+" scan on "+Green+str(ip)+DEFT+" has"+Green+" finished"+DEFT)
 					i +=1
 				else:
 					print(Nmap_list1[0+i]+" scan under process")
 					print(RED+"Other scans not yet started"+DEFT)
 					break
