fin = open("vars.txt", 'r')
fout = open("out.txt", 'w')

for line in fin:
    list = line.split()
    if(len(list) > 2):
        fout.write('nv = {"GLOBAL:')
        fout.write(list[1])
        fout.write('", "')
        fout.write(list[0])
        fout.write('", &')
        fout.write(list[1])
        fout.write(', sizeof(')
        fout.write(list[0])
        fout.write(')};\n')
        fout.write('writeValue(nv, stateFile);\n')

fin.close()
fout.close()
