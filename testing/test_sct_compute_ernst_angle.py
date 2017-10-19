#!/usr/bin/env python
#########################################################################################
#
# Test function for sct_compute_ernst_angle
#
# ---------------------------------------------------------------------------------------
# Copyright (c) 2017 Polytechnique Montreal <www.neuro.polymtl.ca>
# Author: Julien Cohen-Adad
#
# About the license: see the file LICENSE.TXT
#########################################################################################

def init(param_test):
     """
     Initialize class: param_test
     """
     # initialization
     default_args = ['-tr 2000 -t1 850 -o ernst_angle.txt']
     param_test.angle_gt = 84.543553255
     param_test.threshold = 0.00001
     # assign default params
     if not param_test.args:
          param_test.args = default_args
     return param_test


def test_integrity(param_test):
     """
     Test integrity of function
     """
     try:
          # open result file
          f = open('ernst_angle.txt', 'r')
          angle_result = float(f.read())
          f.close()
          # compare with GT
          if abs(angle_result - param_test.angle_gt) < param_test.threshold:
               param_test.output = 'PASS'
          else:
               param_test.output = 'FAIL'
               param_test.status = 99
     except Exception as err:
          param_test.status = 99
          param_test.output += str(err)

     return param_test