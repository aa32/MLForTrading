"""  		   	  			    		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
Student Name: Anshuta Awasthi
GT User ID: aawasthi32
GT ID: 903379179		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
from scipy import stats
  		   	  			    		  		  		    	 		 		   		 		  
class BagLearner(object):

    def __init__(self,learner,verbose=False,kwargs={},bags = 20,boost=False):
        self.learners = []
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        for i in range (bags):
          self.learners.append(learner(**kwargs))

    def author(self):
        return 'aawasthi32'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        numrow = dataX.shape[0]
        for l in self.learners:
          randIndexes = np.random.choice(numrow, numrow,replace = True)
          #print '#############################################################'
          #print randIndexes
          dataX = dataX[randIndexes,:]
          dataY = dataY[randIndexes]
          l.addEvidence(dataX,dataY)
          

        return self.learners
          
          
         


    def query(self, points):
      """
      @summary: Estimate a set of test points given the model we built.
      @param points: should be a numpy array with each row corresponding to a specific query.
      @returns the estimated values according to the saved model.
      """
      if self.verbose:
        print self.learners
      p = []
      for l in self.learners:
        y = l.query(points)
        p.append(y)
      q = np.vstack(p)
      return stats.mode(q,axis = 0)[0]

        
      

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

