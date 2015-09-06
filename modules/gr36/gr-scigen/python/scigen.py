"""

    Copyright 2015
    FOSSEE, IIT Bombay
    Use is subject to license terms.

    @version    0.2, 15-Aug-2015
    @author     Manoj G
    @email      manoj.p.gudi@gmail.com

    A generic block to call scilab functions which uses sciscipy wrapper
"""
import gras
import numpy

from scilab import Scilab

class Generic(gras.Block):
    '''
    Scilab Generic class
        - inherits gras.Block
        - used to call scilab functions
        window_size is size of inputs the function will be called
    '''
    def __init__(self, func_name, window_size):
        gras.Block.__init__(self,
            name="generic",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])

        self.window_size     = window_size
        self.func_name       = func_name
        self.scilab_instance = Scilab()

    def is_window_integral(self, input_item, window):
        """
        Check if value of window is integral of length of input source vector
        For cases like -> input = [3 , 4, 5 ,6] & window = 3
        """
        if (len(input_item) % window ):
            raise Exception("Value of Window should be an integral value of length of input items")

    def work(self, input_items, output_items):

        # Limit output_items to just the size of window
        output_items[0][:] = output_items[0][:self.window_size]

        # Check number of input_instances
        n_input_items = len(input_items)

        # Create output string instance which will be evaluated
        out_eval_string = 'eval("self.scilab_instance.'+self.func_name+'('

        # Iterate for n_input_items
        for i in range(n_input_items):

            # Check window condition
            self.is_window_integral(input_items[i][:], self.window_size)

            # If the window is greater than 1, 
            # input_items[i][:self.window_size] looks like [1   2   3   4   5] which is err for python since it requires comma as delimiters 
            if self.window_size == 1:
                """
                The hell is going on here?
                """
                out_eval_string = out_eval_string + str(input_items[i][:self.window_size]) + ","
            else:
                print 'IN',str(input_items[i][:self.window_size])
                out_eval_string = out_eval_string + (str(input_items[i][:self.window_size].tolist()))  + ","  # Replace 10spaces with a singe comma

        out_eval_string = out_eval_string.rstrip(",") + ')")'
        print "From Scilab",str(out_eval_string)

        # for functions like sin
        if n_input_items == 1 and self.window_size == 1:
            output_items[0][:self.window_size] = eval(out_eval_string)
        else:
            output_items[0] = eval(out_eval_string)

        print "OUT ",output_items[0]

        #Write a for loop for n_inputs
        for i in range(n_input_items):
            self.consume(i,self.window_size) # Consume from port 0 input_items

        self.produce(0,self.window_size) # Produce from port 0 output_items

