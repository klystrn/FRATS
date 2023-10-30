import sqlite3

#cur.execute("CREATE TABLE Userinfo(Name, Image, VerifyImg)")
#cur.execute("SELECT * FROM Userinfo")
#result = cur.fetchall()
#for row in result:
#   print(row[0])

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(name, photo, proofFile):
    try:
        con = sqlite3.connect("FRATS.db")
        cur = con.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Userinfo
                                  (name, photo, proof) VALUES (?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        proof = convertToBinaryData(proofFile)
        # Convert data into tuple format
        data_tuple = (name, empPhoto, proof)
        cur.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table. ", error)
    finally:
        if con:
            con.close()
            print("The sqlite connection is closed")

insertBLOB("P", r"C:\Users\X1 Carbon\Pictures\Saved Pictures\SMO-Award.jpg", r"C:\Users\X1 Carbon\Pictures\uu.txt")

#con.commit()
#con.close()
