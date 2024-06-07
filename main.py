
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
import tkinter
import customtkinter
from pytube import YouTube


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    
    # Update the percentage label text
    pPercentage.configure(text=f'{percentage_of_completion:.2f}%')
    
    # Updating the progress bar value with animation
    animate_progress_bar(percentage_of_completion / 100)

def animate_progress_bar(target_value):
    current_value = progressBar.get()
    step = (target_value - current_value) / 10
    
    def step_progress():
        nonlocal current_value
        current_value += step
        if (step > 0 and current_value < target_value) or (step < 0 and current_value > target_value):
            progressBar.set(current_value)
            app.after(50, step_progress)
        else:
            progressBar.set(target_value)
    
    step_progress()

def startdownload():
    try:
        ytlink = link.get()
        ytObject = YouTube(ytlink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="black")
        resolutionLabel.configure(text=f"Resolution: {video.resolution}")
        finishLabel.configure(text="")
        video.download()

        finishLabel.configure(text="Downloaded!")

    except Exception as e:
        finishLabel.configure(text="Download Error", text_color="red")
        print(e)

# System settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Adding UI Element
title = customtkinter.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=450, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startdownload)
download.pack()

# Progress percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

# Progress Bar
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=20)

# Video Resolution Label
resolutionLabel = customtkinter.CTkLabel(app, text="")
resolutionLabel.pack()

# Run app
app.mainloop()
