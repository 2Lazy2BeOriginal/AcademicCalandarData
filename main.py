from selenium import webdriver
from selenium.webdriver.common.by import By

# Function declerations
def removeNewLine(file):
    return [line.replace('\n', '') for line in file]

# get all the faculties
with open('test.txt', 'r') as f:
    faculty = f.readlines()
faculty = removeNewLine(faculty)

# Rady Faculty is an annoying exception
with open('RadyFaculty', 'r') as f:
    rFaculty = f.readlines()
rFaculty = removeNewLine(rFaculty)
# Collect all the course codes and put into a new file
courseCodes = open("output.txt", "w")


Web = webdriver.Chrome()

def mainLoop(site, fac):
    # open the main website
    Web.get(site)
    # the first div corresponds to the department and starts with 2
    departmentNumber = 2
    # second is the specific course
    # edge case for asper where actuary is counted twice
    if (fac == "science"):
        courseNumber = 2
    else:
        courseNumber = 1
    # no department has more than 50 so its a safe cap
    while departmentNumber < 50:
            # we know we gone through all the courses if it returns an empty array.
            # This is non empty to start the loop
            codeList = ["x"]
            while len(codeList) != 0:
                # xpath slightly differs between law and music
                if fac == "law" or fac == "music" or fac == "social-work":
                    xPath = '//*[@id="coursestextcontainer"]/div/div[{}]/div[1]/span[1]'
                    xPath = xPath.format(courseNumber)
                    # only one department so automatically break with this condition
                    departmentNumber = 60
                else:
                    xPath = '//*[@id="coursestextcontainer"]/div[{}]/div[{}]/div[1]/span[1]'
                    xPath = xPath.format(departmentNumber, courseNumber)
                    # want to break out of the loop since it is only one department
                # will return 1 if there is something, empty if it doesn'rt exist
                codeList = Web.find_elements(By.XPATH, xPath)
                for c in codeList:
                    # write to a text file
                    if len(c.text) != 0:
                        courseCodes.write("{} {}\n".format(c.text, fac))
                    print(c.text)
                courseNumber += 1
            # reset the loop
            departmentNumber += 1
            courseNumber = 1

for x in faculty:
    website = 'https://catalog.umanitoba.ca/undergraduate-studies/' + x + '/#coursestext'
    mainLoop(website, x)
for x in rFaculty:
    website = ('https://catalog.umanitoba.ca/undergraduate-studies/health-sciences/'
               + x +
               '/#coursestext')
    mainLoop(website, 'rady')