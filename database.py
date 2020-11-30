import mysql.connector


def create_db():
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )

    my_cursor = my_db.cursor()

    my_cursor.execute("""
    CREATE DATABASE trustpilot;""")

    my_cursor.execute("""
        USE trustpilot;""")

    my_cursor.execute("""
    CREATE TABLE Users (
      user_id int NOT NULL AUTO_INCREMENT,
      user_name varchar(255),
      country varchar(255),
      rev_wrote int,
      PRIMARY KEY (user_id)
      );
    """)

    my_cursor.execute("""
    CREATE TABLE Reviews (
      review_id int NOT NULL AUTO_INCREMENT,
      user_id int NOT NULL,
      company_id int NOT NULL,
      title varchar(255),
      content varchar(255),
      rev_wrote int,
      PRIMARY KEY (review_id) -- ,
      -- FOREIGN KEY (user_id) REFERENCES Users (user_id),
      -- FOREIGN KEY (company_id) REFERENCES Company (company_id)
      );
      """)

    my_cursor.execute("""
    CREATE TABLE Companies (
      company_id int NOT NULL AUTO_INCREMENT,
      name varchar(255),
      website varchar(255),
      rating float,
      num_reviews int,
      PRIMARY KEY (company_id)
      );  
    """)

    # sql = """INSERT INTO users """


create_db()
