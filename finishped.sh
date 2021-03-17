paste -d',' pedsixcol.txt intermediate.txt > pastedgenofile.txt 
sed 's/NA/NA\/NA/g' pastedgenofile.txt >genotypes_csv.ped
sed 's/\//,/g' genotypes_csv.ped >genotypes__csv.ped
sed 's/,/ /g' genotypes__csv.ped >genotypes.ped
rm genotypes_csv.ped
rm genotypes__csv.ped 