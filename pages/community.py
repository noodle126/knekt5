import streamlit as st
import components.all as ac
import os

ac.topHeader()


st.write("this is the page to about the posts")


# Specify the directory you want to list
directory = '/data/'

# Get a list of files and directories in the specified directory
files_and_directories = os.listdir(directory)

# Print the list
for item in files_and_directories:
    print(item)