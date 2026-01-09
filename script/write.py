import csv
import array

# NON STAI CONSIDERANDO LA FINE </body></html>, dovresti farlo

lm3 = "Previsto il prevedibile || Foreseen the Foreseeable (May 25)"
lm4 = "Raptus Aviario || Down the goose hole (Jun 25)"
lm5 = "Il Giorno dei Pareri || Opinion's Day (Oct 25)"
lm6 = "Ode all'Oblìo || Ode to Oblivion (Dec 25)"
names = []
text = []
eng = []
partialhtml = []

with open('form_again.csv', mode ='r')as form:
    csvFile = csv.reader(form)
    for lines in csvFile:
        if lines[1]==lm6:                            # CAMBIA IL TEMA
            names.append(lines[2])
            text.append(lines[3])
            eng.append(lines[4])


mainfile = open("main_file.html").read()
subfile = open("subfile.html")
substring = subfile.read()
for i in range(0,len(text)):
    rsub = substring.replace("TESTO",text[i].replace("\n","<br>")).replace("TEXT",eng[i].replace("\n","<br>")).replace("PSEUDONIMO",names[i].replace("\n","<br>"))
    partialhtml.append(rsub)

output = open("lm6_internal.html",'w')              # CAMBIA TEMA
output.write(str(mainfile)+"\n")
for i in range(0,len(partialhtml)):
    output.write(str(partialhtml[i])+"\n")
output.close()
