import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
import csv

file_path = "/Users/griffinulsh/Desktop/python_homework/datasets/WorldsBestRestaurants.csv"
data = pd.read_csv(file_path)

all_restaurants = data["restaurant"].tolist()

restaurant_counts = pd.Series(all_restaurants).value_counts()

most_popular = restaurant_counts[restaurant_counts > 10]

#create a bar chart
plt.bar(most_popular.index, most_popular.values)
plt.title("Most Popular Restaurants '02-'24")
plt.xlabel("Restaurant")
plt.ylabel("Number of Appearances")
plt.xticks(rotation=35, ha="right")
plt.show()

