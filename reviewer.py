import csv
import mysql.connector
import re


class Reviewer:
    def __init__(self, name, rating, title, content, rev_wrote, replied):
        self.name = name
        self.rating = rating
        self.stars = int(self.rating.strip().split(' ')[0])
        self.title = title
        self.content = content
        self.rev_wrote = rev_wrote
        self.reviews = int(self.rev_wrote.strip().split(' ')[0])

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

    def save_to_sql(self):
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password='123456'
        )

        my_cursor = my_db.cursor()

        my_cursor.execute("""USE trustpilot;""")
        name = re.sub(r'\W+', ' ', self.name)
        sql = """INSERT INTO Users (user_name, country, rev_wrote) VALUES ("%s" , "%s" , %d)""" % (
            name, "UK", self.reviews)
        my_cursor.execute(sql)
        my_db.commit()

        content = re.sub(r'\W+', ' ', self.content)
        sql = """INSERT INTO Reviews (user_id, company_id, title , content) VALUES (%d, %d, "%s", "%s")""" % (
            112233, 445566, 'my_title', content[:250])
        my_cursor.execute(sql)
        my_db.commit()

        sql = """INSERT INTO Companies (name , website, rating, num_reviews) VALUES ("%s" , "%s" , %d, %d)""" % (
            self.name, "www.mywebsite.com", self.stars, 1)
        my_cursor.execute(sql)
        my_db.commit()

        pass
