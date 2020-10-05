
# rotate
Create recursive image transformation animations

![image transformation animations](https://github.com/Jetsukda/rotate/blob/master/image%20transformation%20animations.gif)


Full demo animation on my Twitter:
https://twitter.com/r_vizzz/status/1311425342310092800?s=20

  

Older animations:
https://www.youtube.com/watch?v=OXo-uzzD4Js
https://www.reddit.com/r/compsci/comments/izy2kf/rotating_an_image_recursively_one_of_my_favorite/

  

## Usage Instructions

An animation can be generated using the `rotate.py` or `transform.py` file.

### rotate&#46;py

#### Arguments:

`python3.7 rotate.py <input_image.png> <output_file.mp4>`

### transform&#46;py

#### Arguments:

`python3.7 transform.py <input_image.png> <output_file.mp4> optional: <transform_type>`

#### Transform Types:

0: rotation

1: vertical flip

2: horizontal flip

3: vertical+horizontal flip

### For both these files:

Valid output formats include .m4a .mp4 .mov .avi

The image needs to have NxN dimensions where N is a power of 2. If these requirements are not met, the program can automatically resize the image to the closest power of 2.
