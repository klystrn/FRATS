import sqlite3
from datetime import datetime

#sqlite3 [database name] - connect to database

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file: #reading binary file
        blobData = file.read() 
    return blobData

def insertBLOB(ID, name, photo, now):
    try:
        con = sqlite3.connect("FRATS.db")
        cur = con.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Userinfo
                                  (ID, Name, Image, DateTimeSaved) VALUES (?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        now = datetime.now()
        # Convert data into tuple format
        data_tuple = (ID, name, empPhoto, now)
        cur.execute(sqlite_insert_blob_query, data_tuple)
        con.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table. ", error)
    finally:
        if con:
            con.close()
            print("The sqlite connection is closed")

insertBLOB(10, 'Pt', 'opencv0.png', "2022-11-15 13:44:26.768439")
