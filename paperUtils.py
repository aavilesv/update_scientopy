import csv
import globalVar
import re
import json
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def analyzeFileDict(ifile, papersDict):

  firstLineTell = ifile.tell()
  firstLine = ifile.readline()
  ifile.seek(firstLineTell)

  if "\t" in firstLine:
    reader = csv.reader(ifile, delimiter='\t')
  else:
    reader = csv.reader(ifile,delimiter=',')

  header = 0
  rownum = 0
  for row in reader:
    # Save header row.
    if rownum == 0:
      header = row
    else:
      colnum = 0
      paperIn = {};
      
      # Init key elements as zero        
      paperIn["authors"] = ""
      paperIn["title"] = ""
      paperIn["year"] = ""
      paperIn["source"] = ""
      paperIn["doi"] = ""
      paperIn["abstract"] = ""
      paperIn["authorKeywords"] = ""
      paperIn["indexKeywords"] = ""
      paperIn["documentType"] = ""
      paperIn["affiliations"] = ""
      paperIn["cr"] = ""
      paperIn["eid"] = ""
      paperIn["dataBase"] = ""
      paperIn["country"] = ""
      paperIn["subject"] = ""
      paperIn["citedBy"] = ""
      paperIn["duplicatedIn"] = ""
      
      for col in row:
        if colnum >= len(header):
          break
        
        headerCol = header[colnum].decode("ascii", errors="ignore").encode()
        
        # Scopus fields
        if headerCol == "Authors": paperIn["authors"] = col.replace(",", ";")
        if headerCol == "Title": paperIn["title"] = col
        if headerCol == "Year": paperIn["year"] = col
        if headerCol == "Source title": paperIn["source"] = col
        if headerCol == "DOI": paperIn["doi"] = col
        if headerCol == "Abstract": paperIn["abstract"] = col
        if headerCol == "Author Keywords": paperIn["authorKeywords"] = col
        if headerCol == "Index Keywords": paperIn["indexKeywords"] = col
        if headerCol == "Document Type": paperIn["documentType"] = col
        if headerCol == "Authors with affiliations": paperIn["affiliations"] = col
        if headerCol == "Cited by": paperIn["citedBy"] = col
        if headerCol == "EID": paperIn["eid"] = col

        # WoS fields
        if headerCol == "AU": paperIn["authors"] = col
        if headerCol == "TI": paperIn["title"] = col
        if headerCol == "PY": paperIn["year"] = col
        if headerCol == "SO": paperIn["source"] = col
        if headerCol == "DI": paperIn["doi"] = col
        if headerCol == "AB": paperIn["abstract"] = col
        if headerCol == "DE": paperIn["authorKeywords"] = col
        if headerCol == "ID": paperIn["indexKeywords"] = col
        if headerCol == "DT": paperIn["documentType"] = col
        if headerCol == "C1": paperIn["affiliations"] = col
        if headerCol == "SC": paperIn["subject"] = col
        if headerCol == "CR": paperIn["cr"] = col
        if headerCol == "TC": paperIn["citedBy"] = col
        if headerCol == "UT": paperIn["eid"] = col
        
        # Own fields
        if headerCol == "duplicatedIn": paperIn["duplicatedIn"] = col
        if headerCol == "country": paperIn["country"] = col
        
          
        colnum += 1
      
      # Remove dots from authors
      paperIn["authors"] = paperIn["authors"].replace(".", "")
      
      # Remove coma from authors
      paperIn["authors"] = paperIn["authors"].replace(",", "")

      # Remove accents in authors
      paperIn["authors"] = strip_accents(unicode(paperIn["authors"], "utf-8"))
      paperIn["authors"] = paperIn["authors"].encode('utf-8')
      
      # Omit papers without title
      if paperIn["title"] == "":
        continue
        
      if paperIn["eid"].startswith("WOS"):
        paperIn["dataBase"] = "WoS"
        globalVar.papersWoS += 1

      if paperIn["eid"].startswith("2-"):
        paperIn["dataBase"] = "Scopus"
        globalVar.papersScopus += 1
      
      if paperIn["country"] == "": 
        # Get the first author affiliations, and extract the last item as contry
        firstAf = re.split("; (?=[^\]]*(?:\[|$))",paperIn["affiliations"])[0]
        paperIn["country"] = re.split(", (?=[^\]]*(?:\[|$))",firstAf)[-1]
        
        if "CHINA".upper() in paperIn["country"].upper():
          paperIn["country"] = "China"
        
        if "USA".upper() in paperIn["country"].upper():
          paperIn["country"] = "United States"

        if "ENGLAND".upper() in paperIn["country"].upper():
          paperIn["country"] = "United Kingdom"
        if "SCOTLAND".upper() in paperIn["country"].upper():
          paperIn["country"] = "United Kingdom"
        if "WALES".upper() in paperIn["country"].upper():
          paperIn["country"] = "United Kingdom"
        
        if "U ARAB EMIRATES".upper() in paperIn["country"].upper():
          paperIn["country"] = "United Arab Emirates"
          
        if "RUSSIA".upper() in paperIn["country"].upper():
          paperIn["country"] = "Russian Federation"
          
        if "VIET NAM".upper() in paperIn["country"].upper():
          paperIn["country"] = "Vietnam"
          
        if "TRINID & TOBAGO".upper() in paperIn["country"].upper():
          paperIn["country"] = "Trinidad and Tobago"


      # If an author instead a country
      if paperIn["country"].endswith('.'):
        paperIn["country"] = "No country"
        
      #printPaper(paperIn)
        
      # Filter papers that are not in document tipe list
      if any(pType.upper() in paperIn["documentType"].upper().split("; ") \
      for pType in globalVar.INCLUDED_TYPES):        
        papersDict.append(paperIn)
      else:
        globalVar.omitedPapers += 1
    rownum += 1
    
  ifile.close()
  

