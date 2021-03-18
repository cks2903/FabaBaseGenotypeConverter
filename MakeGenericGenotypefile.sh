
echo -e "CHR\tSNP\tDummy\tPOS" | cat - genotypes.map > SNPinfo_withheader.txt
sed -e "s/\t/,/g" < SNPinfo_withheader.txt > SNPinfo_withheader.csv



cut -f2 SNPinfo_withheader.csv  >SNPinfo_withheader_.csv
cut -f1,4 SNPinfo_withheader.csv >SNPinfo_withheader__.csv
paste SNPinfo_withheader_.csv SNPinfo_withheader__.csv  > SNPinfo.csv
cat SNPinfo.csv | tr '\t' ',' > SNPinfo_.csv

# merge two files 
paste SNPinfo_.csv genotypes_for_GRM.csv > GenericGenotypeFile.csv
cat GenericGenotypeFile.csv | tr '\t' ',' > GenericGenotypeFile_.csv


# clean up
rm SNPinfo_withheader.txt
rm SNPinfo_withheader.csv
rm SNPinfo_withheader_.csv
rm SNPinfo_withheader__.csv
rm SNPinfo.csv
rm SNPinfo_.csv
rm GenericGenotypeFile.csv
mv GenericGenotypeFile_.csv GenericGenotypeFile.csv
