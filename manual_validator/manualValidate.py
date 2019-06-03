import argparse
import subprocess
import os

from Utils import Utils
from config import *




utils = Utils()



def run(args):

    if os.path.exists( CLONE_HOME_DIR + args.input_clone_file + '.clones') == False:

        total_clone_pairs = utils.get_total_clone_pair_count(CLONE_HOME_DIR + args.input_clone_file)

        print total_clone_pairs

        for i in range(0, total_clone_pairs):

            fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, \
            fragment_2_clone = utils.get_clone_pairs(i,  CLONE_HOME_DIR + args.input_clone_file)

            with open('input_clone_pairs/' + args.input_clone_file + '.clones', "a") as file:
                file.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
                file.write('0\n0\n')

                file.write(fragment_1_path + " " + fragment_1_startline + " " + fragment_1_endline +"\n")
                file.write(fragment_2_path + " " + fragment_2_startline + " " + fragment_2_endline +"\n")

                file.write('----------------------------------------\n')
                file.write(fragment_1_clone)
                file.write('----------------------------------------\n')
                file.write(fragment_2_clone)
                file.write('----------------------------------------\n')


    subprocess.call(['java', '-jar', '../external_tools/manual_clone_validator.jar'])




def main():
    parser = argparse.ArgumentParser(description="This is a framework for manual code clone validation. The manual \
    validated clones can later be used for training machine learning model.")

    parser.add_argument("-in", help="(required) input clone file (i.e., output from NICAD)", dest="input_clone_file", type=str, required=True)
    #parser.add_argument("-out", help="(required) target output file of the prepared clone file", dest="output_clone_file", type=str, required=True)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)



def test_run(args):
    subprocess.call(['java', '-jar', '../external_tools/manual_clone_validator.jar'])





if __name__ == "__main__":
    main()
