import asyncio
import keyboard
import random
from bleak import BleakClient, BleakScanner

# UUIDs for the service, notifications, and writing
# Currently, only the write UUID is used
SERVICE_UUID = "09b600a0-3e42-41fc-b474-e9c0c8f0c801"
NOTIFY_UUID = "09b600b0-3e42-41fc-b474-e9c0c8f0c801"
WRITE_UUID = "09b600b1-3e42-41fc-b474-e9c0c8f0c801"

# Instance of the droid connection
CLIENT = None

# It seems that different personalities use different sequences,
# so some sequences won't make the droid play a sound
async def playRandomSound():
	global CLIENT
	soundBanks = ["0", "1", "2", "3", "4", "5", "6", "7", "A"]
	soundCodes = ["0", "1", "2", "3", "4"]
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2742 0F44 4400 1F0" + random.choice( soundBanks ) ) )
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2742 0F44 4400 180" + random.choice( soundCodes ) ) )
	print( "Playing random sound..." )

async def turnRight():
	global CLIENT
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2942 0546 00FF 012C 0000" ) )
	print( "Turning right..." )

async def turnLeft():
	global CLIENT
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2942 0546 01FF 012C 0000" ) )
	print( "Turning left..." )

async def disableMotors():
	global CLIENT
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2942 0546 0000 012C 0000" ) )
	await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "2942 0546 0100 012C 0000" ) )

async def checkForSoundPress():
	while True:
		keyboard.wait( '1' )
		await playRandomSound()
		await asyncio.sleep( 1 )

async def checkForRightPress():
	while True:
		keyboard.wait( 'd' )
		await turnRight()
		await asyncio.sleep( 0.5 )
		await disableMotors()

async def checkForLeftPress():
	while True:
		keyboard.wait( 'a' )
		await turnLeft()
		await asyncio.sleep( 0.5 )
		await disableMotors()

async def connect():
	print( "Scanning for droids..." )
	droidCount = 0
	droid = None
	devices = await BleakScanner.discover( timeout = 10 )
	for d in devices:
		if d.name == "DROID":
			droid = d
			droidCount += 1
	if droidCount > 0:
		print( "Droid found! It's address is " + d.address )
	else:
		print( "No droids detected. Aborting." )
		return
	if droidCount > 1:
		print( "Found more than one droid. Using last one in the list." )
	if droid is not None:
		global CLIENT
		async with BleakClient( droid.address ) as CLIENT:
			try:
				print( "Connecting to droid..." )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "222001" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "222001" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "222001" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "222001" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "27420f4444001f00" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "27420f4444001802" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "27420f4444001f00" ) )
				await asyncio.sleep( 1.5 )
				await CLIENT.write_gatt_char( WRITE_UUID, bytearray.fromhex( "27420f4444001802" ) )
				await asyncio.sleep( 2 )
				print( "Connection to droid established! Droid is ready to accept inputs!" )
				await checkForSoundPress()
				await checkForRightPress()
				await checkForLeftPress()
			except KeyboardInterrupt:
				print( "Program stopped by user." )
			except BaseException as e:
				print( "ERROR: {0}".format( e ) )
			finally:
				await CLIENT.disconnect()
	else:
		print( "ERROR: Droid was found but it's connection somehow isn't valid." )

loop = asyncio.get_event_loop()
loop.run_until_complete( connect() )
