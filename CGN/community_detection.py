from __future__ import division
from __future__ import print_function

import os

# Train on CPU (hide GPU) due to memory constraints
# os.environ['CUDA_VISIBLE_DEVICES'] = ""



def community_detection(g,algorithm):
    if algorithm == "multilevel":
        community = g.community_multilevel()
        return community

    
