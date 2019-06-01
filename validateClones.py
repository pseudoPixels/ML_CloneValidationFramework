import pickle
import subprocess
import os
import uuid
import glob
import xml.etree.ElementTree as ET
import shutil
import argparse

from mlCCV.MLHelper import MLHelper
from mlCCV.Utils import Utils


mlHelper = MLHelper()
utils = Utils()

def run(args):


    validationThreshold = float(args.val_threshold)
    inputCloneDir = args.input_Dir
    outDir = args.output_Dir

    # print validationThreshold
    # print inputCloneDir
    # print outDir


    list_of_file_for_validation = [x for x in glob.glob(inputCloneDir + '/' + '*.xml')]

    OVERALL_TRUE_CLONES = 0
    OVERALL_CLONE_PAIRS = 0

    print 'Starting Validation...'
    progress = 0

    if os.path.isdir(outDir):
        shutil.rmtree(outDir)
    os.mkdir(outDir)

    cloneFilesCounts = len(list_of_file_for_validation)
    for aCloneFile in list_of_file_for_validation:
        print 'Validation Progress : ' + str(progress * 100 / cloneFilesCounts) + '%'

        cloneFileBaseName = os.path.basename(aCloneFile)
        mlValidation_output_file = outDir + '/' + cloneFileBaseName + '.mlValidated'

        mlValidationCount = 0

        if os.path.exists(mlValidation_output_file) == True:
            # response_code = 'FILE_ALREADY_EXIST'
            mlValidationCount = sum(1 for line in open(mlValidation_output_file))
        else:
            new_file = open(mlValidation_output_file, "w")
            new_file.close()

        tree2 = ET.parse(aCloneFile)
        root = tree2.getroot()
        totalClonePairs = len(root)

        for aCloneIndex in range(mlValidationCount, totalClonePairs):
            fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, clones_validated, total_clones = utils.get_next_clone_pair_for_validation(
                aCloneFile, mlValidation_output_file)
            OVERALL_CLONE_PAIRS = OVERALL_CLONE_PAIRS + 1

            true_probability = mlHelper.app_code_clone_getValidationScore(fragment_1_clone, fragment_2_clone, 'java')

            with open(mlValidation_output_file, "a") as validationFile:
                if true_probability >= validationThreshold:
                    validationFile.write(
                        'true' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' + fragment_2_startline + ',' + fragment_2_endline + '\n')
                    OVERALL_TRUE_CLONES = OVERALL_TRUE_CLONES + 1
                else:
                    validationFile.write(
                        'false' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' + fragment_2_startline + ',' + fragment_2_endline + '\n')

        progress = progress + 1

    print 'Done'

    print '##############################################'
    print '           CLONE VALIDATION STATS             '
    print '##############################################'

    print 'Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS)
    print 'Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES)
    print 'Predicted False Positive Clones: ' + str(OVERALL_TRUE_CLONES - OVERALL_TRUE_CLONES)
    print 'Predicted Precision: ' + str(OVERALL_TRUE_CLONES / OVERALL_CLONE_PAIRS)

    with open(outDir + '/' + '__CLONE_VALIDATION_STATS.txt', "a") as cloneValidationStats:
        cloneValidationStats.write('Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS) + '\n')
        cloneValidationStats.write('Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES) + '\n')
        cloneValidationStats.write(
            'Predicted False Positive Clones: ' + str(OVERALL_CLONE_PAIRS - OVERALL_TRUE_CLONES) + '\n')
        cloneValidationStats.write('Predicted Precision: ' + str(OVERALL_TRUE_CLONES / OVERALL_CLONE_PAIRS) + '\n')


def main():
    parser = argparse.ArgumentParser(description="This is a machine learning based framework for automatic code clone validation.")
    parser.add_argument("-in", help="(required) input directory of detected code clones (i.e., outputs from NICAD)", dest="input_Dir", type=str, required=True)
    parser.add_argument("-out", help="(required) target output directory of machine learning validated clones", dest="output_Dir", type=str, required=True)
    parser.add_argument("-t", help="(optional) the threshold for automatic clone validation. Default=0.5", dest="val_threshold", type=float, default=0.5)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)





if __name__ == "__main__":
    main()





































