import tkinter as tk
from datetime import datetime
import os
import numpy as np
import json

global HEIGHT
global WIDTH
global suffix

HEIGHT = 100
WIDTH = 405
suffix = ".json"

offset_from_top = 20
row_height = 40

col_1 = 20
col_2 = 145
col_3 = 217
col_4 = 363

timers = []
c = 0

global timer_count
timer_count = 1

today = datetime.now().strftime('%Y_%m_%d')

# background_color='#05152e'
# save_button_color = '#06c68c'
# text_color = '#8db5f2'

text_color = '#a8bf9a'
background_color = '#182037'
# save_button_color = '#a8bf9a'
save_button_color = '#2b2528'


def main():
	timers.append(Timer(frame, timer_count))
	print("timer 1 added")
	root.mainloop()


def addTimer():
	global timer_count
	global HEIGHT

	timer_count = len(timers) + 1
	timers.append(Timer(frame, timer_count))

	print("timer " + str(timer_count) + " added")

	HEIGHT = (timer_count - 1) * row_height + 100
	canvas.configure(height=HEIGHT)


def saveData():
	global suffix
	today = datetime.now().strftime('%Y_%m_%d')
	name = file_name.get()
	all_timers = dict()

	all_timers["date"] = today
	all_timers["projects"] = dict()

	for obj in timers:
		timer_data = obj.getJsonTime()
		timer_name = str(timer_data["name"])
		all_timers["projects"][timer_name] = dict()

		all_timers["projects"][timer_name]["hours"] = timer_data["hours"]
		all_timers["projects"][timer_name]["minutes"] = timer_data["minutes"]
		all_timers["projects"][timer_name]["seconds"] = timer_data["seconds"]
	
	if name == "":
		name = today + suffix

	if os.path.exists(name):
		temp = len(name)-len(suffix)
		name = name[:temp] + "_" + name[temp:]
		with open(name, "w") as file:
			json.dump(all_timers, file, indent=2)
		print("File already existed. Changed filename to: " + name)
	else:
		with open(name, "w") as file:
			json.dump(all_timers, file, indent=2)
			print("Writing file: " + name)

	file_name.delete(0, len(name))
	file_name.insert(0, str(name))

	with open(name) as file:
		print(json.load(file))

		# data = json.load(file)
		# for project in data["projects"]:
		# 	print(project)


def sumJsonFiles():
	location = os.getcwd()	
	counter = 0 		#keep a count of all files found
	jsonfiles = []

	for file in os.listdir(location):
	    try:
	        if file.endswith(".json"):
	            # print("json file found:\t", file)
	            jsonfiles.append(str(file))
	            counter = counter+1
	    except Exception as e:
	        raise e
	        print("No files found here!")
	print("Total files found:\t", counter)

	# for f in jsonfiles:



def sumFiles():
	location = os.getcwd()		 # get present working directory location here
	counter = 0 		#keep a count of all files found
	txtfiles = []			#list to keep any other file that do not match the criteria
	project_name = ""
	list_of_projects = []
	list_of_times = []

	for file in os.listdir(location):
	    try:
	        if file.endswith(".txt"):
	            # print("txt file found:\t", file)
	            txtfiles.append(str(file))
	            counter = counter+1
	    except Exception as e:
	        raise e
	        print("No files found here!")
	print("Total files found:\t", counter)

	for f in txtfiles:
		file = open(f)
		for line in file:
  			
  			#print("line: "+ str(line))
  			project_name = ""
  			if line[0] == " ":
  				
  				# offset = line.find(separator)
  				project_name = formatLine(line)[0]
  				time = np.asarray(formatLine(line)[1])
  				
  				#print ("project_name: " + str(project_name) + "\ntime: " + str(time))

	  			if project_name in list_of_projects:
	  				index = list_of_projects.index(project_name)
	  				
	  				#print("added values @ index: ", index)
	  				list_of_times[index] += time
	  			else:
	  				list_of_projects.append(project_name)
	  				list_of_times.append(time)
	  				
	  				#print("appended: ", len(project_name))
		print(">>> NEW file: ",  f, "\n", file.read())

	print("list_of_projects: ", list_of_projects)
	print("list_of_times: ", list_of_times, "\n")

	list_of_times = formatTime(list_of_times)
	print("list_of_projects: ", list_of_projects)
	print("list_of_times: ", list_of_times, "\n")

	saveSumData(list_of_projects, list_of_times)
		# folder_for_single_files = os.path.join(location, r'new_folder')
		# if not os.path.exists(folder_for_single_files):
		# 	os.makedirs(folder_for_single_files)


def formatTime(times):
	print("formatTimes() ", times)
	for time_sum in times:
		for i in range(0, 2):
			if time_sum[i] > 59:
				leftover = time_sum[i] % 60
				additional_time = (time_sum[i] - leftover) / 60
				time_sum[i+1] += additional_time
				time_sum[i] = leftover
				print("time_sum[",i,"]: ", time_sum[i], "current val: ", times[i], "leftover: ",  leftover, "additional_time", additional_time)

	return times

