import tkinter as tk
from tkinter import Tk, filedialog
import cv2
from PIL import Image, ImageTk
import torch
import os
import string
from googletrans import Translator

# Create object
root = Tk()
root.bind("<Escape>", lambda e: root.quit())

# Adjust size
root.geometry("800x800")
root.attributes('-fullscreen', True)

# Load YOLOv5 model
model = torch.hub.load('yolov5','custom' ,path='C:\\Users\\shash\\Downloads\\Sign-Language\\best.pt', source='local')

fin=""

def main_page():
    def web_cam_func():
        def go_back_to_main_frame():
             cap.release()
             display_frame1.place_forget()
             display_frame2.place_forget()
             back_frame.place_forget()
             main_frame.place(relx=0.5, rely=0.5, width=500, height=500, anchor=tk.CENTER)
        
        main_frame.place_forget()
        width, height = 700, 700
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        display_frame1 = tk.Frame(root)
        display_frame1.place(relx=0.2, rely=0.5, width=600, height=700, anchor=tk.CENTER)

        display_frame1_label = tk.Label(display_frame1, text="Original video", font=('Rockwell', 16), bg="yellow")
        display_frame1_label.pack(side=tk.TOP)

        display_frame2 = tk.Frame(root)
        display_frame2.place(relx=0.8, rely=0.5, width=600, height=700, anchor=tk.CENTER)

        display_frame2_label = tk.Label(display_frame2, text="Detection", font=('Rockwell', 16), bg="yellow")
        display_frame2_label.pack(side=tk.TOP)

        back_frame = tk.Frame(root)
        back_frame.pack(side=tk.TOP, anchor=tk.NW)
        back_button = tk.Button(back_frame, text="BACK", font=("Rockwell", 12), command=go_back_to_main_frame)
        back_button.pack()

        lmain = tk.Label(display_frame1)
        lmain1 = tk.Label(display_frame2)
        lmain.place(x=0, y=0, relwidth=1, relheight=1) # Center the webcam frame
        lmain1.place(x=0, y=0, relwidth=1, relheight=1) # Center the detection frame

        # Text widget to display results
        results_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
        results_text.place(x=50, y=50)

        # Variable to accumulate displayed letters
        displayed_letters = ""

        def show_frame():
            nonlocal displayed_letters # Use nonlocal to access the variable outside the function
            _, frame = cap.read()
            frame2 = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)

            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            
            # Perform inference
            results = model(frame)
            resstr = str(results)
            # Clear the text widget
            results_text.delete(1.0, tk.END)
            
            # Iterate over each letter in string.ascii_uppercase
            for letter in string.ascii_uppercase:
                if letter in resstr[20:-92]:
                    # If the letter is found, append it to the variable
                    displayed_letters += letter
                        
            # Update the text widget with the accumulated letters
            results_text.insert(tk.END, displayed_letters + '\n')
            
            # Translate the text and display the translation
            if displayed_letters:
                translator = Translator()
                translated = translator.translate(displayed_letters, src='en', dest='kn')
                if translated.text is not None:
                    results_text.insert(tk.END, translated.text + '\n')
                else:
                    results_text.insert(tk.END, "Translation failed.\n")
            else:
                results_text.insert(tk.END, "No text to translate.\n")
            
            # Parse results and draw bounding boxes
            for *xyxy, conf, cls in results.xyxy[0]:
                if conf > 0.5:
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            frame3 = frame
            cv2image2 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGBA)
            img2 = Image.fromarray(cv2image2)

            imgtk2 = ImageTk.PhotoImage(image=img2)

            lmain1.imgtk = imgtk2
            lmain1.configure(image=imgtk2)
            
            lmain.after(10, show_frame)
            
        show_frame()
    
    main_frame = tk.Frame(root, bg="lightblue")
    main_frame.place(relx=0.5, rely=0.5, width=1000, height=1000, anchor=tk.CENTER)
    
    web_cam = tk.Button(main_frame, text="Open Webcam", command=web_cam_func, bg="pink", fg="purple", font=('Rockwell', 18))
    web_cam.place(x=425, y=425)

main_page()

Title_label = tk.Label(root, text="Sign Language Detection", font=('Rockwell', 20), bg="yellow")
Title_label.pack(side=tk.TOP)

Exit_label = tk.Label(root, text="Press escape to quit", font=('Rockwell', 20), bg="yellow")
Exit_label.pack(side=tk.BOTTOM)

# Execute tkinter
root.mainloop()
