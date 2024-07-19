import cv2
import os
import numpy as np 
import imutils
import easyocr
import tkinter as tk
from tkinter import Tk, Button, Label
from tkinter import filedialog
from PIL import Image, ImageTk
text=""
numberplates=""
message_displayed=""
def handle_upload(event=None):

    filename = filedialog.askopenfilename()
    if filename:
        img = cv2.imread(filename)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        # Convert the PIL image to Tkinter PhotoImage
        img_tk = ImageTk.PhotoImage(pil_img)
        # Display the image in the Tkinter window
        label.config(image=img_tk)
        label.image = img_tk  # Retain reference to the image object

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Perform edge detection
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(bfilter, 30, 200)

        # Find contours
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        print(approx)

        # Perform masking
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)


        # Perform OCR on the masked image (cropped area)
        reader = easyocr.Reader(['en'])
        result = reader.readtext(new_image)
        print(result)

        global text
        text=result[0][-2]
        print(text)
        return text
    


    else:
        print("Failed to read image:", filename)
#pip install opencv-contrib-python
def save_file():
    global numberplates,text,message_displayed
    if not text and not message_displayed:
        # Create a label to display the message
        message_label = Label(root, text="Please select a number plate image")
        message_label.pack()
        message_displayed = True  # Update the flag to indicate that the message has been displayed
        return
    else:
        numberplates="numberplates.txt"
        file=open(numberplates,'a')
        file.write(text+ '\n')
        file.close()
def access_file():
    current_dir = os.getcwd()
    
    # Construct the relative file path
    file_path = os.path.join(current_dir, 'numberplates.txt')
    
    # Open the file
    os.startfile(file_path)



# Create Tkinter window
root = Tk()
root.title("Image Processing")
root.geometry("500x600")
root.configure(bg="#E3FEF7")
label_title = Label(root, text="Automatic Number Plate Recognization",bg='#E3FEF7')
label_title.place(x=10, y=10)
label_title.config(font=("Arial", 18, "bold"), fg="#003C43")
# Create a button for file upload
Acessfile=Button(root,text="access saved files",command=access_file)
Acessfile.pack(side="bottom")


Save_button = Button(root,text="Save Number plate",command=save_file)
Save_button.pack(side="bottom")

browse_button = Button(root, text="Browse Image", command=handle_upload)
browse_button.pack(side='bottom')

label = tk.Label(root)
label.pack(side="bottom")




# Start the Tkinter event loop
root.mainloop()