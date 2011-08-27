'''
Created on Aug 27, 2011

@author: daniel
'''
import os
import psutil
import signal
import sys

class Util:
    #A function which will cleanly exit from the server program.
    @staticmethod
    def clean_exit(exit_code):
        pid = os.getpid()
        parent = psutil.Process(pid)
        
        for child in parent.get_children():
            if os.name == 'posix':
                child.send_signal(signal.SIGINT)
            else:
                child.send_signal(signal.SIGTERM)
        
        sys.exit(exit_code)
