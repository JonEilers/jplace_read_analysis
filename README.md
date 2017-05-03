# jplace_read_analysis
Scripts to calculate read placement summary statistics

## pas.py
#### Arguments: -directory _usr/home/folder_containing_jplace_files_  -out_file *output_file_name.txt*
reads all .jplace files in directory and calculates 'total number of reads', 'number of reads placed on internal edges', 'number of reads placed on leafs'.

## pas_fga.py
#### Arguments: -directory _usr/home/folder_containing_jplace_files_ -out_file *output_file_name.txt*
reads all .jplace files in the directory provided and calculates the numbers of reads placed internally vs leafs for each COG family. Also calculates the total. use this instead of pas.py. 
