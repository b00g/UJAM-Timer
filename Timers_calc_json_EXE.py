import os, json, shutil, sys
import numpy as np
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from datetime import datetime

global HEIGHT, WIDTH, suffix

HEIGHT, WIDTH = 100, 405

suffix = ".json"

offset_from_top = 20
row_height = 40

col_0, col_1, col_2,col_3, col_4 = 5, 37, 166, 229, 345

timers = []

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

target_directory = filedialog.askdirectory(title="Select a directory for saved files") 
print(target_directory)

def resource_path(relative):
	return os.path.join(
		os.environ.get(
			"_MEIPASS2",
			os.path.abspath(".")
		),
		relative
	)
	return os.path.join(base_path, relative_path)


def main():
	image_path = resource_path("bg3.png")
	bg = tk.PhotoImage(file=image_path)
	background.configure(image=bg)

	# add_timer_icon_path = resource_path("addTimer.png")
	# add_timer_button_icon = tk.PhotoImage(file=add_timer_icon_path)
	# add_timer_button.configure(image=add_timer_button_icon)


	timers.append(Timer(frame, timer_count))
	timers[0].update(timer_count)
	print("timer 1 added")

	root.mainloop()


def addTimer():
	global timer_count
	global HEIGHT

	timer_count += 1
	print(len(timers))
	timers.append(Timer(frame, timer_count))
	timers[timer_count-1].update(timer_count)

	print("timer " + str(timer_count) + " added")

	HEIGHT = (timer_count - 1) * row_height + 100
	canvas.configure(height=HEIGHT)


def delTimer(timerIndex):
	global timer_count
	global HEIGHT
	print("timer " + str(timerIndex) + " deleted, length of timers[] was: ", timer_count)

	del timers[timerIndex-1]
	# timers.append(Timer(frame, timer_count))

	for i in range(len(timers)):
		timers[i].update(i + 1)

	timer_count = len(timers)
	print("length of timers[] is: ", len(timers))

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

	while True:
		if os.path.exists(os.path.join(target_directory, name)):
			temp = len(name)-len(suffix)
			name = name[:temp] + "_" + name[temp:]
			print("File already existed. Changed filename to: " + name)
		else:
			print("Writing file: " + name)
			with open(os.path.join(target_directory, name), "w") as file:
				json.dump(all_timers, file, indent=4)
			break

	file_name.delete(0, len(name))
	file_name.insert(0, str(name))

	with open(os.path.join(target_directory, name)) as file:
		print(json.load(file))

		# data = json.load(file)
		# for project in data["projects"]:
		# 	print(project)


def getFilesOfType(location, file_type):
	files = []
	counter = 0
	for file in os.listdir(location):
	    try:
	        if file.endswith(file_type):
	            files.append(str(os.path.join(location, file)))
	            counter += 1
	    except Exception as e:
	        raise e
	        print("No files found here!")
	print("Total files of type " + file_type +  " found: ", counter)
	return files


