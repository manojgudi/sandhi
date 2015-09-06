#!/usr/bin/env python
"""

    Copyright 2015
    FOSSEE, IIT Bombay
    Use is subject to license terms.

    @version    0.2, 15-Aug-2015
    @author     Manoj G
    @email      manoj.p.gudi@gmail.com

    Test Module to check scilab's generic block
"""
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
import numpy

from gnuradio import gr, gr_unittest
from scigen import Generic

class qa_generic (gr_unittest.TestCase):
    '''
    Block to test Generic class from scigen module
    '''

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        src0 = numpy.arange(0,3.1416,1)

        src0 = gr.vector_source_f(src0)
        expected_result = (0.0, 0.8414709568023682, 0.9092974066734314, 0.14112000167369843)

        gen_instance = Generic("sin", 1)


        dst = gr.vector_sink_f()


        self.tb.connect(src0, (gen_instance,0)) # src0(vector_source) -> gen_instance_input_0
        self.tb.connect(gen_instance,dst) # gen_instance_output_0 -> dst (vector_source)

        self.tb.run()

        result_data = dst.data()
        print result_data, "Result data"

        self.assertFloatTuplesAlmostEqual(expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.main()

