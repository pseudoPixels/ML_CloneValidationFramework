

import os
import xml.etree.ElementTree as ET




class Utils:

    def __init__(self):
        pass

    def get_next_clone_pair_for_validation(self, cloneFile, theValidationFile, validationFileExt='.validated'):
        # getting the example program name
        theCloneFile = cloneFile
        # theValidationFile = theCloneFile + validationFileExt

        tree2 = ET.parse(cloneFile)
        root = tree2.getroot()


        print cloneFile

        nextCloneIndex = 0


        if os.path.exists(theValidationFile) == True:
            # response_code = 'FILE_ALREADY_EXIST'
            nextCloneIndex = sum(1 for line in open(theValidationFile))
        else:
            new_file = open(theValidationFile, "w")
            new_file.close()

        # fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, number_of_validated_clones, total_clones
        return root[nextCloneIndex][0].attrib['file'], root[nextCloneIndex][0].attrib['startline'], \
               root[nextCloneIndex][0].attrib['endline'], root[nextCloneIndex][1].text, root[nextCloneIndex][2].attrib[
                   'file'], root[nextCloneIndex][2].attrib['startline'], root[nextCloneIndex][2].attrib['endline'], \
               root[nextCloneIndex][3].text, nextCloneIndex + 1, len(root)


