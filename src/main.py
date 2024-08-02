#!/usr/bin/env python3

import sys
import os


#set up path to include src and subdirectories for imports in other scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = current_dir
model_dir = os.path.join(src_dir, "model")
view_dir = os.path.join(src_dir, "view")
controller_dir = os.path.join(src_dir, "controller")

#add directories to sys.path
sys.path.append(src_dir)
sys.path.append(model_dir)
sys.path.append(view_dir)
sys.path.append(controller_dir)

from app_controller import AppController
import shared_variables as shared_variables

if __name__ == '__main__':
    AppController().run()
