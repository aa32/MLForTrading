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
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class DTLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  np.seterr(divide='ignore', invalid='ignore') 
  def __init__(self,leaf_size=1,verbose = False):
    self.leaf_size = leaf_size
    self.verbose = verbose
    self.tree = []
  		   	  			    		  		  		    	 		 		   		 		  
  def author(self):  		   	  			    		  		  		    	 		 		   		 		  
    return 'aawasthi32' # replace tb34 with your Georgia Tech username


  		   	  			    		  		  		    	 		 		   		 		  
  def addEvidence(self,dataX,dataY):
    	   	  			    		  		  		    	 		 		   		 		  
    """  		   	  			    		  		  		    	 		 		   		 		  
    @summary: Add training data to learner  		   	  			    		  		  		    	 		 		   		 		  
    @param dataX: X values of data to add  		   	  			    		  		  		    	 		 		   		 		  
    @param dataY: the Y training values  		   	  			    		  		  		    	 		 		   		 		  
    """  		   	  			    		  		  	
    if dataX.shape[0] == 1:
      self.tree = np.array([[-1,dataY[0,0],-1,-1]])
      return self.tree

    elif len(np.unique(dataY))<=1:
      self.tree = np.array([[-1,dataY.mean(),-1,-1]])
      return self.tree
    
    elif	 dataX.shape[0] <= self.leaf_size :
      self.tree = np.array([[-1,dataY.mean(),-1,-1]])
      return self.tree

    else:
      numcol = dataX.shape[1]
      correlarr = np.zeros(numcol)
      for i in range(numcol):
        correl = np.corrcoef(dataX[:, i], dataY)
        correlarr[i] = abs(correl[0][1])

      factor = np.nanargmax(correlarr)
      val = max(correlarr)
      
      splitVal = np.median(dataX[:,factor])
      splitData = dataX[:,factor]

      leftIndices = np.nonzero(splitData <= splitVal)
      rightIndices = np.nonzero(splitData > splitVal)

      if (np.size(rightIndices) == 0):
        self.tree = np.array([[-1,dataY.mean(),-1,-1]])
        return self.tree
        
      elif (np.size(leftIndices) == 0):
        self.tree = np.array([[-1,dataY.mean(),-1,-1]])
        return self.tree
        
      leftdataX = dataX[leftIndices]
      leftdataY = np.take(dataY,leftIndices)

      rightdataX = dataX[rightIndices]
      rightdataY = np.take(dataY, rightIndices)

      leftTree = self.addEvidence(leftdataX,leftdataY)
      rightTree = self.addEvidence(rightdataX,rightdataY)

      if(np.ndim(leftTree)==1):
        root = np.array([[factor, splitVal, 1, 2]])
      else:
        root = np.array([[factor, splitVal, 1, leftTree.shape[0]+1]])

      tree = np.append(root,leftTree,axis =0)
      tree = np.append(tree,rightTree,axis =0)
      self.tree = tree

      return self.tree
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  def query(self,points):  		   	  			    		  		  		    	 		 		   		 		  
    """
    @summary: Estimate a set of test points given the model we built.  		   	  			    		  		  		    	 		 		   		 		  
    @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			    		  		  		    	 		 		   		 		  
    @returns the estimated values according to the saved model.  		   	  			    		  		  		    	 		 		   		 		  
    """

    if self.verbose:
      print self.tree
    Y=[]
    for point in points:
      Yval = self.tree_traverse(point,level =0)
      Y.append(Yval) 
    return Y


  def tree_traverse(self,point,level):
    factor = int(self.tree[level][0])
    splitVal = self.tree[level][1]
    if (factor == -1):
      return splitVal

    elif (point[factor] <= splitVal):
      Yval = self.tree_traverse(point,level+ int(self.tree[level][2]))
      return Yval

    else:
      Yval = self.tree_traverse(point,level+int(self.tree[level][3]))
      return Yval
      
        		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"  		   	  			    		  		  		    	 		 		   		 		  
