import sqlite3

poolDict = {"0": "PD2", "1": "PD3", "2": "PD1", "3": "PD1 Art", "4": "PD1 CB"
            , "5": "PD1 SE", "6": "PD2 Art", "7": "PD2 CB", "8": "PD2 PL", "9": "PD2 SE"
            , "10": "PD3 Art", "11": "PD3 CB", "12": "PD3 PL", "13": "PD3 SE", "14": "PS15"
            , "15": "PS15 Art", "16": "PS15 CB", "17": "PS15 SE", "18": "PD4 Art", "19": "PD4 CB"
            , "20": "PD4", "21": "PD4 SE", "22": "PD5", "23": "PD5 SE", "24": "PD5 PL"
            , "25": "PD5 CB", "26": "PD5 Art", "27": "PD6", "28": "PD6 SE", "29": "PD6 PL"
            , "30": "PD6 CB", "31": "PD6 Art", "pk": "Prime Key", "mp": "Masterpiece"
            , "cd": "Catalyst Drive", "core": "The Core", "pd": "Prime Drive"}

async def getSetData(ids):
    #forQuery = str(ids).replace("'", "").strip("[]")
    forQuery = str(ids).strip("[]")
    dbconnection = sqlite3.connect("./databases/cachingPools.db")
    crsr = dbconnection.cursor()
    if "," in forQuery:
        crsr.execute(f"SELECT * FROM sets WHERE poolId IN ({forQuery})")
        results = crsr.fetchall()
        sortedData = []
        for i in range(len(ids)):
            for j in range(len(results)):
                if results[j][0] == ids[i]:
                    sortedData.append(results[j])
        crsr.close()
        return sortedData
    else:
        crsr.execute(f"SELECT * FROM sets WHERE poolId = '{forQuery}'")
        results = crsr.fetchall()
        crsr.close()
        return results

async def getPrimeData(ids):
    #forQuery = str(ids).replace("'", "").strip("[]")
    forQuery = str(ids).strip("[]")
    print(forQuery)
    dbconnection = sqlite3.connect("./databases/prime.db")
    crsr = dbconnection.cursor()
    if "," in forQuery:
        crsr.execute(f"SELECT * FROM prime WHERE name IN ({forQuery})")
        results = crsr.fetchall()
        sortedData = []
        for i in range(len(ids)):
            for j in range(len(results)):
                if results[j][0] == ids[i]:
                    sortedData.append(results[j])
        crsr.close()
        return sortedData
    else:
        crsr.execute(f"SELECT * FROM prime WHERE name = '{forQuery}'")
        results = crsr.fetchall()
        crsr.close()
        return results