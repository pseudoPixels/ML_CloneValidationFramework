import pickle
from mlCVF.TXLHelper import TXLHelper




class MLHelper:

    def __init__(self):
        self.txlHelper = TXLHelper()


    def app_code_clone_getValidationScore(self, sourceCode1, sourceCode2, lang='java', trainedModel='trainedNetwork'):
        # load the trained Neural Net
        fileObject = open('pybrain/'+trainedModel, 'rb')
        loaded_fnn = pickle.load(fileObject)

        type1sim_by_line, type2sim_by_line, type3sim_by_line = self.txlHelper.app_code_clone_similaritiesNormalizedByLine(sourceCode1,
                                                                                                           sourceCode2,
                                                                                                           lang)
        type1sim_by_token, type2sim_by_token, type3sim_by_token = self.txlHelper.app_code_clone_similaritiesNormalizedByToken(
            sourceCode1, sourceCode2, lang)

        # type2sim_by_line, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token
        # network_prediction = loaded_fnn.activate([0.2,0.5,0.6,0.1,0.3,0.7])
        network_prediction = loaded_fnn.activate(
            [type2sim_by_line, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token])

        # out = {'false_clone_probability_score':network_prediction[0], 'true_clone_probability_score':network_prediction[1]}

        # return jsonify({'error_msg': 'None', 'log_msg': 'Preprocessing Source Codes...\nNormalizing Source Codes...\nCalculating Similarities...\nDone.','output': out})

        # true_clone_probability_score
        return network_prediction[1]
