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
    sensor_erdgeschoss = random.randint(2000, 2100) #temperatur_erdgeschoss (2 nachkommastellen)
    add_item(sensor_erdgeschoss, context=context, register= 4, address= 0x10)
    sensor_arbeitszimmer = random.randint(2200, 2300)  # temperatur_arbeitszimmer
    add_item(sensor_arbeitszimmer, context=context, register=4, address=0x11)



def run_modbus_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    print("Starte Modbus Server....")


    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17] * 100),
        co=ModbusSequentialDataBlock(0, [17] * 100),
        hr=ModbusSequentialDataBlock(0, [17] * 100),
        ir=ModbusSequentialDataBlock(0, [17] * 100))
    context = ModbusServerContext(slaves=store, single=True)

    #hier werden die Aktoren hinzugefügt
    jalousie_erdgeschoss = 100
    add_item(jalousie_erdgeschoss, context=context, address=0x16, register=3)
    fenster_1, fenster_2, fenster_3 = 0, 0, 0
    add_item(fenster_1, context=context, address=0x20, register= 3)
    add_item(fenster_2, context=context, address=0x21, register= 3)
    add_item(fenster_3, context=context, address=0x22, register= 3)

    #

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    time = 5  # 5 seconds delay
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False)  # initially delay by time
    StartTcpServer(context, address=("localhost", 5020))

def add_item(sensor, register, address, context, slave_id = 0x00):

    values = [sensor]
    context[slave_id].setValues(register, address,values)

if __name__ == "__main__":
    run_modbus_server()