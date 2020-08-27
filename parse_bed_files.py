#!/home/dh486/gnn-env/bin/python
from src.Datatrack import DataTrack_rvp as dtrvp
import numpy as np
import os

CHROMS = [str(i+1) for i in np.arange(19)] + ['X']

if __name__ == "__main__":
    import argparse
    
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Create a binned and SQRT-VC (Rao et al. 2014) noramlised contact matrix from a .tsv file', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-d","--directory",
                        help="directory in which bed_files are stored",
                        default = "/home/dh486/rds/hpc-work/Hi_C_GNN_data/data_raw/datatracks/")
    parser.add_argument("-o", "--outpath",
                        help="path of the output directory for the numpy archive",
                        default = "/home/dh486/rds/hpc-work/Hi_C_GNN_data/data_torch/raw/",
                        type=str)
    parser.add_argument("-f", "--filenames",nargs = "+",
                        help="List of bed files to parse. If None is passed then this script will attempt to parse all files within the given directory",
                        default = None)
    parser.add_argument("-c", "--chrom_col",
                        type = int,
                        default = 0,
                        help = "The column describing the chromosome of each region in the bed file. Defaults to 0.")
    parser.add_argument("-s", "--start_col",
                        type = int,
                        default = 1,
                        help = "The column describing the start of each region in the bed file. Defaults to 0.")
    parser.add_argument("-e", "--end_col",
                        type = int,
                        default = 2,
                        help = "The column describing the end of each region in the bed file. Defaults to 0.")
    parser.add_argument("-vc", "--value_col",
                        default = None,
                        type = int,
                        help = "The column describing the value of each region in the bed file. Defaults to None. If None then the value given to each region is given by the --value_fill argument")
    parser.add_argument("-vf", "--value_fill",
                        default = 1,
                        type = int,
                        help = "If no column is provided to infer region values from then the value given to each region is given by the --value_fill argument. Defaults to 1")
    parser.add_argument("-i", "--id_col",
                        default = None,
                        type = int,
                        help = "The column describing the unique ID of each region in the bed file (if it exists). Defaults to None. If None then no IDs are given to each region")
    parser.add_argument("-he", "--header",
                        default = None,
                        help = "Determines whether the passed bed file has a header line or not. Defaults to None - i.e. no header. If there is a header line, pass --header=0.")
    parser.add_argument("-ch", "--chromosomes", nargs="+",
                        default = CHROMS,
                        help = "Determines which chromosomes to search for within the bed file. Chromosomes within the bed file that are not in this list will be excluded")
    parser.add_argument("-se", "--sep",
                        default = "\t",
                        type = str,
                        help = "separation character between columns in the bed file(s)")
    
    args = parser.parse_args()
    
    if args.filenames is None:
        args.filenames = os.listdir(args.directory)

    myfiles = [os.path.join(args.directory, file) for file in args.filenames]
    
    for idx, file in enumerate(myfiles):
        print("processing file: {}".format(file))
        stripped_name = os.path.split(file)[-1].split(".")[0]
        print("\tstripped filename: {}".format(stripped_name))
        dtrack = dtrvp(args.filenames[idx]).from_bed(file,chrom_col = args.chrom_col,
                                                     region_cols = (args.start_col,args.end_col),
                                                     value_col = args.value_col,
                                                     ID_col = args.id_col,
                                                     value_fill = args.value_fill,
                                                     header = args.header,
                                                     allowed_chroms = args.chromosomes,
                                                     sep = args.sep)
        outname = os.path.join(args.outpath, stripped_name)
        print("\twriting to: {}".format(outname))
        dtrack.to_npz(outname)
        
        
        