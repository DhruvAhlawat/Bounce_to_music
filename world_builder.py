#gotta create the world here.
import play as m
import keyboard
import sys
import pickle
import numpy as np

def build_world_time_patch(frame_seq, curnum):
    #we will try two orientations, and pick the one that works! I do hope that one of them works, but it probably should.
    if(curnum >= len(frame_seq)):
        return True;
    curframe = frame_seq[curnum];
    
