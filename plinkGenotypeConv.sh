source /com/extra/plink/1.90-beta-2016-03/load.sh
plink --file genotypes --recode12  --nonfounders  --allow-no-sex --output-missing-phenotype 'NA' --transpose --out genotypes_numeric
