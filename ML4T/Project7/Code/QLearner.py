""" 			  		 			     			  	   		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
import random as rand 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
class QLearner(object): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False): 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
        self.verbose = verbose 			  		 			     			  	   		   	  			  	
        self.num_actions = num_actions 			  		 			     			  	   		   	  			  	
        self.s = 0 			  		 			     			  	   		   	  			  	
        self.a = 0
        self.num_states = num_states
        self.rar =rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        self.q_table = np.zeros([num_states, num_actions])
        self.exptuple =[]



    def author(self):
        return 'aawasthi32'


    '''
    def dynaQ(self ,s,a,s_prime,r):

        
        #tc = np.full((self.num_states,self.num_actions,self.num_states), 0.00001)
        self.tc[s,a,s_prime] = self.tc[s,a,s_prime] + 1
        #T = np.zeros((self.num_states,self.num_actions,self.num_states))

        #R = np.zeros((self.num_states,self.num_actions))

        self.T[s,a,s_prime] = np.around(self.tc[s,a ,s_prime] /np.sum(self.tc[s,a]))

        #print "here I am **********************"

        #print np.around(tc[s,a ,s_prime] /np.sum(tc[s,a]))

        self.R[s , a] = (1-self.alpha) * self.R[s,a] + self.alpha * r

        #p = (self.tc[st, ac] / np.sum(self.tc[st, ac]))[0]

        #hallucinate

        for i in range(self.dyna):

            st =  rand.randint(0, self.num_states-1)
            ac =  rand.randint(0, self.num_actions-1)


            #print "ST Prime here I come............"
            #print np.random.choice(100, 1, p.all())
            #print np.random.choice(100, 1, p.all())
            #st_prime = np.random.choice(100, 1, p)

            late_reward = self.q_table[st_prime,np.argmax(self.q_table[st_prime])]

            rt = self.R[st,ac]
            self.q_table[self.s, self.a] = (1 - self.alpha) * self.q_table[st,ac] + self.alpha * (
                        rt + self.gamma * late_reward)

    '''

 			  		 			     			  	   		   	  			  	
    def querysetstate(self, s): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			     			  	   		   	  			  	
        @param s: The new state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        self.s = s
        if rand.uniform(0, 1) < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.q_table[s])

        if self.verbose: print "s =", s,"a =",action
        #self.a = action
        return action


 			  		 			     			  	   		   	  			  	
    def query(self,s_prime,r): 			  		 			     			  	   		   	  			  	
        """ 			  		 			     			  	   		   	  			  	
        @summary: Update the Q table and return an action 			  		 			     			  	   		   	  			  	
        @param s_prime: The new state 			  		 			     			  	   		   	  			  	
        @param r: The ne state 			  		 			     			  	   		   	  			  	
        @returns: The selected action 			  		 			     			  	   		   	  			  	
        """

        old_state = self.s
        old_action = self.a


        later_reward = self.q_table[s_prime,np.argmax(self.q_table[s_prime])]


        self.q_table[self.s,self.a] = (1-self.alpha)*self.q_table[old_state,old_action] + self.alpha *(r + self.gamma*later_reward)

        a_prime = self.querysetstate(s_prime)
        self.rar = self.rar * self.radr


        #Implementing Dyna using Experience Replay

        self.exptuple.append([old_state,old_action, s_prime, r])

        if self.dyna > 0:
            samples = np.random.choice(len(self.exptuple), size = self.dyna)
            for i in samples:
                st,ac,st_prime,rt = self.exptuple[i]
                dyna_reward = self.q_table[st_prime, np.argmax(self.q_table[st_prime])]
                self.q_table[st, ac] = (1 - self.alpha) * self.q_table[st,ac] + self.alpha * (rt + self.gamma * dyna_reward)



        self.s = s_prime
        self.a = a_prime

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r

        return a_prime


 			  		 			     			  	   		   	  			  	
if __name__=="__main__": 			  		 			     			  	   		   	  			  	
    print "Remember Q from Star Trek? Well, this isn't him" 			  		 			     			  	   		   	  			  	
