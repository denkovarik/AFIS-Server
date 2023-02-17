file = open("insertDB1.sql", "w")


def subjects(subjectID):
    file.write("#------------------------SUBJECT %s------------------------\n" % subjectID)
    file.write("INSERT INTO Subjects\nValues('%s');\n\n" % subjectID)
    


def fingers(subjectID, fingerIndex, handID, fingerID):
    a = handID
    b = fingerIndex
    c = fingerID
    d = subjectID
    file.write("INSERT INTO Fingers\nValues(%s, %s, '%s', '%s');\n\n" % (a, b, c, d))
    


def images(imagePath, imageID, fingerID, width, height, res):
    a = imagePath
    b = imageID
    c = fingerID
    d = width
    e = height
    f = res
    file.write("INSERT INTO Images\n")
    file.write("Values('%s', '%s', '%s', %s, %s, %s);\n\n" % (a, b, c, d, e, f))
    


def features(imageID, featureID, count):
    file.write("INSERT INTO Features\n")
    file.write("Values('%s', '%s', %s);\n\n" % (imageID,featureID, count))
    


def minutiaes(minutiaeID, featureID, xytPath):
    file.write("INSERT INTO Minutiaes\n")
    file.write("Values('%s', '%s', '%s');\n\n" % (minutiaeID,featureID, xytPath))
    


def sweatpores():
    pass


def buildFile(subject, finger, image, ext):
    return str(subject) + '_' + str(finger) + '_' + str(image) + ext

def calcCount(xytPath):
    xytFile = open(xytPath, 'r')
    count = 0
    for line in xytFile:
        count += 1

    xytFile.close()

    return count



def main():
    
    subjectMax = 100
    imageMax = 4
    fingerMax = 10
    width = '352'
    height = '544' 
    res = '500'
    imagesRoot = '/var/www/server/Datasets/MOLF/OriginalDataset/DB1_Lumidgm/'
    xytRoot = '/var/www/server/Datasets/MOLF/MindtctOutput/DB1_Lumidgm/'
    countRoot = '/home/kbikeguy/Desktop/SDSMT/Fall2020/SeniorDesign/server/MOLF/MindtctOutput/DB1_Lumidgm/'

    inserts = 0

    for subject in range(1, subjectMax + 1):

        # insert into Subjects table
        subjects(subject)
        inserts += 1

        for finger in range(1, fingerMax + 1):

            #insert into Fingers table
            handID = 'NULL'
            fingerID = str(subject) + '.' + str(finger)
            fingers(subject, finger, handID, fingerID)
            inserts += 1

            for image in range(1, imageMax + 1):

                #insert into Images table
                imagePath = imagesRoot + buildFile(subject, image, finger, '.wsq')
                imageID = fingerID + '.' + str(image)
                images(imagePath, imageID, fingerID, width, height, res)
                inserts += 1

                #insert into Features table
                xytFile = buildFile(subject, image, finger, '.xyt')
                countPath = str(countRoot) + xytFile
                xytPath = str(xytRoot) + xytFile
                count = calcCount(countPath)
                featureID = imageID + '.1'
                features(imageID, featureID, count)
                inserts += 1

                #insert into Matutias table
                minutiaeID = featureID + '.1'
                minutiaes(minutiaeID, featureID, xytPath)
                inserts += 1

    print(inserts, "insert statements were written")
    file.close()


if __name__ == "__main__":
# execute only if run as a script
    main()
