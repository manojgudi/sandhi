"""

    Copyright 2015
    FOSSEE, IIT Bombay
    Use is subject to license terms.

    @version    0.1, 04-Oct-2015
    @author     Manoj G
    @email      manoj.p.gudi@gmail.com

    A State innovation block of Kalman Filter module
"""
import gras
import numpy

class StateInnovation(gras.Block):
    '''
        State Innovation block
        Required Paramters:
            H: Observation Matrix

        Inputs:
            measurement vector zn
    '''
    def __init__(self, _H):
        gras.Block.__init__(self,
            name="state_innovation",
            # XXX Should this change for a matrix input
            in_sig=[numpy.float32, numpy.float32],
            out_sig=[numpy.float32])

        # XXX How to prefetch x0 matrix (can x0 be passed as a parameter 
            #and work function will use it once)

        # Variables
        self.H = _H

    # XXX Add functions to validate sie and nature of inputs(non signular matrix A,B etc..)

    def work(self, input_items, output_items):


        # Get (input) control vector and measurement vector
        xn = input_items[0][:]
        zn = input_items[1][:]

        # Get xn prediction
        y_ = zn - H*xn

        # Limit output_items to just the size of window
        output_items[0][:] = y_

        # Check number of input_instances
        n_input_items = len(input_items)

        # XXX Check consume and produce logic

        #Write a for loop for n_inputs
        for i in range(n_input_items):
            self.consume(i)

        self.produce(0, len(y_)) # Produce from port 0 output_items
