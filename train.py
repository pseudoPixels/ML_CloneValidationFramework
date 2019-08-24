from scipy import diag
import pandas as pd
import numpy as np
from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

import pickle
from mlCVF.TXLHelper import TXLHelper
import argparse







def read_file_in_line_range(filePath, startLine, endLine):
    fileContent = ''
    with open(filePath) as f:
        fileContent = ''.join(f.readlines()[int(startLine):int(endLine)])

    return fileContent

def run(args):
    manual_validated_file = args.manual_validated_file # 'JHotDraw54b1_clones.xml.clones2'
    save_target_name = args.save_target_name #'newTrainedModel'



    print 'Training the Model. Please wait ...'

    manual_validation_data = pd.read_csv('manual_validator/input_clone_pairs/'+manual_validated_file)
    inputDim = 6
    alldata = ClassificationDataSet(inputDim, 1, nb_classes=2)
    txlHelper = TXLHelper()
    for i in range(0, len(manual_validation_data)):
        #print manual_validation_data.iloc[i][3], manual_validation_data.iloc[i][4]
        #print manual_validation_data.iloc[i][2]
        cloneFragment_1_path, cloneFragment_1_start, cloneFragment_1_end = manual_validation_data.iloc[i][3].split()[0], \
                                                                           manual_validation_data.iloc[i][3].split()[1], \
                                                                           manual_validation_data.iloc[i][3].split()[2]
        cloneFragment_2_path, cloneFragment_2_start, cloneFragment_2_end = manual_validation_data.iloc[i][4].split()[0], \
                                                                           manual_validation_data.iloc[i][4].split()[1], \
                                                                           manual_validation_data.iloc[i][4].split()[2]
        cloneFragment_1 = read_file_in_line_range(filePath='manual_validator/input_clone_pairs/'+cloneFragment_1_path, \
                                                  startLine=cloneFragment_1_start, endLine=cloneFragment_1_end)
        cloneFragment_2 = read_file_in_line_range(filePath='manual_validator/input_clone_pairs/' + cloneFragment_2_path,
                                                  startLine=cloneFragment_2_start, endLine=cloneFragment_2_end)


        type1sim_by_line, type2sim_by_line, type3sim_by_line = txlHelper.app_code_clone_similaritiesNormalizedByLine(cloneFragment_1,
                                                     cloneFragment_2, 'java')

        type1sim_by_token, type2sim_by_token, type3sim_by_token = txlHelper.app_code_clone_similaritiesNormalizedByToken(cloneFragment_1,
                                                     cloneFragment_2, 'java')

        label = manual_validation_data.iloc[i][2]
        if label == 'true':
            label = 1
        else:
            label = 0



        input = np.array([type1sim_by_token, type2sim_by_line, type3sim_by_line, type1sim_by_token, type2sim_by_token, type3sim_by_token])

        alldata.addSample(input, int(label))



    # # np.nan_to_num(alldata)
    # # alldata = alldata[~np.isnan(alldata)]
    # #alldata.fillna(0)
    # np.set_printoptions(precision=3)
    # print alldata

    #
    # def load_training_dataSet(fileName):
    #     data = pd.read_csv(fileName, sep=',', header=None)
    #     #data.columns = ["state", "outcome"]
    #     return data
    #
    # myclones_data = load_training_dataSet('Datasets/new_dataset_with_new_features.csv')
    # myclones_data = myclones_data.values
    #
    #
    # inputDim = 6
    #
    #
    # means = [(-1,0),(2,4),(3,1)]
    # cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
    # alldata = ClassificationDataSet(inputDim, 1, nb_classes=2)
    #
    #
    # #input = np.array([ myclones_data[n][16], myclones_data[n][17], myclones_data[n][18], myclones_data[n][15],myclones_data[n][11],myclones_data[n][12],   myclones_data[n][26], myclones_data[n][27]] )
    #
    # for n in xrange(len(myclones_data)):
    #     #for klass in range(3):
    #     input = np.array(
    #         [myclones_data[n][11], myclones_data[n][17], myclones_data[n][12], myclones_data[n][15], myclones_data[n][18],
    #          myclones_data[n][16]])
    #     #print (n, "-->", input)
    #     alldata.addSample(input, int(myclones_data[n][35]))
    #
    #
    tstdata, trndata = alldata.splitWithProportion( 0.25 )

    #print(tstdata)

    tstdata_new = ClassificationDataSet(inputDim, 1, nb_classes=2)
    for n in xrange(0, tstdata.getLength()):
        tstdata_new.addSample( tstdata.getSample(n)[0], tstdata.getSample(n)[1] )

    trndata_new = ClassificationDataSet(inputDim, 1, nb_classes=2)
    for n in xrange(0, trndata.getLength()):
        trndata_new.addSample( trndata.getSample(n)[0], trndata.getSample(n)[1])

    trndata = trndata_new
    tstdata = tstdata_new

    #print("Before --> ", trndata)

    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )



    fnn = buildNetwork( trndata.indim, 107, trndata.outdim, outclass=SoftmaxLayer )
    trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1,learningrate=0.05 , verbose=True, weightdecay=0.001)



    #print "Printing Non-Trained Network..."






    """
    ticks = arange(-3.,6.,0.2)
    X, Y = meshgrid(ticks, ticks)
    # need column vectors in dataset, not arrays
    griddata = ClassificationDataSet(7,1, nb_classes=2)
    for i in xrange(X.size):
        griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
    griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy
    
    """



    #trainer.trainEpochs(1)
    #trainer.testOnData(verbose=True)
    #print(np.array([fnn.activate(x) for x, _ in tstdata]))





    for i in range(1):
        trainer.trainEpochs(10)
        trnresult = percentError(trainer.testOnClassData(),
                                 trndata['class'])
        tstresult = percentError(trainer.testOnClassData(
            dataset=tstdata), tstdata['class'])




        #print "epoch: %4d" % trainer.totalepochs, \
        #    "  train error: %5.2f%%" % trnresult, \
         #   "  test error: %5.2f%%" % tstresult


    #print "Printing Trained Network..."
    #print fnn.params


    print "Saving the trined Model at : ", 'pybrain/'+save_target_name
    #saving the trained network...
    import pickle

    fileObject = open('pybrain/'+save_target_name, 'w')

    pickle.dump(fnn, fileObject)
    fileObject.close()

    #
    # fileObject = open('trainedNetwork79', 'r')
    # loaded_fnn = pickle.load(fileObject)
    #
    #
    # print "Printing the result prediction..."
    #
    # print loaded_fnn.activate([0.2,0.5,0.6,0.1,0.3,0.7])
    #
    # print fnn.activate([0.2,0.5,0.6,0.1,0.3,0.7])
    #


        #out = fnn.activateOnDataset(griddata)
        #out = out.argmax(axis=1)  # the highest output activation gives the class
        #out = out.reshape(X.shape)

    """
    
        figure(1)
        ioff()  # interactive graphics off
        clf()  # clear the plot
        hold(True)  # overplot on
        for c in [0, 1, 2]:
            here, _ = where(tstdata['class'] == c)
            plot(tstdata['input'][here, 0], tstdata['input'][here, 1], 'o')
        if out.max() != out.min():  # safety check against flat field
            contourf(X, Y, out)  # plot the contour
        ion()  # interactive graphics on
        draw()  # update the plot
    
    ioff()
    show()
    """

def main():
    parser = argparse.ArgumentParser(description="This is a machine learning based framework for automatic code clone validation.")
    parser.add_argument("-in", help="(required) validated input clone file (i.e., output file from manual validation)", dest="manual_validated_file", type=str, required=True, default="JHotDraw54b1_clones.xml.clones2")
    parser.add_argument("-out", help="(required) save output name for the newly trained model", dest="save_target_name", type=str, required=True, default="latestTrainedModel")
    #parser.add_argument("-t", help="(optional) the threshold for automatic clone validation. Default=0.7", dest="val_threshold", type=float, default=0.7)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()