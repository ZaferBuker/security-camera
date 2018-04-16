## About Project

This project provides a safe place. If the camera sees a difference on frames, the alarm and the led will work.
At the same time the camera takes a photo every second.

## Circuitry

There is no difficulty about circuitry on this project.
All you have to do is define Buzzer and Led's pins in your code.
![untitled sketch 2_bb](https://user-images.githubusercontent.com/28205392/38816428-b7db94c2-419e-11e8-87a2-2541f0ec14b1.jpg)

## Instructions to collect data

All you need is some knowledge about OpenCV and image processing.

## Some photos of project

![1](https://user-images.githubusercontent.com/28205392/38816837-a9de35fe-419f-11e8-955f-06a9d81fb799.png)

As seen in the photo above, this photo is the image of the argument. (Actually Room status : "Clean")

![2](https://user-images.githubusercontent.com/28205392/38817024-20a71db8-41a0-11e8-80c6-c23733afb195.png)

Here we go! There's some motion. Image processing works very well, camera detects and gives feedback. (Actually Room status : "There's someone!")

## Video of project

<a href="http://www.youtube.com/watch?feature=player_embedded&v=PIh0jmxP5Uo
" target="_blank"><img src="http://img.youtube.com/vi/PIh0jmxP5Uo/0.jpg" 
alt="Video of project" width="240" height="180" border="10" /></a>


On this video, Camera computes the absolute difference between the current frame and first frame and gives feedback. If room is not clean, camera will take a picture every single second and will save in the memory!
