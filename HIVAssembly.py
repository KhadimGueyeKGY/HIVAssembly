#!/usr/bin/python

import os
import sys
from Bio import SeqIO
s = sys.argv
if len(s) < 5 :
	print("Usage:\n $ python HIVAssembly.py  --reads  /input/fastq  --output /output/directory\n\n NB:You can give as input a single fastq file or the folder containing only fastq files or the fastq_pass if it is about barcodes")
	print ("\nRequirements\nsudo apt install minimap2 samtools bcftools seqtk")
	print ("conda install -c conda-forge biopython \n OR \n pip install biopython\n")
	sys.exit()

ref = "reference/HIV_ref_sequence_NC_00182.fasta"
os.system("mkdir -p "+s[4]+"/results/")

def fonc(ont):
	os.system("minimap2 -x map-ont -a "+ref+"  "+ont+" > "+s[4]+"/results/aln.sam")
	print("\nCompressing...")
	os.system("cd "+s[4]+"/results/ ; samtools view -S -b aln.sam > aln.bam")
	print("\nSorting...")
	os.system("cd "+s[4]+"/results/ ; samtools sort -o aln.sorted.bam aln.bam")
	print("\nIndexing...")
	os.system("cd "+s[4]+"/results/ ; samtools index -b aln.sorted.bam")
	print("\ngenerate consensus sequence...")
	os.system("samtools mpileup -uf "+ref+" "+s[4]+"/results/aln.sorted.bam | bcftools call -c | vcfutils.pl vcf2fq > "+s[4]+"/results/aln.fastq")
	input = SeqIO.parse(s[4]+"/results/aln.fastq", "fastq")
	output = SeqIO.write(input, s[4]+"/results/aln_consensus.fasta" , "fasta")
	#os.system("seqtk seq -aQ64 -q20 -n N "+s[4]+"/results/aln.fastq > "+s[4]+"/results/aln_consensus.fasta")

if s[2].find(".fastq") != -1 :
	fonc(s[2])
	l = s[2].split("/")
	l = l[len(l)-1].split(".fastq")[0]
	os.system("cd "+s[4]+" ; cp results/aln_consensus.fasta  "+l+"_consensus.fasta " )
	os.system("cd "+s[4]+" ; sed -i -e \"s/NC_001802.1/"+l+"/g\" "+l+"_consensus.fasta")
	print("\n\nDone..\n")
else:
	a = os.popen("cd "+s[2]+" ; ls ").read().split("\n")
	if a[0].find (".fastq") != -1 :
		for i in range(len(a)):
			if a[i]=="":
				break
			print("\n\nAssembly of "+a[i]+" : "+str(i+1)+"/"+str(len(a)-1)+"\n")
			if a[i].find(".fastq") != -1 :
				fonc(s[2]+"/"+a[i])
				l = a[i].split(".fastq")[0]
				os.system("cp "+s[4]+"/results/aln_consensus.fasta "+s[4]+"/"+l+"_consensus.fasta")
				os.system("cd "+s[4]+" ; sed -i -e \"s/NC_001802.1/"+l+"/g\" "+l+"_consensus.fasta")
				print("\n\nDone...\n")
	else :
		for i in range(len(a)):
			if a[i] =="":
				break
			print("\n\nAssembly of "+a[i]+" : "+str(i+1)+"/"+str(len(a)-1)+"\n")
			b = os.popen("cd "+s[2]+"/"+a[i]+" ; ls ").read().split("\n")
			d = ""
			if b[0].find(".fastq.gz") != -1  :
				c = os.system("zcat "+s[2]+"/"+a[i]+"/* > "+s[4]+"/results/output.fastq.gz")
				d = s[4]+"/results/output.fastq.gz"
			else:
				c = os.system("cat "+s[2]+"/"+a[i]+"/* > "+s[4]+"/results/output.fastq")
				d = s[4]+"/results/output.fastq"
			fonc(d)
			os.system("cp "+s[4]+"/results/aln_consensus.fasta "+s[4]+"/"+a[i]+"_consensus.fasta")
			os.system("cd "+s[4]+" ; sed -i -e \"s/NC_001802.1/"+a[i]+"/g\" "+a[i]+"_consensus.fasta")
			print("\n\nDone..\n")

os.system("rm -r "+s[4]+"/results/")
os.system("cd "+s[4]+" ; cat *fasta > all_consensus.fasta")