def sumJsonFiles():
	location = target_directory
	output = dict()
	output["projects"] = dict()
	dates = []

	jsonfiles = getFilesOfType(location, ".json")

	for f in jsonfiles:
		# print("f:3 ", f[:3])

		if f[:3] != "SUM":
			print("\n+++++++++++++++++++++++++++++++++\n", ">> NEW FILE, filename: ", f)
			with open(f) as file:
				data = json.load(file)
				print("	current file content: ", type(data), json.dumps(data, indent= 4))
				print("processing file...")

				dates.append(data["date"])

				for project in data["projects"]:
					print("	Projectname: ", project, type(project))
	
					# name = str(project)
					# print(name)
					#print("type of data[projects]:", type(data["projects"]))

					h = data["projects"][project]["hours"]
					m = data["projects"][project]["minutes"]
					s = data["projects"][project]["seconds"]

					print("	Times: ",h,"h",m,"m",s,"s")

					if project in output["projects"]:
						print("	>> ...project already exists, adding time")
						output["projects"][project]["hours"] += h
						output["projects"][project]["minutes"] += m
						output["projects"][project]["seconds"] += s

						if output["projects"][project]["seconds"] > 59:
							# print("	seconds / mins was: ", output["projects"][project]["seconds"], "/", output["projects"][project]["minutes"])
							remainder = output["projects"][project]["seconds"] % 60
							output["projects"][project]["minutes"] += (output["projects"][project]["seconds"] - remainder) / 60
							output["projects"][project]["seconds"] = remainder
							# print("	seconds / mins is: ", output["projects"][project]["seconds"], "/", output["projects"][project]["minutes"])

						if output["projects"][project]["minutes"] > 59:
							# print("mins is: ", output["projects"][project]["seconds"], "/", output["projects"][project]["minutes"])
							remainder = output["projects"][project]["minutes"] % 60
							output["projects"][project]["hours"] += (output["projects"][project]["seconds"] - remainder) / 60
							output["projects"][project]["minutes"] = remainder
					else:
						print(">> ...was new project, appending...")
						output["projects"][project] = dict()
						output["projects"][project]["hours"] = h
						output["projects"][project]["minutes"] = m
						output["projects"][project]["seconds"] = s
					print("\n")
		else:
			print(">>>>>>>>>	SUM file, skipping...")

	print("++++  ALL FILES PROCESSED  ++++\n","Output after formatting:", json.dumps(output, indent= 4))
	# print(dates)
	dates.sort()
	print("\ndates of all files:\n", dates)
	time_frame = dates[0] + "-" + dates[len(dates)-1]
	output["timeFrame"] = time_frame

	writeSumJsonFile(output, time_frame)
	moveJsonFilesToNewFolder(time_frame)
	writeTextFile(output, time_frame)


