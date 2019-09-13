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
            if(operation == "help" or operation == "?"):
                printHelp()
            elif(operation == "bootSector"):
                getBootSectorData(hexDump)
            elif(operation == "FAT1"):
                getFATEntries(hexDump, 1)
            elif(operation == "FAT2"):
                getFATEntries(hexDump, 2)
            elif(operation == "exit"):
                exit()
            else:
                print("Unknown command!")
        
def printHelp():
    print("Availibale commands: ")
    print("help       - Print available commands")
    print("?          - Print available commands")
    print("bootSector - Retrive data from boot sector and print")
    print("FAT1       - Print all FAT entries in FAT Table 1")
    print("FAT2       - Print all FAT entries in FAT Table 2")
    print("exit       - Exit program")

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

def getFATEntries(hexDump, FATNumber):
    startOfBootstrapRoutine = hexDump.read(3)
    OEMName = hexDump.read(8)
    bytesPerSector = array.array('h', hexDump.read(2))[0]
    sectorsPerCluster = int(binascii.hexlify(hexDump.read(1)))
    numberOfReservedSectors = array.array('h', hexDump.read(2))[0]
    numberOfFATs = int(binascii.hexlify(hexDump.read(1)))
    maximumNumberOfRootDirectoryEntries = array.array('h', hexDump.read(2))[0]
    totalSectorCount = array.array('h', hexDump.read(2))[0]
    mediaType = hexDump.read(1)
    sectorsPerFAT = array.array('h', hexDump.read(2))[0]
    sectorsPerTrack = array.array('h', hexDump.read(2))[0]
    numberOfHeads = array.array('h', hexDump.read(2))[0]
    numberOfHiddenSectors = array.array('h', hexDump.read(4))[0]
    hexDump.read(6)
    bootSignature = int(binascii.hexlify(hexDump.read(1)))
    volumeId = hexDump.read(4)
    volumeLabel = hexDump.read(11)
    fileSystemType = hexDump.read(8)
    sizeOfTheDevice = 512 * bytesPerSector
    offsetToStartOfFAT1 = 0x200
    #Rest of the boot sector is irrelelevant
    hexDump.read(450)
    #We are now in the beginning of FAT1
    #We have exaclty one entry per cluster
    sector = input("Sector to print(* for all): ")
    if(FATNumber == 1):
        if(sector == "*"):
            for i in range(1, 10):
                print("Sector: " + str(i))
                sector = hexDump.read(bytesPerSector)
                print("-----------------------")
                print(sector)
                print("-----------------------" + "\n")
        else:
            for i in range(1, 10):
                if(i == int(sector)):
                    sectorOrEntries = input("Print entire sector or table entries(sector/entries): ")
                    if(sectorOrEntries == "sector"):
                        print("Sector: " + str(i))
                        sector = hexDump.read(bytesPerSector)
                        print("-----------------------")
                        print(sector)
                        print("-----------------------" + "\n")
                    else:
                        NmbrOfEntris = input("How many entries(* for all): ")
                        counter = 0
                        for i in range(1, int(bytesPerSector)):
                            if(i % 2 ==0):
                                if(NmbrOfEntris == "*"):
                                    # @TODO As we cant divide 512/3 to an integer some data might be missed in the end of the FAT table, we should write logic for handling this.
                                    entry = hexDump.read(3).hex()
                                    entry1 = entry[:int(len(entry)/2)]
                                    entry2 = entry[int(len(entry)/2):]
                                    print("Entry " + str(i - 1) + ": ")
                                    print(entry1)
                                    print("Entry " + str(i) + ": ")
                                    print(entry2)
                                elif(counter == int(NmbrOfEntris)):
                                    break
                                else:
                                    #Since we have 12 bit FAT one entry is 1.5 byte. Therefore we need to read 3 bytes at a time.
                                    entry = hexDump.read(3).hex()
                                    entry1 = entry[:int(len(entry)/2)]
                                    entry2 = entry[int(len(entry)/2):]
                                    print((entry1))
                                    if(entry1 == "FF7"):
                                        print("Entry " + str(i - 1) + " BAD CLUSTER: ")
                                    else:
                                        print("Entry " + str(i - 1) + ": ")
                                    print(entry1)
                                    if(entry2 == "FF7"):
                                        print("Entry " + str(i) + " BAD CLUSTER: ")
                                    else:
                                        print("Entry " + str(i) + ": ")
                                    print(entry2)
                                    counter = counter + 2
                else:
                    #We have to read the sector even though we are not interested of the data in it. 
                    hexDump.read(bytesPerSector)                


    if(FATNumber == 2):
        #Skip FAT1
        hexDump.read(bytesPerSector * 9)
        if(sector == "*"):
            for i in range(1, 10):
                print("Sector: " + str(i))
                sector = hexDump.read(bytesPerSector)
                print("-----------------------")
                print(sector)
                print("-----------------------" + "\n")
        else:
            for i in range(1, 10):
                if(i == int(sector)):
                    print("Entry: " + str(i))
                    entry = hexDump.read(bytesPerSector)
                    print("-----------------------")
                    print(entry)
                    print("-----------------------" + "\n")

#Here we run the program.
main() 
    
    


           