def saveSumData(list_of_projects, list_of_times):
	global suffix
	today = datetime.now().strftime('%Y_%m_%d')
	name = "SUM_" + today

	if name == "":
		name = "SUM_" + today
	try:
		f = open(name+suffix, "x")
	except:
		name += "_"
		f = open(name+suffix, "x")

	print("writing file: " + name + suffix)
	print(">>> Timer Data:")

	f.write("Summarized on: " + today + "\n")

	for project, time in zip(list_of_projects, list_of_times):
		# print(str(project) + ": " + str(time))
		f.write(str(project) + ": " + str(time) + "\n")


	# for obj in list_of_projects:
	# 	pass
	# 	#f.write(" " + str(obj.getTime()) + "\n")
	# 	#print(">>> " + obj.getTime())

	# print(">>> OUT file: ","\n", f.read())
	f.close()

def formatLine(line):	
	separator = ":"
	project_name = line.split(separator)[0][1:]
	time = line.split(separator)[1][1:]
	# print ("project_name: ",project_name,"\ntime: ", time)
	s_m_h = [0, 0, 0]
	i = 0
	index = 0

	while i < len(time)-1:
		if time[i].isdigit():
			# print("found a number: " + time[i] + time[i+1] )
			if time[i+1].isdigit():
				s_m_h[index] = int(time[i]) * 10 + int(time[i+1])
				i += 3
				# print("found: ", s_m_h[index])
			else:
				# print("index; ", index)
				s_m_h[index] = int(time[i])
				i += 2
			# print("s_m_h[",index,"]: ",s_m_h[index])
			index += 1
		else:
			i += 1
			# print("next ",i+1,"\n")

	return project_name, s_m_h


root = tk.Tk()
root.resizable(False, False)
# root.wm_attributes("-transparentcolor", 'grey')
bg = tk.PhotoImage(file="bg3.PNG")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#282d3e')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

background = tk.Label(frame, image=bg)
background.place( x=-50, y=0, width=500, height=1000)

add_timer_button = tk.Button(frame, text="+", font=14, command=addTimer, bg=save_button_color, fg=text_color, bd=0)
add_timer_button.place(relx=0.05, y=12, width=40, height=22)
#add_timer_button.configure(highlightbackground='#06666e', highlightcolor='#06666e')

save_button = tk.Button(frame, text="Save", font=14, command=saveData, bg=save_button_color, fg=text_color,  bd=0)
save_button.place(relx=0.16, y=12, width=60, height=22)

sum_button = tk.Button(frame, text="Sum!", font=14, command=sumJsonFiles, bg=save_button_color, fg=text_color,  bd=0)
sum_button.place(relx=0.75, y=12, width=100, height=22)

file_name = tk.Entry(frame, font=8, bg=save_button_color, fg=text_color, bd=0)
file_name.place(relx=0.33, y=12, width=200, height=22)
file_name.insert(0, str(today)+suffix)



class Timer:
	def __init__(self, parent, row):

		self.seconds = 0
		self.mins = 0
		self.hours = 0
		self.index = row
		# self.y = row / 11 + 0.03 			# 1 / 11 + 0.03 * 500 = 60.4545 pixel
		self.y = 40 * row + offset_from_top
		#print(self.y)
		self.running = False

		# self.delete_button = tk.Button(parent, text=" Start ", font=15, command=self.startTimer, bg=background_color, fg=text_color, bd=0)
		# self.delete_button.place(rely=self.y, x=col_2, relheight=0.05)

		self.name_label = tk.Entry(parent, font=8, bg=background_color, fg=text_color, bd=0)
		self.name_label.insert(-1, 'Enter name')
		self.name_label.place(y=self.y, x=col_1, relwidth=0.3, height=22)
	
		self.start_button = tk.Button(parent, text=" Start ", font=14, command=self.startTimer, bg=background_color, fg=text_color, bd=0)
		self.start_button.place(y=self.y, x=col_2, height=22)

		self.time_label = tk.Label(parent, text="0s 0m 0h", font="Arial 14", width=10, bg=background_color, fg=text_color, bd=0)
		self.time_label.place(y=self.y, x=col_3, relwidth = 0.42, height=22)

		self.reset_button = tk.Button(parent, text="X", font=14, command=self.resetTimer, bg=background_color, fg=text_color, bd=0)
		self.reset_button.place(y=self.y, x=col_4, height=22)

	def startTimer(self):
		if self.running == False:		
			self.running = True
			self.refreshLabel()

			print("timer " + str(self.index) + " started")
			self.start_button.configure(text="Pause")
		else:	
			self.running = False

			print("startTimer(): timer " + str(self.index) + " stopped ")
			self.start_button.configure(text=" Start ")

	def refreshLabel(self):
		self.seconds += 0.1

		if self.seconds > 60:
			self.mins += 1
			self.seconds = 0
		if self.mins > 60:
			self.hours += 1
			self.mins = 0

		# print(str(self.seconds) + " state:" + str(self.running))
		self.time_label.configure(text="%is" % int(self.seconds) + " %im" % int(self.mins) + " %ih" % int(self.hours))

		if self.running == True:
			self.time_label.after(100, self.refreshLabel)

	def resetTimer(self):
		print("timer reset")
		self.seconds = 0
		self.mins = 0
		self.hours = 0
		self.time_label.configure(text="0s 0m 0h")

	def getTime(self):
		return self.name_label.get() + ": " + str(int(self.seconds)) + "s " + str(self.mins) +  "m " + str(self.hours) + "h"

	def getJsonTime(self):
		output = dict()
		output["name"] = self.name_label.get()
		output["hours"] = int(self.hours)
		output["minutes"] = int(self.mins)
		output["seconds"] = int(self.seconds)
		return output


if __name__ == "__main__":
	main()