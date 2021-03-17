# a script to reshape the genotype data outputted by mysql

# load libraries
library(tidyr)
require(data.table)
args=commandArgs(trailingOnly = TRUE)


# Load data
data1 <- as.data.frame(fread(args[1]))
print(paste(nrow(data1),"rows and", ncol(data1),"columns where found"),sep=" ")
data1=data1[,-c(1,20,26,34)]

colnames(data1)=c("SLID","GTID","GenotypingDate","GenotypeCall","Comments1","SNID","SNPidentifier","ProbesetID","Start","Strand","Gene","Annotation","Callrate","FLD","HetSO","HomRO","GenotypingPlatform","Comment2","GPID","HarvestDate","HarvestLocation","ParentSLID","Comment3","Name","Alternative Name","Donor","GeographicOrigin","Maintaining","Comments4","MPID","MapName","Chromosome","Position","Comments5")
print(paste(length(unique(data1$SNID)),"unique SNPs are represented"),sep=" ")
print(paste(length(unique(data1$SLID)), "unique SLIDs are represented"),sep=" ")


# convert table from long t
columnsToExclude = which(colnames(data1) %in% c("GPID","HarvestDate","HarvestLocation","ParentSLID","Comment3","Name","Alternative Name","Donor","GeographicOrigin","Maintaining","Comments4"))
EssentialTable <- data1[-c(columnsToExclude)]

print("starting pivot conversion")
wide_DF <- EssentialTable %>% spread("SLID", "GenotypeCall")
dim(wide_DF)

write.table(wide_DF,"Genotypefile.csv",col.names=T,row.names=F,quote=F,sep=";")


