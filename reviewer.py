import sys
import csv


class Reviewer:
    def __init__(self, name, rating, title, content, rev_wrote, replied):
        self.name = name
        self.rating = rating
        self.title = title
        self.content = content
        self.rev_wrote = rev_wrote

        if replied:
            self.reply = True
        else:
            self.reply = False

    def save_to_csv(self):
        """ saves instance of class to csv file"""
        row = [self.name.strip(), self.rating.strip(), self.title.strip(), self.content.strip(), self.rev_wrote.strip(),
               self.reply, self]
        with open('reviewer.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            csvFile.write(",")
            writer.writerow(row)
        csvFile.close()
