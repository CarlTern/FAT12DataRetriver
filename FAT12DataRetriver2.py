import binascii
import array

def main():
    print("Welcome to floppyDiskDataRetriver!")
    while(True):
        path = input("Enter relative path to FAT12 image file:")
        if (path==''):
            path = './image.dat'
        while(True):
            hexDump = open(path, "rb")
            operation = input("Enter operation: ")
            if(operation == "bootSector"):
                getBootSectorData(hexDump)
            elif(operation == "FAT1"):
                getFATEntries(hexDump)
            elif(operation == "data"):
                getData(hexDump)
            elif(operation == "exit"):
                exit()
            else:
                print("Unknown command!")


def getBootSectorData(hexDump):
    print("Boot sector:" + "\n")
    startOfBootstrapRoutine = hexDump.read(3)
    print("Start of bootstrap routine: " + str(startOfBootstrapRoutine))
    OEMName = hexDump.read(8)
    print("OEM name: " + str(OEMName))
    bytesPerSector = array.array('h', hexDump.read(2))[0]
    print("Bytes per sector: " + str(bytesPerSector))
    sectorsPerCluster = int(binascii.hexlify(hexDump.read(1)))
    print("Sectors per cluster: " + str(sectorsPerCluster))
    numberOfReservedSectors = array.array('h', hexDump.read(2))[0]
    print("Number of Reserved sectors: " + str(numberOfReservedSectors))
    numberOfFATs = int(binascii.hexlify(hexDump.read(1)))
    print("Number of FATs: " + str(numberOfFATs))
    maximumNumberOfRootDirectoryEntries = array.array('h', hexDump.read(2))[0]
    print("Max number of RootDir Entries: " + str(maximumNumberOfRootDirectoryEntries))
    totalSectorCount = array.array('h', hexDump.read(2))[0]
    print("Total sector count: " + str(totalSectorCount))
    mediaType = hexDump.read(1)
    print("Media type: " + str(mediaType))
    sectorsPerFAT = array.array('h', hexDump.read(2))[0]
    print("Sectors per FAT: " + str(sectorsPerFAT))
    sectorsPerTrack = array.array('h', hexDump.read(2))[0]
    print("Sectors per Track: " + str(sectorsPerTrack))
    numberOfHeads = array.array('h', hexDump.read(2))[0]
    print("Number of heads: " + str(numberOfHeads))
    numberOfHiddenSectors = array.array('h', hexDump.read(4))[0]
    print("Number of hidden sectors: " + str(numberOfHiddenSectors))
    hexDump.read(6)
    bootSignature = int(binascii.hexlify(hexDump.read(1)))
    print("bootSignature: " + str(bootSignature))
    volumeId = hexDump.read(4)
    print("VolumeId: " + str(volumeId))
    volumeLabel = hexDump.read(11)
    print("VolumeLabel: " + str(volumeLabel))
    fileSystemType = hexDump.read(8)
    print("File system type: " + str(fileSystemType))
    sizeOfTheDevice = 512 * bytesPerSector
    print("Size of device: " + str(sizeOfTheDevice) + " Bytes")
    offsetToStartOfFAT1 = 0x200
    print("Offset to start FATs: " + str(offsetToStartOfFAT1))
    #Rest of the boot sector is irrelelevant
    hexDump.read(450)

def getFATEntries(hexDump):
    bootSector = hexDump.read(512)
    #We are now in the beginning of FAT1
    #We have exaclty one entry per cluster
    for i in range(0, 200):
        if(i%2 == 0):
            #Since we have 12 bit FAT one entry is 1.5 byte. Therefore we need to read 3 bytes at a time.
            entry = hexDump.read(3).hex()
            dataSector = 33 + i - 2 
            entry1 = str(i) + ": 0x" + entry[3] + entry[0] + entry[1]
            print(entry1)
            entry2 = str(i+1) + ": 0x" + entry[4] + entry[5] + entry[2]
            print(entry2)

