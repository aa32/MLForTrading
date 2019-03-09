"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bal
import InsaneLearner as it
import util
import sys
import math
import pandas as pd
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def author():
    return 'aawasthi32'
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    datafile = "Istanbul.csv"

    # compute how much of the data is training and testing
    testX,testY,trainX,trainY = None,None, None,None                                                                                              
    permutation = None
    np.random.seed(874327890)
                                                                                           
    with util.get_learner_data_file(datafile) as f:                                                                                               
        alldata = np.genfromtxt(f,delimiter=',')                                                                                              
            # Skip the date column and header row if we're working on Istanbul data                                                                                               
                                                                                                       
        alldata = alldata[1:,1:]                                                                                              
        datasize = alldata.shape[0]
        cutoff = int(datasize*0.6)  
        permutation = np.random.permutation(alldata.shape[0])                                                                                                                                                                                  
        train_data = alldata[permutation[:cutoff],:]                                                                                              
            # trainX = train_data[:,:-1]                                                                                              
        trainX = train_data[:,0:-1]                                                                                                
        trainY = train_data[:,-1]  


                                                                                         
        test_data = alldata[permutation[cutoff:],:]                                                                                               
        # testX = test_data[:,:-1]                                                                                                
        testX = test_data[:,0:-1]                                                                                              
        testY = test_data[:,-1]  




    '''
    ************************************************************************************************
    Graph for report question 1
    ***************************************************************************************************
    '''


    
    rmse_train = np.array([])
    rmse_test = np.array([])
    



    for i in xrange (1,51):

        learner = dtl.DTLearner(leaf_size =i,verbose = False)
        learner.addEvidence(trainX,trainY) # train it 
        predY = learner.query(trainX)                                                                                                                                                                                  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])                                                                                               
        rmse_train = np.append(rmse_train,rmse)


                                                                                              
        # evaluate out of sample 
        predY = learner.query(testX) # get the predictions                                                                                                
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        rmse_test = np.append(rmse_test,rmse)



    plt.figure(1)
    plt.title('RMSE Vs Leaf Size for DT Learner Bootstrapping')
    plt.plot(rmse_train ,label ='In Sample')
    plt.plot(rmse_test,label ='Out of Sample')
    plt.xlim(51,1 )
    plt.legend(loc = 'lower left')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('fig1')

    '''
    **************************************************************************************************************
    Graph for report question 2
    *************************************************************************************************************
    '''
    
    rmse1_train = np.array([])
    rmse1_test = np.array([])
    for j in xrange (1,101):
        
        learner1 = bal.BagLearner(learner = dtl.DTLearner,verbose=False, kwargs={"leaf_size": j}, bags = 20, boost=False) # create a DT
        learner1.addEvidence(trainX,trainY) # train it 
        predY1 = learner1.query(trainX)                                                                                                                                                                                  
        rmse1 = math.sqrt(((trainY - predY1) ** 2).sum()/trainY.shape[0])                                                                                               
        rmse1_train = np.append(rmse1_train,rmse1)

                                                                                              
                                                                                              
        # evaluate out of sample 
        predY1 = learner1.query(testX) # get the predictions                                                                                                
        rmse1 = math.sqrt(((testY - predY1) ** 2).sum()/testY.shape[0])
        rmse1_test = np.append(rmse1_test,rmse1)

    plt.figure(2)
    plt.title('RMSE Vs Leaf Size for Bagging with DTLearner')
    plt.plot(rmse1_train ,label ='In Sample')
    plt.plot(rmse1_test,label ='Out of Sample')
    plt.xlim(101,1)
    plt.ylim(0.000,0.010)
    plt.legend(loc = 'lower left')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.grid(b=True, axis='y', linewidth = 1)
    plt.savefig('fig2')

    '''
    ******************************************************************************************************************************
    Graph for report question 3
    ******************************************************************************************************************************
    '''
    DT_Time = np.array([])
    RT_Time = np.array([])
 
    DT_Train = np.array([])
    RT_Train = np.array([])

    rmse_DT = np.array([])
    rmse_RT = np.array([])

    DTTree_depth = np.array([])
    RTTree_depth = np.array([])

    for i in xrange (1,51):
        # evaluate DT learner test
        learnerD = dtl.DTLearner(leaf_size =i,verbose = False)
        start_DT_train = time.time()
        learnerD.addEvidence(trainX,trainY) # train it 
        end_DT_train = time.time()
        time_DT_train = end_DT_train  - start_DT_train
        DT_depth = learnerD.tree.shape[0]
        DTTree_depth = np.append(DTTree_depth,DT_depth)

                                                                                              
        start_DT = time.time()
        predYD = learnerD.query(testX) # get the predictions
        end_DT = time.time()   
        time_DT = end_DT-start_DT                                                                                           
        rmseD = math.sqrt(((testY - predYD) ** 2).sum()/testY.shape[0])
        rmse_DT = np.append(rmse_DT,rmseD)
        DT_Time = np.append(DT_Time,time_DT)
        DT_Train = np.append(DT_Train , time_DT_train)

        #RT learner test
        learnerR = rtl.RTLearner(leaf_size =i,verbose = False)
        start_RT_train = time.time()
        learnerR.addEvidence(trainX,trainY) # train it 
        end_RT_train = time.time()
        time_RT_train = end_RT_train-start_RT_train

        RT_depth = learnerR.tree.shape[0]
        RTTree_depth = np.append(RTTree_depth ,RT_depth)


        start_RT =time.time()
        predYR = learnerR.query(testX) # get the predictions
        end_RT =time.time()
        time_RT = end_RT-start_RT                                                                                               
        rmseR = math.sqrt(((testY - predYR) ** 2).sum()/testY.shape[0])
        rmse_RT = np.append(rmse_RT,rmseR)
        RT_Time = np.append(RT_Time,time_RT)
        RT_Train = np.append(RT_Train,time_RT_train)



    plt.figure(3)
    plt.title('Query time comparison for DTLearner Vs RTLearner')
    plt.plot(DT_Time ,label ='DT Learner')
    plt.plot(RT_Time,label ='RT Learner')
    plt.xlim(51, 1)
    plt.legend(loc = 'upper left')
    plt.ylabel('Time')
    plt.xlabel('Leaf Size')
    plt.savefig('fig3')

    plt.figure(4)
    plt.title('Training time comparison for DTLearner Vs RTLearner')
    plt.plot(DT_Train ,label ='DT Learner')
    plt.plot(RT_Train,label ='RT Learner')
    plt.xlim(51, 1)
    plt.legend(loc = 'upper left')
    plt.ylabel('Time')
    plt.xlabel('Leaf Size')
    plt.savefig('fig4')


    plt.figure(5)
    plt.title('RMSE comparison for DTLearner Vs RTLearner')
    plt.plot(rmse_DT ,label ='DT Learner')
    plt.plot(rmse_RT,label ='RT Learner')
    plt.xlim(51, 1)
    plt.legend(loc = 'upper left')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('fig5')



    plt.figure(6)
    plt.title('Tree depth comparison for DTLearner Vs RTLearner')
    plt.plot(DTTree_depth ,label ='DT Learner')
    plt.plot(RTTree_depth,label ='RT Learner')
    plt.xlim(51, 1)
    plt.legend(loc = 'upper left')
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('fig6')


    '''
    *******************************************************************************************************************
    Test cases-Uncomment this portion if need to test
    ******************************************************************************************************************
    



    #create a RT learner and train it                                                                                             
    learner = rtl.RTLearner(verbose = True) # create a DTLearner
    tree = learner.addEvidence(trainX, trainY) # train it 
    #print "trained tree"
    #print tree
    predY = learner.query(trainX)                                                                                             
    print learner.author()                                                                                        
    # evaluate in sample                                                                                                                                                                                              
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])                                                                                               
    print "In sample results RT learner"                                                                                              
    print "RMSE: RT Learner", rmse                                                                                                
    c = np.corrcoef(predY, y=trainY)                                                                                              
    print "corr: ", c[0,1]                                                                                                
                                                                                              
    # evaluate out of sample                                                                                              
    predY = learner.query(testX) # get the predictions                                                                                                
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                             
    print                                                                                             
    print "Out of sample results RT Learner"                                                                                              
    print "RMSE: RTLearner", rmse                                                                                             
    c = np.corrcoef(predY, y=testY)                                                                                               
    print "corr: ", c[0,1] 




    #create a DT learner and train it                                                                                             
    learner = dtl.DTLearner(verbose = True) # create a DTLearner
    tree = learner.addEvidence(trainX, trainY) # train it 
    #print "trained tree"
    #print tree
    predY = learner.query(trainX)                                                                                             
    print learner.author()                                                                                        
    # evaluate in sample                                                                                                                                                                                              
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])                                                                                               
    print "In sample results DT learner"                                                                                              
    print "RMSE: DT Learner", rmse                                                                                                
    c = np.corrcoef(predY, y=trainY)                                                                                              
    print "corr: ", c[0,1]                                                                                                
                                                                                              
    # evaluate out of sample                                                                                              
    predY = learner.query(testX) # get the predictions                                                                                                
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                             
    print                                                                                             
    print "Out of sample results DT Learner"                                                                                              
    print "RMSE: DTLearner", rmse                                                                                             
    c = np.corrcoef(predY, y=testY)                                                                                               
    print "corr: ", c[0,1] 



    #create a bag learner with RTLearner and train it

    learner1 = bal.BagLearner(learner = dtl.DTLearner, kwargs={"leaf_size": 1}, bags = 20, boost=False, verbose=False)
    learner1.addEvidence(trainX, trainY)
    q_rv = learner1.query(testX)
    a_rv = learner1.author()

 
                                                                                                                                                              
    # evaluate in sample                                                                                              
    predY1 = learner1.query(trainX) # get the predictions                                                                                               
    rmse = math.sqrt(((trainY - predY1) ** 2).sum()/trainY.shape[0])
    print "In sample results1 Bag learner with DT"                                                                                             
    print "RMSE1: Bag Learner 1 ", rmse                                                                                              
    c = np.corrcoef(predY1, y=trainY)                                                                                              
    #print "corr1: ", c[0,1]                                                                                                
                                                                                              
    # evaluate out of sample                                                                                              
    predY1 = learner1.query(testX) # get the predictions                                                                                                
    rmse1 = math.sqrt(((testY - predY1) ** 2).sum()/testY.shape[0])                                                                                             
    print                                                                                             
    print "Out of sample results Bag learner With DT"                                                                                             
    print "RMSE:1 Bag Learner", rmse1                                                                                              
    c = np.corrcoef(predY1, y=testY)                                                                                               
    #print "corr: ", c[0,1] 
    


    #create insane learner

    learner3 = it.InsaneLearner(verbose = False) # constructor
    learner3.addEvidence(trainX, trainY) # training step
    Y = learner3.query(testX) # query

    # evaluate in sample                                                                                              
    predY3 = learner3.query(trainX) # get the predictions                                                                                               
    rmse3 = math.sqrt(((trainY - predY3) ** 2).sum()/trainY.shape[0])
    print "In sample results3"                                                                                             
    print "RMSE3: Insane Learner", rmse3                                                                                             
    c = np.corrcoef(predY3, y=trainY)                                                                                              
    print "corr1: ", c[0,1]                                                                                                
                                                                                              
    # evaluate out of sample                                                                                              
    predY3 = learner3.query(testX) # get the predictions                                                                                                
    rmse3 = math.sqrt(((testY - predY3) ** 2).sum()/testY.shape[0])                                                                                             
    print                                                                                             
    print "Out of sample results"                                                                                             
    print "RMSE:3 Insane Learner", rmse3                                                                                              
    c = np.corrcoef(predY3, y=testY)                                                                                               
    print "corr: ", c[0,1] 

    '''
    




   






        





    


    
    

    

