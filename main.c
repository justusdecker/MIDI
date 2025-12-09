#include <windows.h>
#include <mmsystem.h>
#include <stdio.h>

UINT MIM = 0x3C3;


void CALLBACK midiInProc(HMIDIIN hMidiIn, UINT wMsg, DWORD_PTR dwInstance, DWORD_PTR dwParam1, DWORD_PTR dwParam2) {
    if (MIM == wMsg) {
        UINT status = dwParam1 & 0xFF;
        UINT data1 = (dwParam1 >> 8) & 0xFF;
        UINT data2 = (dwParam1 >> 16) & 0xFF;
        printf("Message: status=0x%x, data1=%d, data2=%d\n", status, data1, data2);
    }
    
};

int getMidiValues() {

    UINT deviceID = 0;

    HMIDIIN hMidiIn;
    MMRESULT result;

    result = midiInOpen(
        &hMidiIn,
        deviceID,
        (DWORD_PTR)midiInProc,  // pointer to the function
        0,                      // Userdata?= 0
        CALLBACK_FUNCTION);     // We give a function
    
    if (result != MMSYSERR_NOERROR) {
        printf("An error occurred, (Code: %u)\n", result);
        return 1;
    }

    midiInStart(hMidiIn);
    printf("Started MIDI-Receiver");
    
    char input_char;
    while (scanf(" %c", &input_char) && input_char != 'q');

    midiInStop(hMidiIn);
    midiInClose(hMidiIn);
    printf("closed connectection");
    return 0;
}

int setLED() {
    HMIDIOUT hMidiOut;
    MMRESULT result;

    UINT deviceID = 1;
    result = midiOutOpen(&hMidiOut, deviceID, 0, 0, CALLBACK_NULL);
    
    if (result != MMSYSERR_NOERROR) {
        printf("An error occurred, (Code: %u)\n", result);
        return 1;
    }
    for (int j = 0x90;j<0x98;j++) {
        for (int i = 0; i<128; i++) {
            UCHAR status = j;
            UCHAR note = i;
            UCHAR velocity = 127;

            DWORD messageOn = status | (note << 8) | (velocity << 16);
            midiOutShortMsg(hMidiOut, messageOn);
            printf("%x %u\n",j,i);
            Sleep(150);
            velocity = 0;
            DWORD messageOff = status | (note << 8) | (velocity << 16);
            midiOutShortMsg(hMidiOut, messageOff);
       }
    }
    midiOutClose(hMidiOut);
    
    
    
}

int main() {
    UINT numDevs = midiInGetNumDevs();
    
    if (numDevs == 0) {
        printf("Cannot find any Devices\n");
        return 1;
    } else {
        printf("Found MIDI: INPUT-DEVICES: %u\n", numDevs);
    }
    setLED();
    //getMidiValues();
    return 0;
}