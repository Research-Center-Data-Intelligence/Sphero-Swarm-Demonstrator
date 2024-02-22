import spherov3


# define scanner
scanner = spherov3.Scanner()
# show all bolts in the area
scanner.discover()

# define a connector and pass the mac address
connector = spherov3.spherov3_connector("FE:47:FA:CC:4B:05")
#connect the bolt with this mac address : FE:47:FA:CC:4B:05
connected_bolt = connector.connect()
# set speed 50 and go forward
connected_bolt.roll(speed=50,heading=180)
# disconnect
connected_bolt.disconnect()
