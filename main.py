import tkinter as tk
import subprocess
import requests
import json

class DynamicGUI(tk.Frame):
    def __init__(self, parent, objects, weather_data):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.objects = objects
        self.weather_data = weather_data
        self.create_buttons()
        self.create_weather_section()

    def create_buttons(self):
        for i, obj in enumerate(self.objects):
            tk.Button(self, text=obj["text"], command=lambda obj=obj: self.execute_command(obj)).grid(row=i//3, column=i%3)

    def execute_command(self, obj):
        if obj["os"] == "mac":
            subprocess.call(["osascript", "-e", obj["command"]])
        elif obj["os"] == "win":
            subprocess.call(["cmd", "/c", obj["command"]])

    def create_weather_section(self):
        weather_frame = tk.Frame(self)
        weather_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(weather_frame, text="Weather: ").pack(side=tk.LEFT)
        self.weather_dropdown = tk.StringVar()
        self.weather_dropdown.set("Select Zipcode")
        self.weather_dropdown.trace("w", self.update_weather)
        tk.OptionMenu(weather_frame, self.weather_dropdown, "Select Zipcode", *self.weather_data.keys()).pack(side=tk.LEFT)

        self.zip_entry = tk.Entry(weather_frame)
        self.zip_entry.pack(side=tk.LEFT)
        tk.Button(weather_frame, text="Add Zipcode", command=self.add_zipcode).pack(side=tk.LEFT)
        tk.Button(weather_frame, text="Remove Zipcode", command=self.remove_zipcode).pack(side=tk.LEFT)

        self.weather_label = tk.Label(self, text="", justify=tk.LEFT)
        self.weather_label.pack(side=tk.TOP)

    def add_zipcode(self):
        zipcode = self.zip_entry.get()
        if zipcode and zipcode not in self.weather_data.keys():
            weather_info = self.get_weather_info(zipcode)
            if weather_info:
                self.weather_data[zipcode] = weather_info
                self.weather_dropdown.set(zipcode)

    def remove_zipcode(self):
        zipcode = self.weather_dropdown.get()
        if zipcode != "Select Zipcode":
            del self.weather_data[zipcode]
            self.weather_dropdown.set("Select Zipcode")
            self.weather_label.config(text="")

    def update_weather(self, *args):
        zipcode = self.weather_dropdown.get()
        if zipcode != "Select Zipcode":
            weather_info = self.weather_data[zipcode]
            self.weather_label.config(text=f"Weather for {zipcode}: {weather_info['description']}, {weather_info['temperature']}°F")

    def get_weather_info(self, zipcode):
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode}&units=imperial&appid=YOUR_API_KEY_HERE"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = json.loads(response.content)
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            return {"description": description, "temperature": temperature}
        else:
            return None

objects = [
    {
        "text": "Open Google",
        "command": "open https://www.google.com",
        "os": "mac"
    },
    {
        "text": "Open Notepad",
        "command": "notepad.exe",
        "os": "win"
    },
]

# Add more objects as required

