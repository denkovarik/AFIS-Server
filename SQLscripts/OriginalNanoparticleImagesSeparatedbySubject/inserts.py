import os
from PIL import Image
import pprint

file = open("inserts.sql", "w")


def subjects(subjectID):
    file.write("#------------------------SUBJECT %s------------------------\n" % subjectID)
    file.write("INSERT INTO Subjects\nValues('%s');\n\n" % subjectID)
    


def fingers(subjectID, fingerIndex, handID, fingerID):
    file.write("INSERT INTO Fingers\n")
    file.write("Values(%s, %s, '%s', '%s');\n\n" % (handID, fingerIndex, fingerID, subjectID))
    


def images(imagePath, imageID, fingerID,localImage):
    image = Image.open(localImage)
    a = imagePath
    b = imageID
    c = fingerID
    w, h = image.size
    r = 'NULL'

    file.write("INSERT INTO Images\n")
    file.write("Values('%s', '%s', '%s', %s, %s, %s);\n\n" % (a, b, c, w, h, r))
    image.close
    


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
    finger = 1
    minutiae = 1
    feature = 1
    imagesRoot = '/var/www/server/Datasets/Nanoparticle_Images/images/'
    xytRoot = '/var/www/server/Datasets/Nanoparticle_Images/mindtctOutput/'
    imageLocal = '/home/kbikeguy/Desktop/SDSMT/Fall2020/SeniorDesign/server/MOLF/MindtctOutput/DB1_Lumidgm/'
    xytLocal = '/home/kbikeguy/Desktop/SDSMT/Fall2020/SeniorDesign/server/SQLscripts/OriginalNanoparticleImagesSeparatedbySubject/dataset/mindtctOutput/'
    inserts = 0

    path = '/home/kbikeguy/Desktop/SDSMT/Fall2020/SeniorDesign/server/SQLscripts/OriginalNanoparticleImagesSeparatedbySubject/dataset'

    print("test")
    for root,d_names,f_names in os.walk(path):
        
        #skip outer dir
        if root[-1] not in {'A', 'B', 'C', 'E', 'F', 'I'}:
            continue
        # insert into Subjects table
        subject = root[-1]
        subjects(subject)
        inserts += 1
        imageID = 1

        for name in f_names:
            #insert into Fingers table
            fingerIndex = 'NULL'            
            handID = 'NULL'
            fingerID = subject + '.' + str(finger)
            finger += 1
            fingers(subject, fingerIndex, handID, fingerID)
            inserts += 1            

            #insert into Images table
            imageID = name.split('_')[1].split('.')[0]
            imagePath = imagesRoot + name
            image_id = fingerID + '.' + str(imageID)
            localImage = root + '/' + name 
            images(imagePath, image_id, fingerID, localImage)
            inserts += 1

            #insert into Features table
            xytFile = name[:-3] + 'xyt'
            countPath = xytLocal + xytFile
            xytPath = xytRoot + xytFile
            count = calcCount(countPath)
            featureID = image_id + '.' + str(feature)
            feature += 1
            features(image_id, featureID, count)
            inserts += 1  
            
            #insert into Matutias table
            minutiaeID = featureID + '.' + str(minutiae)
            minutiae += 1
            minutiaes(minutiaeID, featureID, xytPath)
            inserts += 1
        

    """

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
                images(imagePath, imageID, fingerID)
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

    """

if __name__ == "__main__":
# execute only if run as a script
    main()
