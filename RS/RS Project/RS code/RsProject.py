import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
import user_based_cf as Ucf
import content_based_rs as cb_rs
import naive_rs


rs_project = tk.Tk()

rs_project.configure()

rs_project.title("Movie Recommender System")


# Create a Canvas widget
canvas = tk.Canvas(rs_project, width=700, height=600)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a Scrollbar widget
scrollbar = tk.Scrollbar(rs_project, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure the Canvas to use the Scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a Frame inside the Canvas to hold the grid
frame = tk.Frame(canvas)

# Add the Frame to the Canvas
canvas.create_window((0, 0), window=frame, anchor=tk.NW)


# text for selecting the dataset file
label = Label(frame, text="Select Dataset")
label.config(font=("helvetica", 14, "bold"))

# text for displaying the file path
file_label = tk.Label(frame, text="Selected file: ")


# Function for selecting the file

def select_file():
    file_path = filedialog.askopenfilename()
    file_label.config(text="Selected file: " + file_path)
    # print("Selected file:", file_path)
    file_path
    display_headings(file_path)


# function for displaying records
def display_headings(dataset_path):
    filename = dataset_path

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = [', '.join(row) for row in reader][:10]

    # Clear the text field
    sample_data.delete(1.0, tk.END)

    # Insert the headings into the text field
    for line in lines:
        sample_data.insert(tk.END, line + '\n')


# select button
select_button = tk.Button(
    frame, text="Select Dataset", command=select_file)


# Heading for Sample Data

label_sample = Label(frame, text="Sample Data")
label_sample.config(font=("helvetica", 12, "bold"))

# Sample Data
sample_data = Text(frame, height=10, width=80)

# Heading for Collaborative filtering

label_sample_collaborative = Label(frame, text="Collaborative filtering")
label_sample_collaborative.config(
    font=("helvetica", 12, "bold"))


# taking input movie name

entry_collaborative = tk.Entry(frame, width=30)
entry_collaborative.insert(0, "Enter user id here")

# Create a button to get the input text


def get_input_text_collaborative():
    user_input = entry_collaborative.get()
    cf_recommendations = Ucf.collaborative_filtering(user_input)
    collaborative_recommened_movies.delete("1.0", tk.END)
    for i in cf_recommendations:
        collaborative_recommened_movies.insert(tk.END, i + '\n')


collaborative_button = tk.Button(frame, text="Submit",
                                 command=get_input_text_collaborative)
# recommended movies box
collaborative_recommened_movies = Text(frame, height=5, width=80)


# Heading for Content based filtering

label_sample_content = Label(frame, text="Content based filtering")
label_sample_content.config(
    font=("helvetica", 12, "bold"))

# taking input movie name
entry_content_based = tk.Entry(frame, width=30)
entry_content_based.insert(0, "Enter user id here")

# Create a button to get the input text


def get_input_text_content_based():
    user_input = entry_content_based.get()
    cb_recommendations = cb_rs.content_based_filtering(user_input)
    content_based_recommened_movies.delete("1.0", tk.END)
    for i in cb_recommendations:
        content_based_recommened_movies.insert(tk.END, i + '\n')


content_based_button = tk.Button(frame, text="Submit",
                                 command=get_input_text_content_based)


# recommended movies box
content_based_recommened_movies = Text(frame, height=5, width=80)


# Heading for Naive based filtering

label_sample_naive = Label(frame, text="Naive based filtering")
label_sample_naive.config(
    font=("helvetica", 12, "bold"))

# taking input of movie tags
entry_movie_tags = tk.Entry(frame, width=30)
entry_movie_tags.insert(0, "Enter user id:")

# Create a button to get the input text


def get_input_text_naive():
    user_input = entry_movie_tags.get()
    naive_recommendations = naive_rs.naive_bayes_cf(user_input)
    naive_recommened_movies.delete("1.0", tk.END)
    for i in naive_recommendations:
        naive_recommened_movies.insert(tk.END, i + '\n')


naive_button = tk.Button(frame, text="Submit",
                         command=get_input_text_naive)


# recommended movies box
naive_recommened_movies = Text(frame, height=5, width=80)


# File dialog selection heading manifestation
label.grid(row=0, sticky='nw', pady=20, padx=10)

# showing the file label
file_label.grid(row=1, column=0, columnspan=3, padx=10)


# File selection button manifest
select_button.grid(row=1, column=4, padx=10)

# Sample Data heading
label_sample.grid(row=2, sticky='nw', pady=0, padx=10)

# Sample data manifest
sample_data.grid(row=3, sticky='w', padx=10, pady=20, columnspan=5)


# Collaborative fitlering heading manifestation
label_sample_collaborative.grid(row=4, sticky='nw', pady=0, padx=10)

# CF movie input and button
entry_collaborative.grid(row=5, column=0, sticky='w',
                         padx=10, columnspan=5)
collaborative_button.grid(row=5, column=2, sticky='w',
                          padx=10, columnspan=5)

# Collaborative Movies Suggestions manifest
collaborative_recommened_movies.grid(
    row=6, sticky='w', padx=10, pady=10, columnspan=5)


# Content based filtering heading manifestation
label_sample_content.grid(row=7, sticky='nw', pady=0, padx=10)
# Content movie input and button
entry_content_based.grid(row=8, column=0, sticky='w',
                         padx=10, columnspan=5)
content_based_button.grid(row=8, column=2, sticky='w',
                          padx=10, columnspan=5)


# Content Based Movies Suggestions manifest
content_based_recommened_movies.grid(
    row=9, sticky='w', padx=10, pady=10, columnspan=5)


# Naive based filtering manifestation
label_sample_naive.grid(row=10, sticky='nw', pady=0, padx=10)
# Naive movie input and button
entry_movie_tags.grid(row=11, column=0, sticky='w',
                      padx=10, columnspan=5)
naive_button.grid(row=11, column=2, sticky='w',
                  padx=10, columnspan=5)
# Naive Movies Suggestions manifest
naive_recommened_movies.grid(
    row=12, sticky='w', padx=10, pady=10, columnspan=5)


frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))
tk.mainloop()