def printPaper(paper):
  print('Authors: %s' % (paper["authors"]))
  print('Title: %s' % (paper["title"]))
  print('Year: %s' % (paper["year"]))
  print('Source: %s' % (paper["source"]))
  print('DOI: %s' % (paper["doi"]))
  #print('Abstract: %s' % (paper["abstract"]))
  print('Author Key: %s' % (paper["authorKeywords"]))
  print('Index Key: %s' % (paper["indexKeywords"]))
  print('eid: %s' % (paper["eid"]))
  print('Data base: %s' % (paper["dataBase"]))
  print('Affilations:')
  
  for af in re.split("; (?=[^\]]*(?:\[|$))",paper["affiliations"]):
    print("- " + af)
  print('Country: %s' % (paper["country"]))
  print('Document type: %s' % (paper["documentType"]))
  print('\n')
  
  

  
def removeDuplicates(paperDict):
  duplicatedPapersCount = 0
  removedPapersScopus = 0
  removedPapersWoS = 0
  originalPapersCount = len(paperDict)
  noAuthors = 0
  
  print("Sorting documents, WoS first, then Scopus")
  paperDict = sorted(paperDict, key=lambda x: x["dataBase"], reverse=True)
  
  print("Removing duplicates...")
  print len(paperDict)

  # Run on paper list
  for i in range(0, len(paperDict)):

    if i >= len(paperDict):
      continue
    
    # Comparte this paper on a second run
    for j in range(0, len(paperDict)):
      
      if i == j:
        continue

      if j >= len(paperDict):
        continue
        
      if i >= len(paperDict):
        continue
      
      # Compare title and first author last name
      
      # Remove part of the title inside parentisis or square brakets
      # Some journals put this the original language tile in the brakets
      # Remove whitespace at the end of the tile
      
      try:
        match = paperDict[i]["authors"][0].upper() == paperDict[j]["authors"][0].upper()
        if not match:
          continue
      except:
        noAuthors += 1

      match = paperDict[i]["authors"].split(" ")[0].upper() == paperDict[j]["authors"].split(" ")[0].upper()
      if not match:
        continue
      
      titleI = re.sub("[\(\[].*?[\)\]]", "", paperDict[i]["title"].upper()).rstrip()
      titleJ = re.sub("[\(\[].*?[\)\]]", "", paperDict[j]["title"].upper()).rstrip()
      match &=  titleI == titleJ

      
      # If the criteria match
      if(match == True):
        print("\nPaper %s duplicated with %s" %  (i, j))
        
        print("Dup A: %s, %s" % (paperDict[i]["title"], paperDict[i]["year"]))
        print("Autrhos, database: %s, %s" % 
        (paperDict[i]["authors"], paperDict[i]["dataBase"]))
        
        print("Dup B: %s, %s" % (paperDict[j]["title"], paperDict[j]["year"]))
        print("Authors, database: %s, %s" % 
        (paperDict[j]["authors"], paperDict[j]["dataBase"]))
        
        if paperDict[j]["dataBase"] == "WoS":
          removedPapersWoS += 1

        if paperDict[j]["dataBase"] == "Scopus":
          removedPapersScopus += 1
          
        # Remove paper j
        print("Removing: %s" % paperDict[j]["dataBase"])
        paperDict[i]["duplicatedIn"] = paperDict[j]["eid"]
        paperDict.remove(paperDict[j])
        duplicatedPapersCount += 1
        j -= 1
        continue

        
        
        
    print("\r{0:.0f}%".format(float(i)/float(len(paperDict)) * 100)),
        
  print("\nDuplicated papers found: %s" % duplicatedPapersCount)
  print("Original papers count: %s" % originalPapersCount)
  print("Actual papers count: %s" % len(paperDict))
  print("Removed papers WoS: %s" % removedPapersWoS)
  print("Removed papers Scopus: %s" % removedPapersScopus)
  
  
  globalVar.logFile.write("\nDuplicated papers found: %s\n" % duplicatedPapersCount)
  globalVar.logFile.write("Original papers count: %s\n" % originalPapersCount)
  globalVar.logFile.write("Actual papers count: %s\n" % len(paperDict))
  globalVar.logFile.write("Removed papers WoS: %s\n" % removedPapersWoS)
  globalVar.logFile.write("Removed papers Scopus: %s\n" % removedPapersScopus)
  
  return paperDict


  
def sourcesStatics(paperDict):
  statics = {}
  
  statics["Scopus"] = {}
  statics["WoS"] = {}
  
  statics["Scopus"]["Article"] = 0
  statics["Scopus"]["Conference Paper"] = 0
  statics["Scopus"]["Proceddings Paper"] = 0
  statics["Scopus"]["Review"] = 0
  statics["Scopus"]["Total"] = 0
  
  statics["WoS"]["Article"] = 0
  statics["WoS"]["Conference Paper"] = 0
  statics["WoS"]["Proceedings Paper"] = 0
  statics["WoS"]["Review"] = 0
  statics["WoS"]["Total"] = 0
  
  noDocumentTypeCount = 0
  
  for paper in paperDict:
    try:
      statics[paper["dataBase"]][paper["documentType"].split("; ")[0]] += 1
    except:
      noDocumentTypeCount += 1
      
    statics[paper["dataBase"]]["Total"] += 1

  print(json.dumps(statics, indent = 2))
  globalVar.logFile.write(json.dumps(statics, indent = 2))
  





  

