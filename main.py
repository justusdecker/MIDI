import subprocess
from subprocess import PIPE, Popen
import time
import os
import signal
from os.path import abspath, isfile
import ctypes
from ctypes import wintypes

C_READER = './main.exe'
WINMM = ctypes.windll.winmm
MIM = 0x3C3
CALLBACK_FUNCTION = 0x00030000
CALLBACK_NULL = 0x00000000
UCHAR = ctypes.c_ubyte

def midi_callback(hMidiIn, wMsg, dwInstance, dwParam1, dwParam2):
    if MIM == wMsg:
        status = dwParam1 & 0xFF
        data1 = (dwParam1 >> 8) & 0xFF
        data2 = (dwParam1 >> 16) & 0xFF
        print(f"Event: Status={hex(status)}, Data1={data1}, Data2={data2}")
    return 0

MidiInProc = ctypes.WINFUNCTYPE(None, wintypes.HANDLE, wintypes.UINT, 
                                ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong)
def getMidiValues():
    callback = MidiInProc(midi_callback)

    hMidiIn = wintypes.HANDLE()
    device_id = 0

    result = WINMM.midiInOpen(
        ctypes.byref(hMidiIn),
        device_id,
        callback,
        0,
        CALLBACK_FUNCTION
    )
    
    if not result:
        print('Started MIDI-Receiver')
        WINMM.midiInStart(hMidiIn)
    
    while 1:
        input('ENTER TO STOP')
        break
    
    WINMM.midiInStop(hMidiIn)
    WINMM.midiInClose(hMidiIn)
    print("closed connection")



def setLED():
    hMidiOut = wintypes.HANDLE()
    device_id = 1
    
    result = WINMM.midiOutOpen(
        ctypes.byref(hMidiOut),
        device_id,
        0,
        0,
        CALLBACK_FUNCTION
    )

    if result == 0:
        while 1:

            inp = input('ENTER [STATUS] [NOTE] [ON/OFF]')
            if inp == 'exit': break

            try:
                
                status, note, velocity = map(int, inp.split(' '))
                message = ctypes.c_ulong(status | (note << 8) | (velocity << 16))
                print(message)
            except Exception as e: 
                print(e)
                continue
            
            WINMM.midiOutShortMsg(hMidiOut, message)
        WINMM.midiOutClose(hMidiOut)
    else:
        print(result)
        print('Something went wrong')
a = 0x96
#8351894
if __name__ == '__main__':
    setLED()