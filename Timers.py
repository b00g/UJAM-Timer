import tkinter as tk
from datetime import datetime

global HEIGHT
global WIDTH
global suffix

HEIGHT = 100
WIDTH = 405
suffix = ".txt"

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

	if name == "":
		name = today
	try:
		f = open(name+suffix, "x")
	except:
		name += "_"
		f = open(name+suffix, "x")

	file_name.delete(0,len(name))
	file_name.insert(0, str(name))

	print("writing file: " + name + suffix)
	print(">>> Timer Data:")

	f.write(today + "\n")

	for obj in timers:
		f.write(" " + str(obj.getTime()) + "\n")
		print(">>> " + obj.getTime())

	f.close()



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
#save_button.configure(highlightbackground='#06666e', highlightcolor='#06666e')

file_name = tk.Entry(frame, font=8, bg=save_button_color, fg=text_color, bd=0)
file_name.place(relx=0.36, y=12, width=240, height=22)
file_name.insert(0, str(today)+suffix)
#file_name.configure(highlightbackground='#06666e', highlightcolor='#06666e')



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



if __name__ == "__main__":
	main()