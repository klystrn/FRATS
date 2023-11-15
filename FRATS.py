import sqlite3

#sqlite3 [database name] - connect to database

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file: #reading binary file
        blobData = file.read() 
    return blobData

def insertBLOB(name, photo, proofFile):
    try:
        con = sqlite3.connect("FRATS.db")
        cur = con.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Userinfo
                                  (name, Image, VerifyImg) VALUES (?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        proof = convertToBinaryData(proofFile)
        # Convert data into tuple format
        data_tuple = (name, empPhoto, proof)
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

insertBLOB("QY", "opencv0.png", "opencv1.png")
