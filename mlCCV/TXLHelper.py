import subprocess
import os
import uuid






class TXLHelper:

    def __init__(self):
        pass

    def app_code_clone_execTxl(self, txlFilePath, sourceCode, lang, saveOutputFile=False):
        # get an unique file name for storing the code temporarily
        fileName = str(uuid.uuid4())
        sourceFile = 'txl_tmp_file_dir/' + fileName + '.txt'

        # write submitted source code to corresponding files
        with open(sourceFile, "w") as fo:
            fo.write(sourceCode)

        # get the required txl file for feature extraction
        # txlPath = '/home/ubuntu/Webpage/txl_features/txl_features/java/PrettyPrint.txl'

        # do the feature extraction by txl
        p = subprocess.Popen(['/usr/local/bin/txl', '-Dapply', txlFilePath, sourceFile], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        # convert to utf-8 format for easier readibility
        # out = str(out, 'utf-8')
        # err = str(err, 'utf-8')

        out = str(out)
        err = str(err)

        err = err.replace(sourceFile, 'YOUR_SOURCE_FILE')
        err = err.replace(txlFilePath, 'REQUIRED_TXL_FILE')

        # once done remove the temp file
        os.remove(sourceFile)

        if saveOutputFile == False:
            return out, err
        else:
            outputFileLocation = str(uuid.uuid4())
            outputFileLocation = 'txl_tmp_file_dir/' + outputFileLocation + '.txt'
            with open(outputFileLocation, "w") as fo:
                fo.write(out)

            return outputFileLocation, out, err




    def app_code_clone_getCodeCloneSimilarity(self, sourceCode1, sourceCode2, lang, txlFilePath):
        saveOutputFile = True
        outputFileLocation1, out1, err1 = self.app_code_clone_execTxl(txlFilePath, sourceCode1, lang, saveOutputFile)
        outputFileLocation2, out2, err2 = self.app_code_clone_execTxl(txlFilePath, sourceCode2, lang, saveOutputFile)

        p = subprocess.Popen(['/usr/bin/java', '-jar', 'txl_tmp_file_dir/calculateCloneSimilarity.jar',
                              outputFileLocation1, outputFileLocation2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        similarityValue, err = p.communicate()

        #similarityValue = str(similarityValue, 'utf-8')
        similarityValue = str(similarityValue)
        similarityValue = similarityValue.replace('\n', '')
        #err = str(err, 'utf-8')
        err = str(err)


        # once done remove the temp files
        os.remove(outputFileLocation1)
        os.remove(outputFileLocation2)

        return similarityValue



    def app_code_clone_similaritiesNormalizedByLine(self, sourceCode1, sourceCode2, lang):
        # getting the txl and the input file to parse
        # sourceCode1 = request.form['sourceCode_1']
        # sourceCode2 = request.form['sourceCode_2']
        # lang = request.form['lang']

        txlFilePath = 'txl_features/txl_features/java/PrettyPrint.txl'
        type1sim_by_line = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToDefault.txl'
        type2sim_by_line = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
        type3sim_by_line = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        #out = {'type_1_similarity_by_line': type1sim_by_line, 'type_2_similarity_by_line': type2sim_by_line,
        #	   'type_3_similarity_by_line': type3sim_by_line}

        #return jsonify({'error_msg': 'None',
        #				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
        #				'output': out})

        return type1sim_by_line, type2sim_by_line, type3sim_by_line



    def app_code_clone_similaritiesNormalizedByToken(self, sourceCode1, sourceCode2, lang):
        # getting the txl and the input file to parse
        # sourceCode1 = request.form['sourceCode_1']
        # sourceCode2 = request.form['sourceCode_2']
        # lang = request.form['lang']

        txlFilePath = 'txl_features/txl_features/java/consistentRenameIdentifiers.txl'
        type1sim_by_token = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
        type2sim_by_token = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        txlFilePath = 'txl_features/txl_features/java/normalizeLiteralsToZero.txl'
        type3sim_by_token = self.app_code_clone_getCodeCloneSimilarity(sourceCode1, sourceCode2, lang, txlFilePath)

        # out = {'type_1_similarity_by_token': type1sim_by_token, 'type_2_similarity_by_token': type2sim_by_token,
        # 	   'type_3_similarity_by_token': type3sim_by_token}
        #
        # return jsonify({'error_msg': 'None',
        # 				'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.',
        # 				'output': out})

        return type1sim_by_token, type2sim_by_token, type3sim_by_token


