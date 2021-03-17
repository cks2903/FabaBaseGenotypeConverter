
echo -e "CHR\tSNP\tDummy\tPOS" | cat - genotypes.map > SNPinfo_withheader.txt
sed -e "s/\t/,/g" < SNPinfo_withheader.txt > SNPinfo_withheader.csv



cut -f2 SNPinfo_withheader.csv -d "," >SNPinfo_withheader_.csv
cut -f1,4 SNPinfo_withheader.csv -d "," >SNPinfo_withheader__.csv
paste SNPinfo_withheader_.csv SNPinfo_withheader__.csv -d "," > SNPinfo.csv

# merge two files 
paste SNPinfo.csv genotypes_for_GRM.csv -d "," > GenericGenotypeFile.csv

# clean up
rm SNPinfo_withheader.txt
rm SNPinfo_withheader.csv
rm SNPinfo_withheader_.csv
rm SNPinfo_withheader__.csv
rm SNPinfo.csv