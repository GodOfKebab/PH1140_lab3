# How to use this repo for your damped pendulum lab:

- Take a video of your damping pendulum's motion for approx. 1 minute
- edit the line 20 of main.py and enter your video's path
- If you recorded with 60fps, then you can execute the code, but if you instead used a 30fps recording, then you need to change all the 60.0 to 30.0
- After executing the main.py, select the object you want to track and press [space]
- Let the code track the object for 1 minute. If you want faster (though less accurate) tracking, you can change your tracking algorithm from the OPENCV_OBJECT_TRACKERS list. For this just change the tracker selected on line 16 of main.py
- When the program comes to an end, it should print data points on x and y axis as a list. Copy this and paste it on the top of the plot_and_fit.py.
- Enter the length of your string and guess the damping factor. Then execute the code.
- This should open a window and show you the graph of the scattered data points and plot the differential equation that governs the motion of damped oscillations(this doesn't rely on the data you collected but you should try different damping_factor values to get a better fit). 
- On the output, you will also see a number. This the chi-squared statistic of the data --> chi-square statistic(X^2) is the sum of all the data points' abs(((observed - expected)^2)/expected)