import ctypes
from ctypes import WINFUNCTYPE, byref
from ctypes.wintypes import HANDLE, UINT
from time import sleep
from threading import Thread

C_READER = './main.exe'
WINMM = ctypes.windll.winmm

MIM = 0x3C3
CALLBACK_FUNCTION = 0x00030000
CALLBACK_NULL = 0x00000000
UCMAX = 0xFF
STATUS_OKAY = 0
STATUS_ERROR = 1
DEVICE_INPUT = 0
DEVICE_OUTPUT = 1

UCHAR = ctypes.c_ubyte
ULONG = ctypes.c_ulong
MidiInProc = WINFUNCTYPE(None, HANDLE, UINT, ULONG, ULONG, ULONG)
type Switch = list[bool | int]
type DataIO = list[ULONG]
PTR = byref

inputAlive = [True]
outputAlive = [True]
inputData: DataIO = []
outputData: DataIO = []
errorState = [STATUS_OKAY]

def isError(obj: Switch) -> bool: return obj[0]
def isAlive(obj: Switch) -> bool: return obj[0]

def unwrapData(data: int) -> tuple[int, int, int]:
    return (data & UCMAX, (data >> 8) & UCMAX, (data >> 16) & UCMAX)

def wrapData(status: int, note: int, velocity: int) -> ULONG:
    return ULONG(status & UCMAX | (note << 8) & UCMAX | (velocity << 16) & UCMAX)

def __midiCallback(hMidiIn, wMsg, dwInstance, dwParam1, dwParam2):
    if MIM == wMsg:
        inputData.append(dwParam1)
    return STATUS_OKAY

def __inputRead():
    callback = MidiInProc(__midiCallback)
    hMidiIn = HANDLE()
    
    error = WINMM.midiInOpen( PTR(hMidiIn), DEVICE_INPUT, callback, 0, CALLBACK_FUNCTION )
    if error: return error

    WINMM.midiInStart(hMidiIn)
    
    while isAlive(inputAlive) and not isError(errorState):
        sleep(0.2)
    
    WINMM.midiInStop(hMidiIn)
    WINMM.midiInClose(hMidiIn)

def __outputWrite():
    hMidiOut = HANDLE()

    error = WINMM.midiOutOpen( PTR(hMidiOut), DEVICE_OUTPUT, 0, 0, CALLBACK_FUNCTION )
    if error: return error

    while isAlive(outputAlive) and not isError(errorState):
        if not outputData: continue
        data = outputData.pop(0)
        message = data
        WINMM.midiOutShortMsg(hMidiOut, message)
        sleep(0.2)
        
    WINMM.midiOutClose(hMidiOut)

def startIO() -> tuple[Thread, Thread, DataIO, Switch, DataIO, Switch, Switch]:
    inputThread = Thread(target=__inputRead)
    outputThread = Thread(target=__outputWrite)
    return (
        inputThread,
        outputThread,
        inputData,
        inputAlive,
        outputData,
        outputAlive,
        errorState
    )