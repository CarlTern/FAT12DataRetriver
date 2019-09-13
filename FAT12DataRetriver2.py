import binascii
import array

def main():
    print("Welcome to floppyDiskDataRetriver!" + "\n")
    while(True):
        path = input("Enter relative path to FAT12 image file:" + "\n")
        if (path==''):
            path = './image.dat'
        while(True):
            hexDump = open(path, "rb")
            operation = input("Enter operation: ")
            if(operation == "bootSector"):
                getBootSectorData(hexDump)
            elif(operation == "FAT1"):
                getFATEntries(hexDump)
            elif(operation == "FAT2"):
                getFATEntries(hexDump, 2)
            elif(operation == "exit"):
                exit()
            else:
                print("Unknown command!")


def getBootSectorData(hexDump):
    print("Boot sector:" + "\n")
    startOfBootstrapRoutine = hexDump.read(3)
    print("Start of bootstrap routine: " + str(startOfBootstrapRoutine) + "\n")
    OEMName = hexDump.read(8)
    print("OEM name: " + str(OEMName) + "\n")
    bytesPerSector = array.array('h', hexDump.read(2))[0]
    print("Bytes per sector: " + str(bytesPerSector) + "\n")
    sectorsPerCluster = int(binascii.hexlify(hexDump.read(1)))
    print("Sectors per cluster: " + str(sectorsPerCluster) + "\n")
    numberOfReservedSectors = array.array('h', hexDump.read(2))[0]
    print("Number of Reserved sectors: " + str(numberOfReservedSectors) + "\n")
    numberOfFATs = int(binascii.hexlify(hexDump.read(1)))
    print("Number of FATs: " + str(numberOfFATs) + "\n")
    maximumNumberOfRootDirectoryEntries = array.array('h', hexDump.read(2))[0]
    print("Max number of RootDir Entries: " + str(maximumNumberOfRootDirectoryEntries) + "\n")
    totalSectorCount = array.array('h', hexDump.read(2))[0]
    print("Total sector count: " + str(totalSectorCount) + "\n")
    mediaType = hexDump.read(1)
    print("Media type: " + str(mediaType) + "\n")
    sectorsPerFAT = array.array('h', hexDump.read(2))[0]
    print("Sectors per FAT: " + str(sectorsPerFAT) + "\n")
    sectorsPerTrack = array.array('h', hexDump.read(2))[0]
    print("Sectors per Track: " + str(sectorsPerTrack) + "\n")
    numberOfHeads = array.array('h', hexDump.read(2))[0]
    print("Number of heads: " + str(numberOfHeads) + "\n")
    numberOfHiddenSectors = array.array('h', hexDump.read(4))[0]
    print("Number of hidden sectors: " + str(numberOfHiddenSectors) + "\n")
    hexDump.read(6)
    bootSignature = int(binascii.hexlify(hexDump.read(1)))
    print("bootSignature: " + str(bootSignature) + "\n")
    volumeId = hexDump.read(4)
    print("VolumeId: " + str(volumeId) + "\n")
    volumeLabel = hexDump.read(11)
    print("VolumeLabel: " + str(volumeLabel) + "\n")
    fileSystemType = hexDump.read(8)
    print("File system type: " + str(fileSystemType) + "\n")
    sizeOfTheDevice = 512 * bytesPerSector
    print("Size of device: " + str(sizeOfTheDevice) + " Bytes" + "\n")
    offsetToStartOfFAT1 = 0x200
    print("Offset to start FATs: " + str(offsetToStartOfFAT1) + "\n")
    #Rest of the boot sector is irrelelevant
    hexDump.read(450)
    #We are now in the beginning of FAT1
    FAT1 = hexDump.read(bytesPerSector * 9)
    #print(FAT1)
    #We are now in the beginning of FAT2
    offsetToStartOfFAT2 = 0x400
    FAT2 = hexDump.read(bytesPerSector * 9)
    #We are in the beginning of root directory.
    rootDirectoryOffset = 0x600
    #The root directory has a finite size (For FAT12, 14 sectors * 16 directory entries per sector = 224 possible entries
    
    # nmbOfBytesToGet = int((bytesPerSector * maximumNumberOfRootDirectoryEntries) / 16)
    # rootDirectory = hexDump.read(nmbOfBytesToGet)
    # print(rootDirectory)
    # fileName = hexDump.read(8)
    # print(fileName)
    # extension = hexDump.read(3)
    # print(extension)
    
    #print(rootDirectory)
    #We are in the beginning of the data ares.
    offseToDataArea = 0x2200

def getFATEntries(hexDump):
    bootSector = hexDump.read(512)
    #We are now in the beginning of FAT1
    #We have exaclty one entry per cluster
    for i in range(0, 100):
            #Since we have 12 bit FAT one entry is 1.5 byte. Therefore we need to read 3 bytes at a time.
            entry = hexDump.read(3).hex()
            entry1 = "0x" + entry[3] + entry[0] + entry[1]
            if(entry1 == "0xff7"):
                print(entry1 + " : BAD CLUSTER")
            else:
                print(entry1)
            entry2 = "0x" + entry[5] + entry[4] + entry[2]
            if(entry2 == "0xff7"):
                print(entry2 + " : BAD CLUSTER")
            else:
                print(entry2)
                   
#Here we run the program.
main() 
    
    


           