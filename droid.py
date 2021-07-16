import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "09b600a0-3e42-41fc-b474-e9c0c8f0c801"
NOTIFY_UUID = "09b600b0-3e42-41fc-b474-e9c0c8f0c801"
WRITE_UUID = "09b600b1-3e42-41fc-b474-e9c0c8f0c801"

def convertBytes( bytes ):
	return bytearray( bytes )

async def run():
	droidCount = 0
	droid = None
	devices = await BleakScanner.discover()
	for d in devices:
		if d.name == "DROID":
			droid = d
			droidCount += 1
	if droidCount > 1:
		print( "Found more than one droid. Using last one in the list." )
	if droidCount == 0:
		print( "No droids detected. Aborting." )
		return
	if droid is not None:
		async with BleakClient( droid.address ) as client:
			try:
				print( "Attempting to connect to droid..." )
				connected = await client.connect()
				if connected:
					print( "Connection established successfully! Writing initial messages..." )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'222001' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'222001' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'222001' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'222001' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'27420f4444001f00' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'27420f4444001802' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'27420f4444001f00' )
					await asyncio.sleep( 1.5 )
					await client.write_gatt_char( WRITE_UUID, b'27420f4444001802' )
					await asyncio.sleep( 2 )

					print( "Successfully wrote initial messages! Attempting to play sound..." )
					await client.write_gatt_char( WRITE_UUID, b'2742 0F44 4400 1803' )
					print( "Successfully played sound!" )
			except KeyboardInterrupt:
				print( "Program stopped by user." )
			except BaseException as e:
				print( "ERROR: {0}".format( e ) )
			finally:
				await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete( run() )
