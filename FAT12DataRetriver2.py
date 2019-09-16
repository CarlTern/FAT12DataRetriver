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
                bootSector = hexDump.read(512)
                FAT1 = hexDump.read(512 * 9)
                FAT2 = hexDump.read(512 * 9)
                rootDirOffset = 0x2600
                getDataRecursivly(224, '', hexDump, 0)
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

def getDataRecursivly(entries, parentFileName, hexDump, counter):
    dirHasContent = False
    if(counter == entries):
        return True
    #tempHex = hexDump
    #unused or empty directory
    indentifier = hexDump.read(1).hex()
    if( indentifier == "00"):
        hexDump.read(31)
        counter = counter + 1
        getDataRecursivly(entries, '', hexDump, counter)
        return
    elif(indentifier == "e5"):
        print("Parent: " + parentFileName)
        fileName = hexDump.read(10).hex() 
        fileName = bytes.fromhex(fileName).decode('utf-8')
        print("filename(Deleted): " + str(fileName))
    else:
        print("Parent: " + parentFileName)
        fileName = indentifier + hexDump.read(10).hex() 
        fileName = bytes.fromhex(fileName).decode('utf-8') 
        print("filename: " + str(fileName))
    fileAttributes = hexDump.read(1).hex()
    fileAttributes = bin(int(fileAttributes, 16))[2:].zfill(8)
    fileAttributes = str(fileAttributes)
    print("File attributes: " + str(fileAttributes))
    fileAttributes = fileAttributes[2:]
    if(fileAttributes[2:] == "1111"):
        print("File is on long file format")
    else:
        if(fileAttributes[4]== "1"):
            print("File is hidden.")
        if(fileAttributes[3] == "1"):
            print("The file is a system file.")
        if(fileAttributes[2] == "1"):
            print("The directory entry contains a volume label.")
        if(fileAttributes[1] == "1"):
            print("The entry represents a directory (not a file).") 
            if( not (fileName[0] == '.' or fileName[0] == '..')):
                dirHasContent = True
        if(fileAttributes[0] == "1"):
            print("File is archived")
    WinNTReserved = hexDump.read(1)
    creationMillsecondStamp = hexDump.read(1)
    creationTime = hexDump.read(2)
    creationDate = array.array('h', hexDump.read(2))[0]
    print("Date: " + str(creationDate) + "\t" + "Time: " + str(creationTime) + "\t" + "ms: " + str(creationMillsecondStamp))
    lastAccessDate = array.array('h', hexDump.read(2))[0]
    print("Last access date: " + str(lastAccessDate))
    ReservedForFAT32 = hexDump.read(2)
    lastWriteTime = array.array('h', hexDump.read(2))[0]
    lastWriteDate = array.array('h', hexDump.read(2))[0]
    print("Last Write date and time: " + str(lastWriteDate) + " : " + str(lastWriteTime))
    firstLogicalClusterOfFile = array.array('h', hexDump.read(2))[0]
    print("First logical cluster file: " + str(firstLogicalClusterOfFile))
    fileSizeinBytes = hexDump.read(4).hex()
    fileSizeinBytes = fileSizeinBytes[::-1]
    fileSizeinBytes = int(fileSizeinBytes, 16)
    print("File size: " + str(fileSizeinBytes) + " bytes")
    print("--------------------------------")
    if(dirHasContent):
        firstLogicalClusterOfFile = 33 + firstLogicalClusterOfFile - 2
        newHexDump = open("./image.dat", "rb")
        newHexDump.read(firstLogicalClusterOfFile * 512)
        #we are in begining of right cluster
        getDataRecursivly(16, fileName, newHexDump, 0)
    counter = counter + 1
    getDataRecursivly(entries, parentFileName, hexDump, counter)

#Here we run the program.
main() 
    
    


           