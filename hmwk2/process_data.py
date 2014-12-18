treatment_prefixes = ['timings_reduc2','timings_reducCol', 'timings_reduc3']

p_s = ['1','4','16','64','256']
n_s = ['100','10','5000']

reps = range(1,11)

header = "uid treatment n p time\n"

outputFileName = "processed_timings_prob1.dat"

outFile = open(outputFileName, 'w')
outFile.write(header)

for t in treatment_prefixes:
    for p in p_s:
        for n in n_s:
            for r in reps:
                fname = t+n+"_"+p+"_"+str(r)+".dat"
                uid = t+"_"+n+"_"+p+"_"+str(r)
                curFile = open(fname, 'r')
                line = curFile.readlines()[0].strip()
                oneLine = uid + " " + t+" "+n+" "+p+" "+line+"\n"
                outFile.write(oneLine)
                curFile.close()
outFile.close()
                