def writeTextFile(data, time_frame):
	name = time_frame + ".txt"

	while True:
		if os.path.exists(os.path.join(target_directory, name)):
			temp = len(name)-4
			name = name[:temp] + "_" + name[temp:]
			print("File already existed. Changed filename to: " + name)
		else:
			print("Writing textfile: " + os.path.join(target_directory, name))
			break

	f = open(os.path.join(target_directory, name), "x")
	f.write("Timeframe: " + time_frame + "\n\n")

	for project in data["projects"]:
		project_name = project
		hours = data["projects"][project]["hours"]
		minutes = data["projects"][project]["minutes"]
		seconds = data["projects"][project]["seconds"]
		# print(str(project))

		f.write("   " + str(project) + ": " + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s" + "\n")

	f.close()


def writeSumJsonFile(output, time_frame):
	global suffix
	name = "SUM_" + time_frame + suffix
	print("\nWriting file....")

	while True:
		if os.path.exists(os.path.join(target_directory, name)):
			temp = len(name)-len(suffix)
			name = name[:temp] + "_" + name[temp:]
			print("	>>File already existed. Changed filename to: " + name)
		else:
			print("...writing '" + name + "'")
			with open(os.path.join(target_directory, name), "w") as file:
				json.dump(output, file, indent=4)
			break

	showinfo("Data Saved", "Saved to: " + str(os.path.join(target_directory, name)))


def moveJsonFilesToNewFolder(time_frame):
	print("")
	print("	>> moving files to new folder:")
	global suffix
	location = target_directory
	newFolderPath = os.path.join(location, time_frame)

	while True:
		if os.path.exists(newFolderPath):
			newFolderPath += "_"
			print(f'		{newFolderPath} existed, changed to: {newFolderPath}')
		else:
			os.makedirs(newFolderPath)
			break

	for file in os.listdir(location):
		if file.endswith(".json"):
			newFilePath = os.path.join(newFolderPath, file)
			original_file_path = os.path.join(location, file)
			print(f'		new File Path: {newFilePath}')

			shutil.move(original_file_path, newFilePath)


root = tk.Tk()
root.resizable(False, False)
root.title("Timer")
# root.wm_attributes("-transparentcolor", 'grey')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#282d3e')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

background = tk.Label(frame) # , image=bg
background.place( x=-50, y=0, width=500, height=1000)

add_timer_button = tk.Button(frame, text="+", font=14, command=addTimer, bg=save_button_color, fg=text_color, bd=1)
add_timer_button.place(x=15, y=12, width=40, height=22)
#add_timer_button.configure(highlightbackground='#06666e', highlightcolor='#06666e')

save_button = tk.Button(frame, text="Save", font=14, command=saveData, bg=save_button_color, fg=text_color,  bd=1)
save_button.place(relx=0.16, y=12, width=60, height=22)

sum_button = tk.Button(frame, text="Sum!", font=14, command=sumJsonFiles, bg=save_button_color, fg=text_color,  bd=1)
sum_button.place(x=340, y=12, width=65, height=22)

file_name = tk.Entry(frame, font=8, bg=save_button_color, fg=text_color, bd=1)
file_name.place(relx=0.33, y=12, width=200, height=22)
file_name.insert(0, str(today)+suffix)


class Timer:
	def __init__(self, parent, row):

		self.seconds, self.mins, self.hours, self.index = 0, 0, 0, row
		# self.y = row / 11 + 0.03 			# 1 / 11 + 0.03 * 500 = 60.4545 pixel
		self.y = 40 * row + offset_from_top
		# self.row = row
		self.parent = parent
		#print(self.y)
		self.running = False

		# self.index_label = tk.Label(self.parent, text=str(self.row), font="Arial 10", width=10, bg=text_color, fg=background_color, bd=0)
		# self.index_label.place(y=self.y, x=col_0-15, relwidth = 0.065, height=22)

		# self.name_label = tk.Entry(self.parent, font=8, bg=background_color, fg=text_color, bd=0)
		# self.name_label.insert(-1, 'Enter name')
		# self.name_label.place(y=self.y, x=col_1, relwidth=0.3, height=22)

		# self.time_label = tk.Label(self.parent, text="0s 0m 0h", font="Arial 14", width=10, bg=text_color, fg=background_color, bd=0)
		# self.time_label.place(y=self.y, x=col_3, relwidth = 0.3, height=22)
		self.makeGUI(row, 'Enter name', '0s 0m 0h')


	def makeGUI(self, row, name, times):
		# print("makeGUI().row = ", row)
		self.y = 40 * row + offset_from_top
		self.row = row
		self.timer_name = name
		self.times = times
		# self.parent = parent

		self.index_label = tk.Label(self.parent, text=str(self.row), font="Arial 10", width=10, bg=text_color, fg=background_color, bd=0)
		self.index_label.place(y=self.y, x=col_0, relwidth = 0.065, height=22)
		
		self.name_label = tk.Entry(self.parent, font=8, bg=background_color, fg=text_color, bd=0)
		self.name_label.insert(-1, self.timer_name)
		self.name_label.place(y=self.y, x=col_1, width=126, height=22)

		self.start_button = tk.Button(self.parent, text=" Start ", font=14, command=self.startTimer, bg=background_color, fg=text_color, bd=0)
		self.start_button.place(y=self.y, x=col_2, width = 60, height=22)

		self.time_label = tk.Label(self.parent, text=self.times, font="Arial 14", width=10, bg=background_color, fg=text_color, bd=0)
		self.time_label.place(y=self.y, x=col_3, width = 114, height=22)

		self.reset_button = tk.Button(self.parent, text="X", font=14, command=self.resetTimer, bg=background_color, fg=text_color, bd=0)
		self.reset_button.place(y=self.y, x=col_4, width=23, height=22)

		self.del_button = tk.Button(self.parent, text="del", font=14, command=self.delete, bg='#690a1c', fg=text_color, bd=0)
		self.del_button.place(y=self.y, x=col_4+26, width=35, height=22)
		# canvas.update()


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
		self.seconds, self.mins, self.hours = 0, 0, 0
		self.time_label.configure(text="0s 0m 0h")


	def delete(self):
		delTimer(self.row)


	def update(self, row):
		self.makeGUI(row, self.name_label.get(), self.time_label.cget("text"))


	def getTime(self):
		return self.name_label.get() + ": " + str(int(self.seconds)) + "s " + str(self.mins) +  "m " + str(self.hours) + "h"


	def getJsonTime(self):
		output = dict()
		output["name"] = self.name_label.get()
		output["hours"] = int(self.hours)
		output["minutes"] = int(self.mins)
		output["seconds"] = int(self.seconds)
		return output

# --------------------------------------------------------------------

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        saved_dir = os.getcwd()
        os.chdir(sys._MEIPASS)
        try:
            main()
        finally:
            os.chdir(saved_dir)
    else:
        main()