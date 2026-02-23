import os
import re
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm


import matplotlib.patches as mpatches
from matplotlib.dates import relativedelta as rd 
from matplotlib.legend_handler import HandlerPatch

import warnings
warnings.filterwarnings('ignore')