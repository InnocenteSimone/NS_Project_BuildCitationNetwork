#Add the missing tag to the JOI file
def addPublicationYear():
    with open('JOI_WOD_CORD.txt','r',encoding='utf8') as f1, open('JOI.txt','w',encoding='utf8') as newfile:
        c = 0
        for count,line in enumerate(f1):
            if line[0] == "P" and line[1]=="Y":
                c+=1
            if line == "ER\n":
                if c == 0:
                    newfile.write("PY 2019\n")
                c = 0
            newfile.write(line)
            
    f1.close()
    newfile.close()

#Concatenate the JOI from Web Of Science with the JOI from CORD_19
def addCordToJOI():
    with open('JOI_old.txt','r',encoding='utf8') as f1, open('JOI_CORD.txt','r',encoding='utf8') as cord19,open('JOI_WOD_CORD.txt','w',encoding='utf8') as newa:
        lines = f1.readlines()
        lines = lines[:-1]

        cord_lines = cord19.readlines()
        lines.append(cord_lines)
        lines.append("EF\n")

        for line in lines:
            newa.writelines(line)

#Concatenate the different JOI of each paper in one unique JOI file
def concatenateJOI_Cord():
    with open('JOI_CORD.txt','w',encoding='utf8') as newjoi:
        for i in range(1,10):
            file = open(f'records_cord_paper/savedrecs_CORD{i}.txt','r',encoding='utf8') 
            lines = file.readlines()[2:]
            lines = lines[:-1]

            newjoi.writelines(lines)

            file.close()

if __name__ == '__main__':
    concatenateJOI_Cord()
    addCordToJOI()
    addPublicationYear()
