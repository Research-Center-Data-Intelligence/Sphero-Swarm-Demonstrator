from tkinter import *
import spherov3
import threading
import time
import pygame
import time
import math
import asyncio




class ControllerUi:
	def __init__(self):
		self.bolts = []
		self.selected_mac = ""
		self.selected_name = ""
		self.client = ""
		self.speed = 50
		self.run = False
		self.all_bolts = []
		self.current_bolt = ""
		self.current_heading = 0

	def GetClients(self):
		while True:
			try:
				scanner = spherov3.Scanner()
				self.bolts = scanner.discover(debug="readable")
				for bolt in self.bolts:
					if bolt in self.all_bolts:
						pass
					else:
						self.all_bolts.append(bolt)
						self.bolts_list.insert("end", str(bolt))

				time.sleep(20)
			except:
				time.sleep(2)

	def GetSelectBolt(self):
		try:
			selected = ""
			for i in self.bolts_list.curselection():
				selected = self.bolts_list.get(i)

			self.connection_button.config(state=DISABLED)
			self.selected_mac = selected.split(": ")[0].strip()
			self.selected_name = selected.split(": ")[1].strip()
			if self.connection_button['text'] != 'Disconnect': 
				self.current_bolt = self.selected_name
				self.run = True
				self.client = spherov3.spherov3_connector(self.selected_mac)
				self.client.connect()
				self.connection_label['text'] = "Connected: "+self.selected_name
				self.connection_label['fg'] = "green"
				self.connection_button['text'] = 'Disconnect'
				self.connection_button['fg'] = 'red'
				threading.Thread(target=self.Control,args=()).start()
				self.connection_button.config(state=NORMAL)
			else:
				self.connection_button.config(state=NORMAL)
				self.connection_label['text'] = "No Bolts Are Connected"
				self.connection_label['fg'] = 'red'
				self.connection_button['text'] = 'Connect'
				self.connection_button['fg'] = 'black'
				self.speed = 50
				self.run = False
				self.client.roll(0,0)
				self.client.rest_yaw()
				asyncio.run(self.client.CutConnection())
				self.connection_button.config(state=NORMAL)
		except:
			self.connection_button.config(state=NORMAL)
			

	def RunThread(self,target,data=()):
		threading.Thread(target=target,args=data).start()
	def gui(self):
		# create a main windows
		self.frm = Tk()
		self.frm.title("BOLTS UI")
		# change geometry
		self.frm.geometry('400x230')
		# create main frame
		self.main_frame = Frame(self.frm)
		# create bolts label
		self.connection_label = Label(self.main_frame,text="No Bolts Are Connected",fg="red",font='ariel 12')
		# create connect button
		self.connection_button = Button(self.main_frame,text="Connect",font="ariel 12",command=lambda:self.RunThread(self.GetSelectBolt))

		# create a frame contains all bots
		self.bolts_frame = Frame(self.main_frame)
		# create listbox 
		self.bolts_list = Listbox(self.bolts_frame,width=40)

		# create tutorial frame

		self.tutorial_frame = Frame(self.main_frame)
		# create rt frame
		self.rt_frame = Frame(self.tutorial_frame)
		# create rt_label 
		self.rt_label = Label(self.rt_frame,text="RT",bg='green',fg='white')
		# create rt_function label
		self.rt_function_label = Label(self.rt_frame,text="Move forward",fg='black')

		# create rt frame
		self.lb_frame = Frame(self.tutorial_frame)
		# create rt_label 
		self.lb_label = Label(self.lb_frame,text="Joystick",bg='#ccc',fg='white')
		# create rt_function label
		self.lb_function_label = Label(self.lb_frame,text="Steering",fg='black')

		threading.Thread(target=self.GetClients).start()
		self.main_frame.pack()
		self.connection_label.pack()
		self.connection_button.pack()

		self.bolts_frame.pack(side=LEFT)
		self.bolts_list.pack(pady=2)

		self.tutorial_frame.pack(side=RIGHT,anchor='n')
		self.rt_frame.pack(padx=15,pady=10)
		self.rt_label.pack(side=LEFT,padx=1)
		self.rt_function_label.pack(side=RIGHT)

		self.lb_frame.pack(padx=13,pady=10)
		self.lb_label.pack(side=LEFT,padx=1)
		self.lb_function_label.pack(side=RIGHT)


		# mainloop
		self.frm.mainloop()

	def change_speed(self):
		while self.run:
			try:
				speed_input = self.controller.get_axis(5)

				# Normalize speed input
				speed_input = (speed_input + 1) / 2

				# Set speed
				self.speed = int(speed_input * 256)

				time.sleep(0.2)
			except:
				pass

	def get_heading(self, current_heading, x, y):
		if abs(x) <= 0.3 and abs(y) <= 0.3:
			return current_heading
		
		# Turn left or right based on x value
		heading = current_heading + x*10

		# Adjusting for going left to right and forward to backward
		adjusted_heading = heading - 360 * (heading // 360)
		return adjusted_heading
	def Control(self):
		pygame.init()
		#joystick= pygame.joystick.Joystick(0)
		# Initialize the Xbox 360 controller
		self.controller = pygame.joystick.Joystick(0)
		self.controller.init()

		threading.Thread(target=self.change_speed).start()
		try:
			while self.run:
				pygame.event.pump()
				# Get joystick axes values
				x_axis = self.controller.get_axis(0)
				y_axis = self.controller.get_axis(1)

				# Round to 1 decimal place
				x_axis = round(x_axis, 1)
				y_axis = round(y_axis, 1)

				# Get heading in degrees
				self.current_heading = self.get_heading(self.current_heading, x_axis, y_axis)
				# Print heading
				self.client.roll(self.speed,int(self.current_heading))

				self.client.rest_yaw()

		except KeyboardInterrupt:
			pass
		finally:
			pygame.quit()




ControllerAi = ControllerUi()
ControllerAi.gui()

