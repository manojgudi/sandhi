"""

    Copyright 2015
    FOSSEE, IIT Bombay
    Use is subject to license terms.

    @version    0.1, 04-Oct-2015
    @author     Manoj G
    @email      manoj.p.gudi@gmail.com

    A Covariance Prediction block of Kalman Filter module
"""
import gras
import numpy

from scilab import Scilab

class CovarPrediction(gras.Block):
    '''
        State Prediction block
        Required Paramters:
        A: State Transition Matirx
        Q: Process Error Covariance Matrix

        Inputs:
            previous covariance matrix(Pn_1)
        which gives out a covariance prediction Pn
    '''
    def __init__(self, _A, _Q):
        gras.Block.__init__(self,
            name="covar_prediction",
            # XXX Should this change for a matrix input
            in_sig=[numpy.float32, numpy.float32],
            out_sig=[numpy.float32])

        # XXX How to prefetch P0 matrix (can P0 be passed as a parameter 
            #and work function will use it once)

        # Variables
        self.A = _A  # State transition matrix
        self.Q = _Q  # Process Error Matrix


    # XXX Add functions to validate sie and nature of inputs(non signular matrix A,B etc..)

    def work(self, input_items, output_items):


        # Get (input) control vector and measurement vector
        Pn_1 = input_items[0][:]

        # Get xn prediction
        Pn = self.A*Pn_1*self.A.T + self.Q

        # Limit output_items to just the size of window
        output_items[0][:] = Pn

        # Check number of input_instances
        n_input_items = len(input_items)

        # XXX Check consume and produce logic

        #Write a for loop for n_inputs
        for i in range(n_input_items):
            self.consume(i)

        self.produce(0, len(Pn)) # Produce from port 0 output_items
