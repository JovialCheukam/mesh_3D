
from tkinter import *
import json


class DataCollectWindow:
    def __init__(self):

        self.root = Tk()
        self.root.title("Collect the 3D cloud")
        self.root.minsize(420, 150)  # width, height
        self.root.geometry("450x100+50+50")
        self.root.config(bg="#6FAFE7")

        self.frame = Frame(self.root, width=245, height=100, bg='grey')
        self.frame.grid(row=0, column=0, padx=10, pady=5)

        # Create Label in our window
        self.text = Label(self.frame, text="Please, enter the absolute path name of your data cloud json file")
        self.text.grid(row=0, column=0, padx=2, pady=2)
        #self.text2 = Label(self.frame, text="of your data cloud json file.")
        #self.text2.grid(row=1, column=0, padx=2, pady=2)

        # Ceate a data cloud user collector
        self.data_frame = Frame(self.root, width=245, height=300, bg='grey')
        self.data_frame.grid(row=3, column=0, padx=10, pady=10)
        self.data_entry = Entry(self.data_frame, bd=3)
        self.data_entry.pack(side='right')

        # Create Button  widgets 
        self.turn_on = Button(self.root, text="Save the data of cloud", command=self.get_and_save_user_data_cloud)
        self.turn_on.grid()
    
    def data_cloud_collect(self):
        return self.root
    
    def get_and_save_user_data_cloud(self):
        
        self.json_file_name = self.data_entry.get()

         # Opening JSON file
        with open(self.json_file_name, 'r') as openfile:
 
        # Reading from json file
            points = json.load(openfile)

        # Serializing json
        json_object = json.dumps(points)
 
        # Writing to sample.json
        with open("cloud.json", "w") as outfile:
             outfile.write(json_object)
        
        self.root.destroy()
