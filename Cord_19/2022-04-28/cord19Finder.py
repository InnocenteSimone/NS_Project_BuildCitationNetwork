from ast import Break
import csv
import os
import json
from collections import defaultdict



def main(file_present=True):
    papersCount = 0
    titlesAndRef = {}
    with open('metadata.csv',encoding='utf8') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:        
            # access some metadata
            cord_uid = row['cord_uid']
            title = row['title']
            abstract = row['abstract']
            authors = row['authors']
            
            if (('Covid-19 vaccine' in title) or ('covid-19 vaccine' in title) or ("Vaccine Covid-19" in title) or ("vaccine Covid-19" in abstract) or (("Vaccine Covid-19" in abstract))):
                papersCount+=1
                print(f"TITLE:{title}")
            else:
                continue
            
            # access the full text (if available) for Intro
            reference = []
            if(file_present):
                if row['pdf_json_files']:
                    for json_path in row['pdf_json_files'].split('; '):
                        with open(json_path,encoding='utf8') as f_json:
                            full_text_dict = json.load(f_json)

                            #print("\tREFERENCE:")
                            for i,el in enumerate(full_text_dict['bib_entries'].keys()):   
                                #print(full_text_dict['bib_entries'][el])
                                reference.append(full_text_dict['bib_entries'][el]['title'])

                            # stop searching other copies of full text if already got introduction
                            if reference:
                                break

                if len(reference) > 40:
                    titlesAndRef[title] = reference

                    print(f"TITLE: {title} - #REF: {len(reference)}")
                    print(f"\tAUTHOURS: {authors}")
                    print("\tREFERENCE:")
                    for i,el in enumerate(reference):   
                        print(f"\t {i}){el}")        
                    print("-"*100)
                


                with open('titleAndRef.txt',"w",encoding="utf8") as newfile, open('titles.txt','w',encoding='utf8') as onlytitles:
                    s = ""
                    for title in titlesAndRef.keys():
                        s += "TITLE: "+ title + " ---- # REF: " + f"{len(titlesAndRef[title])}\n\t"
                        for i,ref in enumerate(titlesAndRef[title]):
                            s += f"{i})"+ref + "\n\t"
                        s = s[:-1]
                        s += "\n"
                        onlytitles.write(title+"\n")
                        
                    newfile.write(s)
        
    print(f"Number of papers regarding Covid-19 and vaccine: {papersCount}")

if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("File Not Found, please copy the 'metadata.csv' file and document_parses' folder from CORD_19 in this directory")
        main(file_present=False)


