# HIVAssembly

## Introduction

In order to combat HIV worldwide, we have developed the ```HIVAssembly pipeline```, to allow you to generate the consensus fasta format from ```Oxford Nanopore technology``` (ONT) data.


## Prerequisite:

You must first install the following packages :
```
sudo apt install minimap2 samtools bcftools seqtk 
```
## Installation

This pipeline can be used directly on the terminal. 
```
git clone https://github.com/KhadimGueyeKGY/HIVAssembly.git
```

## Usage
To know how to use it, just type

```
python HIVAseembly.py
```
You can do the assembly of: 

### 1. A single fastq file
```
python HIVAseembly.py --read ./data/Sample.fastq --output ./data/output/
```
### 2. The fastq files of the different samples which are located in a single directory 
```
python HIVAseembly.py --read ./data/ONT_data/ --output ./data/output/
```
### 3. Fastq_pass after basecalling from fast5 to fastq 
```
python HIVAseembly.py --read ./data/fastq_pass/ --output ./data/output/
```








