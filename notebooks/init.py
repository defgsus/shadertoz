import os
import sys

import numpy as np
import pandas as pd
from IPython.display import HTML

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shadertox.settings")

import django

django.setup()

from shaders.models import *

