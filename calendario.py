from BestCalendar import bestCalendar

def chaptersWithPages(fileName):
    f = open(fileName, "r", encoding="utf-8")
    lines = f.readlines()

    chapter = {}

    for line in lines:
        lineList = line.split(":")
        title = lineList[0]
        pages = lineList[1].split(",")
        
        chapter[title] = int(pages[1]) - int(pages[0])

    return chapter


if __name__ == "__main__":
    chapterList = chaptersWithPages("cap.txt")
    numberofDays = 26
    numberofChapters = len(chapterList)

    calendar = bestCalendar(chapterList, numberofDays)

    print(numberofChapters)