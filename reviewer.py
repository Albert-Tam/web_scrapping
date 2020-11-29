import sys
import csv
import mysql.connector

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

    def save_to_sql(self):
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456"
        )

        my_cursor = my_db.cursor()

        my_cursor.execute("""USE trustpilot;""")

        sql = "INSERT INTO Users (user_name, country, rev_wrote) VALUES (%s , %s , %d);"
        val = (self.name, "UK", self.rev_wrote)
        my_cursor.execute(sql, val)
        my_db.commit()

        sql = "INSERT INTO Reviews (user_id, company_id, title , content) VALUES (%d, %d, %s , %s);"
        val = (112233, 445566, self.title, self.content)
        my_cursor.execute(sql, val)
        my_db.commit()

        sql = "INSERT INTO Companies (name , website, rating, num_reviews) VALUES (%s , %s , %d, %d);"
        val = (self.name, "www.mywebsite.com", self.rating, 1)
        my_cursor.execute(sql, val)
        my_db.commit()

        pass
