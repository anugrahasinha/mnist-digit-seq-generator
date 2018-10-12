# Coding Project: MNIST digits sequence generator

The goal of this project is to write a program that can generate images
representing sequences of numbers, for data augmentation purposes.

These images would be used to train classifiers and generative deep learning
models.  A script that saves examples of generated images is helpful in
inspecting the characteristics of the generated images and in inspecting the
trained models behaviours.

## Specifications

Please use Python. As a starting point, you may use images representing each
digit from the [MNIST database](http://yann.lecun.com/exdb/mnist/), and be
processed from the files coming from this website, using your own code. If you
use 3rd party libraries, please specify which ones and at which versions so
that we can easily run your script.

To generate an image of a sequence, the digits have to be stacked horizontally
and the spacing between them should follow a uniform distribution over a range
determined by two user specified numbers. The numerical values of the digits
themselves are provided by the user and each digit in the generated sequence is
then chosen randomly from one of its representations in the MNIST dataset.

The width of the output image in pixels is specified by the user, while the
height should be 28 pixels (i.e. identical to that of the MNIST digits).  The
code should contain both an API and a script.

The function should look as follows:

```python
# A single function defined as follows:
def generate_numbers_sequence(digits, spacing_range, image_width):
    """
    Generate an image that contains the sequence of given numbers, spaced
    randomly using an uniform distribution.

    Parameters
    ----------
    digits:
	A list-like containing the numerical values of the digits from which
        the sequence will be generated (for example [3, 5, 0]).
    spacing_range:
	a (minimum, maximum) pair (tuple), representing the min and max spacing
        between digits. Unit should be pixel.
    image_width:
        specifies the width of the image in pixels.

    Returns
    -------
    The image containing the sequence of numbers. Images should be represented
    as floating point 32bits numpy arrays with a scale ranging from 0 (black) to
    1 (white), the first dimension corresponding to the height and the second
    dimension to the width.
```

And a script, to act as a command line tool to the above API. The script is
expected to use the above API, and accept the following parameters:

* sequence: the sequence of digits to be generated
* min spacing: minimum spacing between consecutive digits
* max spacing: maximum spacing between consecutive digits
* image width: width of the generated image

The generated image is saved in the current directory as a .png.

Note that besides implementing the expected function all, you are free to
implement as you wish. If you have time, you may also want to expand the
project and think about additional methods for data expansion (warping, etc.).

It is expected that some of the problems have multiple reasonable solutions: in
this case, you should be ready to answer questions about the tradeoffs.
Ideally, you would document them in the assignement.

## What should be provided

* a python module (or package) that defines the main function. That
  module/package should be written such as it can be imported by a 3rd party
  program.
* a README file explaining how to use the scripts, and discussing
  implementation details.

We expect the code to be organized, designed, tested and documented as if it
were going into production.

You can send the work assignement as a zipfile, tarball, etc. or better yet the
whole code repository (git, hg, etc.). Just make sure it is not put in a public
place !

## Scoring

We value quality over feature-completeness. It is fine to leave things aside
provided you call them out in your project's README. Part of the goal of this
exercise is to help us identify what you consider production-ready code.

We will look at the following to assess your code:

* clarity: is the code organized in well defined functions, with separated
  concerns ? Is it implemented in a way that makes it difficult or simple to
  extend ? Depending on your advertised python expertise, we will also look
  whether the code is idiomatic python.
* documentation: does the README clearly and concisely explains the problem and solution ?
  Are technical tradeoffs explained ?
* testing and correctness: the code needs to do what is asked, and you need to be able to
  explain why it is correct. Ideally, the code would have some tests. We're not
  looking for full coverage (given time constraint) but just trying to get a
  feel for your testing skills.
* technical choices: do choices of libraries, architecture etc. seem appropriate for the
  chosen application?
* going the last mile: if you find the problem trivial, can you think of more
  advanced data augmentation techniques for the problem of handwritten digit
  recognition ? Can you think of a way to generate many images

Good luck !
