from bleak import BleakScanner,BleakClient
import sphero_constractors
from colorama import Fore,init
import asyncio
import warnings
import sphero_constractors
from datetime import datetime,timedelta


warnings.simplefilter(action='ignore', category=FutureWarning)

init()
class Scanner:
	def __init__(self):
		self.bolts = []
		self.bolt_str = ""
		self.Retry = 0
	async def Scan(self,debug=None):
		# discover devices that used low energy bluetooth and get only sphero bolts
		devices = await BleakScanner.discover()
		for device in devices:
			# check for sphero bolts
			if 'SB' in str(device):
				if debug == "readable":
					self.bolts.append(str(device).strip())
				else:
					self.bolts.append(str(device).split(": ")[0].strip())
				self.bolt_str+=str(device)+"\n"

		# return all discoverd sphero bolts
		if debug == "bolts" or debug == "readable":
			return self.bolts


		# show how many bolt has been found
		print(f"Total Bolts ({len(self.bolts)}):")
		# show all bolts
		print(self.bolt_str.strip())

	def discover(self,debug=None):
		response = asyncio.run(self.Scan(debug))

		if response:
			return response




class spherov3_connector:
	def __init__(self,mac_address):
		self.mac = mac_address
		self.client = None

	async def ActiveAntiDos(self):
		AntiDOS_characteristic = "00020005-574f-4f20-5370-6865726f2121"

		# active it into the client
		await self.client.write_gatt_char(AntiDOS_characteristic,
		b"usetheforce...band",
		response=True)

	def checkBytes(self,command: list, byte: int) -> list:
		if byte == sphero_constractors.API_CONSTANTS["startOfPacket"]:
			command.extend([
			sphero_constractors.API_CONSTANTS["escape"],
			sphero_constractors.API_CONSTANTS["escapedStartOfPacket"]
			])
			return command

		elif byte == sphero_constractors.API_CONSTANTS["escape"]:
			command.extend([
			sphero_constractors.API_CONSTANTS["escape"],
			sphero_constractors.API_CONSTANTS["escapedEscape"]
			])
			return command

		elif byte == sphero_constractors.API_CONSTANTS["endOfPacket"]:
			command.extend([
			sphero_constractors.API_CONSTANTS["escape"],
			sphero_constractors.API_CONSTANTS["escapedEndOfPacket"]
			])
			return command

		else:
			return command.append(byte)


	async def send(self,characteristic=None, devID=None,
	       commID=None, targetId=None, data=[]):
		"""
		Generate databytes of command using input dictionary
		This protocol copied completely from JS library
		Messages are represented as:
		[start flags targetID sourceID deviceID commandID seqNum data
		checksum end]
		The flags byte indicates which fields are populated.
		The checksum is the ~sum(message[1:-2]) | 0xff.
		"""
		sequence = 0
		sequence = (sequence + 1) % 256
		running_sum = 0
		command = []
		command.append(sphero_constractors.API_CONSTANTS["startOfPacket"])
		if targetId is None:
			cmdflg = (sphero_constractors.FLAGS["requestsResponse"] |
			          sphero_constractors.FLAGS["resetsInactivityTimeout"] |
			          0)
			command.append(cmdflg)
			running_sum += cmdflg
		else:
			cmdflg = (sphero_constractors.FLAGS["requestsResponse"] |
			sphero_constractors.FLAGS["resetsInactivityTimeout"] |
			targetId)
			command.append(cmdflg)
			running_sum += cmdflg
			command.append(targetId)
			running_sum += targetId

		command.append(devID)
		running_sum += devID
		command.append(commID)
		running_sum += commID
		command.append(sequence)
		running_sum += sequence

		if data is not None:
			for datum in data:
			    self.checkBytes(command, datum)
			    running_sum += datum
		checksum = (~running_sum) & 0xff
		self.checkBytes(command, checksum)

		command.append(sphero_constractors.API_CONSTANTS["endOfPacket"])

		await self.client.write_gatt_char(characteristic, bytes(command))

	async def roll_bolt(self,speed: int, heading: int, time: int = None):
		"""        Rolls the device at a specified speed (int between 0 and 255)
		heading (int between 0 and 359) and time (int in seconds).
		Data is format [speed, heading byte 1, heading byte 2,
		direction (0-forward, 1-back)].

		Parameters
		----------
		speed : int
		Speed of the bot.
		heading : int
		Heading of the bot.
		time : int, optional
		Let the bot drive for an amount of time, by default None.
		"""

		if time:
			run_command_till = datetime.now() + timedelta(seconds=time)
			while datetime.now() + timedelta(seconds=1) < run_command_till:
				await self.roll_bolt(speed, heading)
		else:
		# print("[SEND {}] Rolling with speed {} and heading {}".format(
		#     self.sequence, speed, heading))
			await self.send(
		    characteristic=sphero_constractors.APIV2_CHARACTERISTIC,
		    devID=sphero_constractors.DEVICE_ID["driving"],
		    commID=sphero_constractors.DRIVING_COMMAND_IDS["driveWithHeading"],
		    targetId=0x012,
		    data=[speed, (heading >> 8) & 0xff, heading & 0xff, 0]
			)

		# await asyncio.sleep(2)

	async def wake(self):
        # """
        # Bring device out of sleep mode (can only be done if device was in
        # sleep, not deep sleep).\n
        # If in deep sleep, the device should be connected to USB power to wake.
        # """
		print("[SEND {}] Waking".format(0))

		await self.send(
		characteristic=sphero_constractors.APIV2_CHARACTERISTIC,
		devID=sphero_constractors.DEVICE_ID["powerInfo"],
		commID=sphero_constractors.POWER_COMMAND_IDS["wake"],
		data=[])  # empty payload

	async def resetYaw(self):

		await self.send(
		characteristic=sphero_constractors.APIV2_CHARACTERISTIC,
		devID=sphero_constractors.DEVICE_ID["driving"],
		commID=sphero_constractors.DRIVING_COMMAND_IDS["resetYaw"],
		data=[]
		)

	async def EstablishConnection(self):
		for _ in range(3):
			try:
				# define bleak client
				self.client = BleakClient(self.mac)
				# connect using bleak client
				await self.client.connect()
				
				# not connected # show error that connection has failed
				if not self.client.is_connected():
					assert False,f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}] The connection has failed"

				# active antidos on the client block interception
				await self.ActiveAntiDos()

				# wake up the chosen bolt
				await self.wake()

				print(f"[{Fore.GREEN}+{Fore.WHITE}] Connected --> {self.mac}")
				break
			except:
				pass


	async def CutConnection(self):
		await self.client.disconnect()
	def roll(self,speed,heading,sec=None):
		asyncio.run(self.roll_bolt(speed,heading,sec))

	def rest_yaw(self):
		asyncio.run(self.resetYaw())
	def connect(self):
		asyncio.run(self.EstablishConnection())

	def disconnect(self):
		asyncio.run(self.CutConnection())

