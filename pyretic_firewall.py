'''
    Coursera:
    - Software Defined Networking (SDN) course
    -- Module 6 Programming Assignment
    
    Professor: Nick Feamster
    Teaching Assistant: Arpit Gupta
'''

################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

from pyretic.modules.mac_learner import mac_learner
import os
import csv

# insert the name of the module and policy you want to import
#from pyretic.examples.<....> import <....>
policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]

def main():
    # Copy the code you used to read firewall-policies.csv from the Pox Firewall assignment
    acl_rules = []
    f = open(policy_file, "rb")
    freader = csv.reader(f)
    rn = 0
    for rule in freader:
        if rn == 0:
            rn += 1
            continue
        acl_rules.append((rule[1], rule[2]))
        rn += 1
    f.close()
    

    # start with a policy that doesn't match any packets
    not_allowed = none

    # and add traffic that isn't allowed
    for rule in acl_rules:
        not_allowed = union([not_allowed,(union([ \
        match(srcmac=MAC(rule[0]),dstmac=MAC(rule[1])),\
        match(srcmac=MAC(rule[1]),dstmac=MAC(rule[0]))\
        ]))])

    # express allowed traffic in terms of not_allowed - hint use '~'
    allowed = ~not_allowed

    '''
    print "not_allowed:\n"
    print not_allowed
    print "allowed:\n"
    print allowed
    '''

    # and only send allowed traffic to the mac learning (act_like_switch) logic
    return allowed >> mac_learner()



