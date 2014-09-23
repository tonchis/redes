import sys
sys.path.append("tp1")
sys.path.append("tmp")
import helpers
import scapy.all
from ggplot import *
import pandas as pd
import collections

def plot_histogram(file_name, size, x_axis):
  print "This method assumes execution in root directory"
  arp_sample = helpers.load_sample("tmp/" + file_name) # ARP-Restorando-AP01_1140_1240.pcap
  sample = { 'src': arp_sample.src[:size], 'dst': arp_sample.dst[:size] }
  df = pd.DataFrame(sample)
  return qplot(df[x_axis], data = df, geom = 'histogram')
  # qplot('variable del eje x', data = 'dataframe', geom = 'histogram')

def dict_from(dataframe):
  return dict(dataframe)

def dataframe_from(dictionary):
  return pd.DataFrame(dictionary.items())

def help_rename_column(index, new_name):
  print "Copy and paste the following to rename column '" + index + "' to '" + new_name + "'"
  print "variable_name.rename(columns={" + str(index) + ": '" + new_name + "'}, inplace=True)"

def count_repetition_dict(collection): # for example, a column from a dataframe
  return dict(collections.Counter(collection))