def getDataRecursivly(hexDump, counter):
    if(counter == 16):
        exit()
    #tempHex = hexDump
    #unused or empty directory
    indentifier = hexDump.read(1).hex()
    if( indentifier == "00"):
        hexDump.read(31)
        counter = counter + 1
        getDataRecursivly(hexDump, counter)
    elif(indentifier == "e5"):
        fileName = hexDump.read(10).hex()
        fileName = bytes.fromhex(fileName).decode('utf-8')
        print("filename: " + str(fileName))
    else:
        fileName = indentifier + hexDump.read(10).hex() 
        fileName = bytes.fromhex(fileName).decode('utf-8')
        print("filename: " + str(fileName))
    fileAttributes = hexDump.read(1).hex()
    fileAttributes = bin(int(fileAttributes, 16))[2:].zfill(8)
    print("File attributes: " + str(fileAttributes))
    WinNTReserved = hexDump.read(1)
    creationMillsecondStamp = hexDump.read(1).hex()
    creationMillsecondStamp = int(bin(int(creationMillsecondStamp, 16))[2:].zfill(8),2)
    creationTime = getCorrectDateAndTimeFormat(hexDump)
    creationTimeHourInt = int(creationTime[:-11],2)
    creationTimeMinuteInt = int(creationTime[5:-5],2)
    creationTimeSecondInt = int(creationTime[11:],2)*2
    creationDate = getCorrectDateAndTimeFormat(hexDump)
    creationDateYearInt = int(creationDate[:-9],2)
    creationDateMonthInt = int(creationDate[7:-5],2)
    creationDateDayInt = int(creationDate[11:],2)
    print("Date: " + str(creationDateDayInt) + "/" + str(creationDateMonthInt) + "/" + str(creationDateYearInt + 1980) +  "\t" + "Time: " + str(creationTimeHourInt) + ":" + str(creationTimeMinuteInt) + ":" + str(creationTimeSecondInt) + "\t" + "ms: " + str(creationMillsecondStamp))
    lastAccessDate = getCorrectDateAndTimeFormat(hexDump)
    lastAccessDateYearInt = int(lastAccessDate[:-9],2)
    lastAccessDateMonthInt = int(lastAccessDate[7:-5],2)
    lastAccessDateDayInt = int(lastAccessDate[11:],2)
    print("Last access date: " + str(lastAccessDateDayInt) + "/" + str(lastAccessDateMonthInt) + "/" + str(lastAccessDateYearInt + 1980))
    ReservedForFAT32 = hexDump.read(2)
    lastWriteTime = getCorrectDateAndTimeFormat(hexDump)
    lastWriteTimeHourInt = int(lastWriteTime[:-11],2)
    lastWriteTimeMinuteInt = int(lastWriteTime[5:-5],2)
    lastWriteTimeSecondInt = int(lastWriteTime[11:],2)*2
    lastWriteDate = getCorrectDateAndTimeFormat(hexDump)
    lastWriteDateYearInt = int(lastWriteDate[:-9],2)
    lastWriteDateMonthInt = int(lastWriteDate[7:-5],2)
    lastWriteDateDayInt = int(lastWriteDate[11:],2)
    print("Last Write date: " + str(lastWriteDateDayInt) + "/" + str(lastWriteDateMonthInt) + "/" + str(lastWriteDateYearInt + 1980) +  "\t" + "Last Write Time: " + str(lastWriteTimeHourInt) + ":" + str(lastWriteTimeMinuteInt) + ":" + str(lastWriteTimeSecondInt))
    firstLogicalClusterOfFile = array.array('h', hexDump.read(2))[0]
    print("First logical cluster file: " + str(firstLogicalClusterOfFile))
    fileSizeinBytes = array.array('h', hexDump.read(4))[0]
    print("File size: " + str(fileSizeinBytes) + " bytes")
    print("--------------------------------")
    counter = counter + 1 
    getDataRecursivly(hexDump, counter)

def getCorrectDateAndTimeFormat (hexDump):
    var = hexDump.read(2).hex()
    var = bin(int(var, 16))[2:].zfill(8)
    #var = var[::-1] #toBigEndian
    if (len(var)!=16):
        numberOfAdded = 16 - len(var)
        for i in range(0, numberOfAdded):
            var = '0' + var 
    var1 = var[8:]
    var2 = var[:8]
    var = var1 + var2
    return var

def getData(hexDump):
    bootSector = hexDump.read(512)
    FAT1 = hexDump.read(512 * 9)
    FAT2 = hexDump.read(512 * 9)
    rootDirOffset = 0x2600

    fileName = hexDump.read(11)
    print("\n" + "Root Directory:")
    print("filename: " + str(fileName))
    fileAttributes = hexDump.read(1).hex()
    fileAttributes = bin(int(fileAttributes, 16))[2:].zfill(8)
    print("File attributes: " + str(fileAttributes))
    WinNTReserved = hexDump.read(1)
    creationMillsecondStamp = hexDump.read(1)
    creationTime = array.array('h', hexDump.read(2))[0]
    creationDate = array.array('h', hexDump.read(2))[0]
    print("Date: " + str(creationDate) + "\t" + "Time: " + str(creationTime) + "\t" + "ms: " + str(creationMillsecondStamp))
    lastAccessDate = array.array('h', hexDump.read(2))[0]
    print("Last access data: " + str(lastAccessDate))
    ReservedForFAT32 = hexDump.read(2)
    lastWriteTime = array.array('h', hexDump.read(2))[0]
    lastWriteDate = array.array('h', hexDump.read(2))[0]
    print("Last Write date and time" + str(lastWriteDate) + " : " + str(lastWriteTime))
    firstLogicalClusterOfFile = array.array('h', hexDump.read(2))[0]
    print("First logical cluster file: " + str(firstLogicalClusterOfFile))
    fileSizeinBytes = array.array('h', hexDump.read(4))[0]
    print("File size: " + str(fileSizeinBytes) + " bytes")
    print("--------------------------------")

    getDataRecursivly(hexDump, 1)
    #Root directory begin. 

#Here we run the program.
main() 
    
    


           