# Genotype Converter

This is a small workflow to convert the FabaBase genotype output to the following formats:
1) .tped and .tfam files needed for EMMAX
2) .ped and .map files needed for plink
3) A file called "GenericGenotypeFile.csv" which contains 3+N columns and M rows,  where N is the number of genotyped individuals and M is the number of markers after missingness filter.
col1: SNP_ID, col2: CHR, col3: POS, col4-colN: SLIDs
Genotypes are in the following format: -1 (reference homozygote),0 (heterozygote),1 (alternative homozygote). 

The needed inputs are:
1) The genotype file outputted from FabaBase.au.dk 
2) A number indicating the threshold you want to apply for the SNP missingness filter.
The number should be between  0.00 and 1.00. 
0.00 indicates that SNPs with more than 0% missingness should be removed, 
1.00 indicates that SNPs with more than 1.00% missingness should be removed

Both arguments are required. If no missingness filter is wanted use: "1.00"





## Getting Started

To use this code, you will need to have conda or miniconda installed.
If you don't have conda/miniconda, you can get it here: 
https://docs.conda.io/en/latest/miniconda.html



### Prerequisites

All other requirements are provided in YAML files

### Installing

To install the program you need to follow these steps:

Step 1:

Open the command line and navigate to the folder where you want the conversion to take place.

Clone the github repository to the location:
```
git clone https://github.com/cks2903/FabaBaseGenotypeConverter.git

```

Step 2:

Create the needed environments by typing: 

```
cd FabaBaseGenotypeConverter
chmod u+x Prepare.sh

./Prepare.sh
```
Step 3:
Source the needed environment:

```
source activate python3
```
Step 4:
Now open up an additinal command-line window and write:
```
gwf workers
```

This should say "Started 12 workers, listening on port 12345". Keep the window open but navigate to the other one.

Step 5:
Define the inputs as follows:
```
file="[path/genotype file you have from FabaBase]"
export file
missingness="[the missingness threshold you want]"
export missingness
```
You are now ready to run the pipeline. You do so by typing:

```
gwf run
```

You should now see your screen say "Submitting target Step1", "Submitting target Step2" etc. until 6 steps have been submitted.
By writing
```
gwf status
```
you can follow how far the workflow has come. When All steps read "Completed" your files should be ready and in the current directory





## Example of how to run
```
file="field-trial-genotype-data-by-map-name--NV644xNV153_F6_RIL_Axiom_Vfaba_v2--profaba.tsv"
export file
missingness="0.10" # applying a missingness filter of 10%
export missingness

gwf run
```

## If problems 
If you have problems running the workflow, i.e. 'gwf status' report steps as "shouldrun"
Run the steps one by one as follows:

Step1
```
conda deactivate
source activate Rprogram
Rscript longtowide.R [path/genotype file you have from FabaBase]
```
Proceed to step 2 when the "Genotypefile.csv" is generated


Step2
```
conda deactivate
source activate Rprogram
Rscript MakePedAndMapFile.R [missingness_threshold_snps] 
```
Proceed to step 3 when the "genotypes.map", "intermediate.txt" and "pedsixcol.txt" files are  generated


Step3
```
chmod u+x finishped.sh
./finishped.sh
```
Proceed to step 4 when "genotypes.ped" is generated

Step4
```
conda deactivate
source activate plink
chmod u+x plinkGenotypeConv.sh
./plinkGenotypeConv.sh
```
Proceed to step 5 when the files "genotypes_numeric.tped","genotypes_numeric.tfam","genotypes_numeric.nosex" and "genotypes_numeric.log" are generated

Step5
```
conda deactivate
source activate python3
python MakeGenofileReadyforGRM.py "genotypes_numeric.tped"

```
Proceed to step 6 when the file "genotypes_for_GRM.csv" is generated 

Step6
```
chmod u+x MakeGenericGenotypefile.sh
./MakeGenericGenotypefile.sh
```
Should generate the file called "GenericGenotypeFile.csv". 
