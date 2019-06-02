from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET
import shutil
import argparse

from mlCVF.MLHelper import MLHelper
from mlCVF.Utils import Utils


mlHelper = MLHelper()
utils = Utils()


def run(args):

    validationThreshold = float(args.val_threshold)
    inputCloneFile = args.input_clone_file
    outDir = args.output_Dir

    formattedCloneFile = utils.parse_and_format_clone_pairs_from_nicad_clone_file('input_clone_pairs/' + inputCloneFile)

    inputCloneFile = formattedCloneFile




    OVERALL_TRUE_CLONES = 0
    OVERALL_CLONE_PAIRS = 0

    print 'Validation in progress, please wait...'


    if os.path.isdir(outDir):
        shutil.rmtree(outDir)
    os.mkdir(outDir)


    aCloneFile = inputCloneFile
    cloneFileBaseName = os.path.basename(aCloneFile)
    mlValidation_output_file = outDir + '/' + cloneFileBaseName + '.mlValidated'

    mlValidationCount = 0

    if os.path.exists(mlValidation_output_file) == True:
        mlValidationCount = sum(1 for line in open(mlValidation_output_file))
    else:
        new_file = open(mlValidation_output_file, "w")
        new_file.close()




    # tree2 = ET.parse(aCloneFile)
    # root = tree2.getroot()
    # totalClonePairs = len(root)

    soup = ''
    with open(aCloneFile) as fp:
        soup = BeautifulSoup(fp, 'lxml')

    totalClonePairs = len(soup.find_all('clone'))
    #print totalClonePairs

    for aCloneIndex in range(mlValidationCount, totalClonePairs):
        fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline,\
        fragment_2_clone, clones_validated, total_clones = utils.get_next_clone_pair_for_validation(
            aCloneFile, mlValidation_output_file)
        OVERALL_CLONE_PAIRS = OVERALL_CLONE_PAIRS + 1

        true_probability = mlHelper.app_code_clone_getValidationScore(fragment_1_clone, fragment_2_clone, 'java')
        #print true_probability
        print "Validated : ", aCloneIndex , "/", totalClonePairs, " clones. Last clone prob. : ", true_probability

        with open(mlValidation_output_file, "a") as validationFile:
            if true_probability >= validationThreshold:
                validationFile.write(
                    'true' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' +\
                    fragment_2_startline + ',' + fragment_2_endline + '\n')
                OVERALL_TRUE_CLONES = OVERALL_TRUE_CLONES + 1
            else:
                validationFile.write(
                    'false' + ',' + fragment_1_path + ',' + fragment_1_startline + ',' + fragment_1_endline + ',' + fragment_2_path + ',' +\
                    fragment_2_startline + ',' + fragment_2_endline + '\n')



    print 'Done'



    print '##############################################'
    print '           CLONE VALIDATION STATS             '
    print '##############################################'

    print 'Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS)
    print 'Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES)
    print 'Predicted False Positive Clones: ' + str(int(OVERALL_TRUE_CLONES) - int(OVERALL_TRUE_CLONES))
    print 'Predicted Precision: ' + str(float(OVERALL_TRUE_CLONES) / float(OVERALL_CLONE_PAIRS))

    with open(outDir + '/' + '__CLONE_VALIDATION_STATS.txt', "a") as cloneValidationStats:
        cloneValidationStats.write('Total Clone Pairs Validated: ' + str(OVERALL_CLONE_PAIRS) + '\n')
        cloneValidationStats.write('Predicted True Positive Clones: ' + str(OVERALL_TRUE_CLONES) + '\n')
        cloneValidationStats.write(
            'Predicted False Positive Clones: ' + str(int(OVERALL_CLONE_PAIRS) - int(OVERALL_TRUE_CLONES)) + '\n')
        cloneValidationStats.write('Predicted Precision: ' + str(float(OVERALL_TRUE_CLONES) / float(OVERALL_CLONE_PAIRS)) + '\n')


def main():
    parser = argparse.ArgumentParser(description="This is a machine learning based framework for automatic code clone validation.")
    parser.add_argument("-in", help="(required) input clone file (i.e., output from NICAD)", dest="input_clone_file", type=str, required=True)
    parser.add_argument("-out", help="(required) target output directory of machine learning validated clones", dest="output_Dir", type=str, required=True)
    parser.add_argument("-t", help="(optional) the threshold for automatic clone validation. Default=0.5", dest="val_threshold", type=float, default=0.5)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)



def test_run(args):
    print "In test Run..."
    utils = Utils()
    formattedCloneFile = utils.parse_and_format_clone_pairs_from_nicad_clone_file('input_clone_pairs/'+args.input_clone_file)
    print formattedCloneFile





if __name__ == "__main__":
    main()


