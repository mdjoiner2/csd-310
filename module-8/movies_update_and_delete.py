""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values
#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}
try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the movies database 
    
    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

    db.close()

cursor = db.cursor()
# Function to display films
def show_films(cursor, title):
    cursor.execute("SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' FROM film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")
    films = cursor.fetchall()
    
    print("\n -- {} --".format(title))
    for film in films:
        print(f"Film Name: {film[0]}\n Director: {film[1]}\n Genre Name: {film[2]}\n Studio Name: {film[3]}\n")

# Display initial films
show_films(cursor, "DISPLAYING FILMS")

# Inserted "Inception" as new film
insert_query = """INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
                  VALUES ('Inception', 2010, 148, 'Christopher Nolan', 1, 2)"""
cursor.execute(insert_query)
db.commit()

# Display films after insertion
show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

# Update the film "Alien" to being a Horror film
update_query = "UPDATE film SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') WHERE film_name = 'Alien'"
cursor.execute(update_query)
db.commit()

# 5. Display films after update
show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

# 6. Delete "Gladiator"
delete_query = "DELETE FROM film WHERE film_name = 'Gladiator'"
cursor.execute(delete_query)
db.commit()

# 7. Display films after deletion
show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

# Close the database connection
db.close()




		
