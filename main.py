from midi_access import startIO, unwrapData, ULONG, wrapData, sleep


while 1:
    threadIn, threadOut, dataIn, aliveIn, dataOut, aliveOut, error = startIO()
    threadIn.start()
    threadOut.start()
    if dataIn:
        data = dataIn.copy()
        dataIn = dataIn.clear()
        
        print(data)
    try:
        d = 0x97
        #inp = input('ENTER STR: [0x90[151], 111, 127]')
        #status, note, velocity = map(int, inp.split(' '))
        status, note, velocity = 151, 112, 127
        message = wrapData(status, note, velocity)
        dataOut.append(message)
        #print(message)
        sleep(0.2)
    except Exception as e: 
        print(e)
        continue