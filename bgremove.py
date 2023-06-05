from rembg import remove
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from threading import Thread

def upload_file():
    input_path = filedialog.askopenfilename(title='Select an image file')
    if input_path:
        try:
            global input_image
            input_image = Image.open(input_path)
            status_label.config(text='File uploaded successfully!')
            remove_button.config(state='normal')
        except Exception as e:
            status_label.config(text='An error occurred: {}'.format(str(e)))
    else:
        status_label.config(text='Please select an image file.')

def remove_background():
    output_path = filedialog.asksaveasfilename(title='Save output as', defaultextension='.png',
                                               filetypes=(('PNG files', '*.png'), ('All files', '*.*')))
    if output_path:
        try:
            # Disable the buttons and show the progress bar
            upload_button.config(state='disabled')
            remove_button.config(state='disabled')
            progress_bar.start()

            def background_removal():
                output_image = remove(input_image)
                output_image.save(output_path)

                # Enable the buttons and stop the progress bar
                upload_button.config(state='normal')
                remove_button.config(state='normal')
                progress_bar.stop()

                status_label.config(text='Background removed successfully!')

            # Run background_removal in a separate thread
            thread = Thread(target=background_removal)
            thread.start()
        except Exception as e:
            status_label.config(text='An error occurred: {}'.format(str(e)))
    else:
        status_label.config(text='Please select an output path.')

# Create the GUI window
window = tk.Tk()
window.title('Background Removal')
window.geometry('400x300')

# Create the "Upload File" button
upload_button = tk.Button(window, text='Upload File', command=upload_file)
upload_button.pack(pady=20)

# Create the "Remove Background" button
remove_button = tk.Button(window, text='Remove Background', command=remove_background, state='disabled')
remove_button.pack(pady=10)

# Create the progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', length=200, mode='indeterminate')

# Create a label to display the status
status_label = tk.Label(window, text='')
status_label.pack()

# Start the GUI event loop
window.mainloop()
