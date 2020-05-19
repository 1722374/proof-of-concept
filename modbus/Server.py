#!/usr/bin/env python
"""
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
import random

# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #


def updating_writer(a):
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """
    log.debug("updating the context")
    context = a[0]
    sensor_erdgeschoss = round((random.uniform(20.00, 21.00)),2)  #temperatur_erdgeschoss (2 nachkommastellen)
    add_item_float_16_bit(sensor_erdgeschoss, context=context, address= 0x10)
    sensor_arbeitszimmer = round((random.uniform(22.00, 23.00)),2)  # temperatur_arbeitszimmer
    add_item_float_16_bit(sensor_arbeitszimmer, context=context, address=0x11)



def run_updating_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #



    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17] * 100),
        co=ModbusSequentialDataBlock(0, [17] * 100),
        hr=ModbusSequentialDataBlock(0, [17] * 100),
        ir=ModbusSequentialDataBlock(0, [17] * 100))
    context = ModbusServerContext(slaves=store, single=True)

    #hier werden die Aktoren hinzugefügt
    klingel = 0
    add_item_bit(klingel, context=context, address=0x16, register=3)
    fenster_1, fenster_2, fenster_3 = 0, 0, 0
    add_item_bit(fenster_1, context=context, address=0x20, register= 3)
    add_item_bit(fenster_2, context=context, address=0x21, register= 3)
    add_item_bit(fenster_3, context=context, address=0x22, register= 3)

    #

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    time = 5  # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False)  # initially delay by time
    StartTcpServer(context, address=("localhost", 5020))

#fügt einen Sensor einer Adresse im 4 Register zu
def add_item_float_16_bit(sensor, address, context, slave_id = 0x00, register=4):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder.add_16bit_float(sensor)
    payload = builder.to_registers()
    context[slave_id].setValues(register, address, payload)
    builder.reset()
def add_item_bit(sensor, address, context, slave_id = 0x00, register=4):

    values = [sensor]
    context[slave_id].setValues(register, address,values)


if __name__ == "__main__":
    run_updating_server()