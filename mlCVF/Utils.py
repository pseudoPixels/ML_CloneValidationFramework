
from bs4 import BeautifulSoup
import os
import xml.etree.ElementTree as ET




class Utils:

    def __init__(self):
        self.nextCloneIndex = 0
        pass

    def get_next_clone_pair_for_validation(self, cloneFile, theValidationFile, validationFileExt='.validated'):
        # getting the example program name
        theCloneFile = cloneFile
        # theValidationFile = theCloneFile + validationFileExt

        # tree2 = ET.parse(cloneFile)
        # root = tree2.getroot()

        soup = ''
        with open(cloneFile) as fp:
            soup = BeautifulSoup(fp, 'lxml')

        root = soup.find_all('clone')








        src = root[self.nextCloneIndex].find_all('source')

        fragment_1_file = src[0]['file']
        fragment_1_strt = src[0]['startline']
        fragment_1_end = src[0]['endline']

        fragment_2_file = src[1]['file']
        fragment_2_strt = src[1]['startline']
        fragment_2_end = src[1]['endline']

        codes = root[self.nextCloneIndex].find_all('code')

        fragment_1_code = codes[0].text
        fragment_2_code = codes[1].text

        #print fragment_1_strt

        if os.path.exists(theValidationFile) == True:
            # response_code = 'FILE_ALREADY_EXIST'
            nextCloneIndex = sum(1 for line in open(theValidationFile))
        else:
            new_file = open(theValidationFile, "w")
            new_file.close()

        self.nextCloneIndex += 1
        # fragment_1_path, fragment_1_startline, fragment_1_endline, fragment_1_clone, fragment_2_path, fragment_2_startline, fragment_2_endline, fragment_2_clone, number_of_validated_clones, total_clones
        return fragment_1_file, fragment_1_strt, \
               fragment_1_end, fragment_1_code, fragment_2_file, fragment_2_strt, fragment_2_end, \
               fragment_2_code, self.nextCloneIndex, len(root)




    def read_file_in_line_range(self, filePath, startLine, endLine):
        fileContent = ''
        with open(filePath) as f:
            fileContent = ''.join(f.readlines()[int(startLine):int(endLine)])

        return fileContent


    def write_a_clone_fragment(self, outputFile, sourcePath, startLine, endLine, cloneFragment):
        with open(outputFile, "a") as file:

            file.write('<source file="' + sourcePath + '" startline= "' + str(
                startLine) + '" endline= "' + str(endLine) + '" />\n')
            file.write("<code>\n")
            file.write(str(cloneFragment).encode('utf-8'))
            file.write("</code>\n")



    def parse_and_format_clone_pairs_from_nicad_clone_file(self, nicadCloneFile):

        tree = ET.parse(nicadCloneFile)
        root = tree.getroot()

        formatedCloneFile = nicadCloneFile + '.xml'

        if os.path.exists(formatedCloneFile) == True:
            os.remove(formatedCloneFile)


        with open(formatedCloneFile, "a") as file:
            file.write("<clones>\n")


        for aClone in root.findall('clone'):
            with open(formatedCloneFile, "a") as file:
                file.write("<clone>\n")
            fragment_1_path = aClone[0].attrib['file']
            fragment_1_start_line = int(aClone[0].attrib['startline'])
            fragment_1_end_line = int(aClone[0].attrib['endline'])

            fragment_2_path = aClone[1].attrib['file']
            fragment_2_start_line = int(aClone[1].attrib['startline'])
            fragment_2_end_line = int(aClone[1].attrib['endline'])

            clone_fragment_1 = self.read_file_in_line_range('input_clone_pairs/'+fragment_1_path, fragment_1_start_line, fragment_1_end_line)

            clone_fragment_2 = self.read_file_in_line_range('input_clone_pairs/'+fragment_2_path, fragment_2_start_line, fragment_2_end_line)



            self.write_a_clone_fragment(formatedCloneFile, fragment_1_path, fragment_1_start_line, fragment_1_end_line, clone_fragment_1)
            self.write_a_clone_fragment(formatedCloneFile, fragment_2_path, fragment_2_start_line, fragment_2_end_line, clone_fragment_2)

            with open(formatedCloneFile, "a") as file:
                file.write("</clone>\n")

        with open(formatedCloneFile, "a") as file:
            file.write("</clones>")


        return formatedCloneFile