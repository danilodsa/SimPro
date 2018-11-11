for i in `seq 1 100`;
 do
    python SimPro.py PRTY cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py FCFS cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py SJF cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py RR cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py SRT cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py PFCS cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py IFCS cenarios/cenarioP6.txt P  #Compilation
done

for i in `seq 1 100`;
 do
    python SimPro.py FPCS cenarios/cenarioP6.txt P  #Compilation
done