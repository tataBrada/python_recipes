import tkinter as tk
from collections import deque
import numpy as np
import cv2
import PIL.ImageTk as ImageTk
import PIL.Image as Image

# Initialize default values for lower and upper green color boundaries
default_lower = (29, 86, 6)
default_upper = (91, 255, 255)

# Create a deque to store tracked points
pts = deque(maxlen=64)

# Initialize video capture
vs = cv2.VideoCapture(0)

# Create tkinter window
window = tk.Tk()
window.title("Green Ball Tracking")

# Create sliders for lower and upper color boundaries
lower_hue = tk.Scale(window, from_=0, to=255, label="Lower Hue", orient=tk.HORIZONTAL, length=300)
lower_hue.set(default_lower[0])
lower_hue.pack()
lower_saturation = tk.Scale(window, from_=0, to=255, label="Lower Saturation", orient=tk.HORIZONTAL, length=300)
lower_saturation.set(default_lower[1])
lower_saturation.pack()
lower_value = tk.Scale(window, from_=0, to=255, label="Lower Value", orient=tk.HORIZONTAL, length=300)
lower_value.set(default_lower[2])
lower_value.pack()
upper_hue = tk.Scale(window, from_=0, to=255, label="Upper Hue", orient=tk.HORIZONTAL, length=300)
upper_hue.set(default_upper[0])
upper_hue.pack()
upper_saturation = tk.Scale(window, from_=0, to=255, label="Upper Saturation", orient=tk.HORIZONTAL, length=300)
upper_saturation.set(default_upper[1])
upper_saturation.pack()
upper_value = tk.Scale(window, from_=0, to=255, label="Upper Value", orient=tk.HORIZONTAL, length=300)
upper_value.set(default_upper[2])
upper_value.pack()

# Create a canvas to display the video output
canvas = tk.Label(window)
canvas.pack()

# Update lower and upper color boundaries
lower_color = (lower_hue.get(), lower_saturation.get(), lower_value.get())
upper_color = (upper_hue.get(), upper_saturation.get(), upper_value.get())


# Update color boundaries when sliders are moved
def update_color_boundaries(event):
    global lower_color, upper_color
    lower_color = (lower_hue.get(), lower_saturation.get(), lower_value.get())
    upper_color = (upper_hue.get(), upper_saturation.get(), upper_value.get())


# Bind update_color_boundaries function to slider events
lower_hue.bind("<ButtonRelease-1>", update_color_boundaries)
lower_saturation.bind("<ButtonRelease-1>", update_color_boundaries)
lower_value.bind("<ButtonRelease-1>", update_color_boundaries)
upper_hue.bind("<ButtonRelease-1>", update_color_boundaries)
upper_saturation.bind("<ButtonRelease-1>", update_color_boundaries)
upper_value.bind("<ButtonRelease-1>", update_color_boundaries)


# Main loop
def main_loop():
    # Grab the current frame
    ret, frame = vs.read()

    if not ret:
        return

    # Resize the frame, blur it, and convert it to the HSV color space
    frame = cv2.resize(frame, (600, 400))
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construct a mask for the color "green" using the updated color boundaries
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask and initialize the current (x, y) center of the ball
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Only proceed if at least one contour was found
    if len(contours) > 0:
        # Find the largest contour in the mask
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius meets a minimum size
        if radius > 10:
            # Draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Update the points queue
    pts.appendleft(center)

    # Loop over the set of tracked points
    for i in range(1, len(pts)):
        # If either of the tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # Compute the thickness of the line and draw the connecting lines
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Convert the frame to RGB format and create a PIL ImageTk object
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(image=img)

    # Update the canvas with the new image
    canvas.configure(image=img_tk)
    canvas.img = img_tk

    # Call the main_loop function after a delay
    window.after(1, main_loop)


# Call the main_loop function to start the application
main_loop()

# Start the tkinter event loop
window.mainloop()

# Release the video capture and close all windows
vs.release()
cv2.destroyAllWindows()
