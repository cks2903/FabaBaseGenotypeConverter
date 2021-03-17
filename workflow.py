"""
Workflow for genotype conversion from FabaBase output 
to useful output in downstream genetic analyses
"""
import os

from gwf import Workflow 

param_one = os.environ.get("file") #User-specified file to work on
param_two = int(float(os.environ.get("missingness")))

gwf=Workflow()


def LongtoWide(genotypefileFabaBase, outputs):
    inputs = [genotypefileFabaBase]
    outputs = outputs
    options = {
        'account': 'nchain',
        'memory': '8g',
        'walltime': '08:00:00'
    }

    spec = '''
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate Rprogram
    Rscript longtowide.R {genotypefileFabaBase} 
    '''.format(genotypefileFabaBase=genotypefileFabaBase,outputs=outputs)

    return inputs, outputs, options, spec

def MakePedAndMapFiles(genotypefilecsv, outputs):
    inputs = [genotypefilecsv]
    outputs = outputs
    options = {
        'account': 'nchain',
        'memory': '250g',
        'cores': '10',
        'walltime': '08:00:00'
    }

    spec = '''
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate Rprogram
    Rscript MakePedAndMapFile.R {missingness_threshold_snps} 
    '''.format(missingness_threshold_snps=param_two)

    return inputs, outputs, options, spec

def FinishPedAndMapFiles(inputs,outputs):
    inputs = inputs
    outputs = outputs
    options = {
        'account': 'nchain',
    }
    spec = '''
    ./finishped.sh
    '''

    return inputs, outputs, options, spec

def PlinkPrep(inputs,outputs):
    inputs = inputs
    outputs = outputs
    options = {
        'account': 'nchain',
    }
    spec = '''
    ./plinkGenotypeConv.sh
    '''

    return inputs, outputs, options, spec


def GenotypeFileReady(genofile, pedsix,outputs):
    inputs = [genofile,pedsix]
    outputs = outputs
    options = {
        'account': 'nchain',
        'cores': '10',
    }

    spec = '''
    source ~/miniconda2/etc/profile.d/conda.sh
    conda activate myproject
    python MakeGenofileReadyforGRM.py {genofile} 
    '''.format(genofile=genofile)

    return inputs, outputs, options, spec

def GenericGenotypefile(map, genotypes,outputs):
    inputs = [map,genotypes]
    outputs = outputs
    options = {
        'account': 'nchain',
        'cores': '10',
    }

    spec = '''
    ./MakeGenericGenotypefile.sh
    '''

    return inputs, outputs, options, spec

def Cleaning(file1, file2, file3, file4, file5, file6, file7, file8,outputs):
    inputs = [file1,file2,file3,file4,file5,file6,file7,file8]
    outputs = outputs
    options = {
        'account': 'nchain',
        'cores': '10',
    }

    spec = '''
    ./cleaning.sh {file1} {file2} {file3} {file4} {file5} {file6} {file7} {file8} 
    '''.format(file1=file1,file2=file2,file3=file3,file4=file4,file5=file5,file6=file6,file7=file7,file8=file8)

    return inputs, outputs, options, spec


# Convert long to wide format
gwf.target_from_template("Step1",
                         LongtoWide(genotypefileFabaBase=param_one,
                         outputs=["Genotypefile.csv"]))

# Make ped and map files
gwf.target_from_template("Step2",
                         MakePedAndMapFiles(genotypefilecsv="Genotypefile.csv",
                         outputs=["genotypes.map","intermediate.txt","pedsixcol.txt"]))


# Finish ped files
gwf.target_from_template("Step3",
                         FinishPedAndMapFiles(inputs=["pedsixcol.txt","intermediate.txt"],
                         outputs=["genotypes.ped"]))

# Plink conversion
gwf.target_from_template("Step4",
                        PlinkPrep(inputs=["genotypes.ped","genotypes.map"],
                        outputs=["genotypes_numeric.tped","genotypes_numeric.tfam","genotypes_numeric.nosex","genotypes_numeric.log"]))

# genotype for GRM
gwf.target_from_template("Step5",
                         GenotypeFileReady(genofile="genotypes_numeric.tped",pedsix="pedsixcol.txt",
                         outputs=["genotypes_for_GRM.csv"]))


# Make a genetic genotype file
gwf.target_from_template("Step6",
                         GenericGenotypefile(map="genotypes.map",genotypes="genotypes_for_GRM.csv",
                         outputs=["GenericGenotypeFile.csv"]))

# Cleaning up
#gwf.target_from_template("Step7",
                    #     Cleaning(file1="genotypes_for_GRM.csv", file2="genotypes_numeric.tped", file3="genotypes_numeric.tfam", file4="genotypes_numeric.nosex", file5="genotypes_numeric.log", file6="pastedgenofile.txt",file7="pedsixcol.txt",file8="intermediate.txt",
                    #     outputs=[]))




