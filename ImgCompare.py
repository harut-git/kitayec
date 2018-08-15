from PIL import Image, ImageChops
import os


def is_equal(img_actual, img_expected):
    "Returns true if the images are identical(all pixels in the difference image are zero)"
    result_flag = False

    # Check that img_actual exists
    if not os.path.exists(img_actual):
        print 'Could not locate the generated image: %s' % img_actual

    # Check that img_expected exists
    if not os.path.exists(img_expected):
        print 'Could not locate the baseline image: %s' % img_expected

    if os.path.exists(img_actual) and os.path.exists(img_expected):
        actual = Image.open(img_actual)
        expected = Image.open(img_expected)
        result_image = ImageChops.difference(actual, expected)

        # Where the real magic happens
        if ImageChops.difference(actual, expected).getbbox() is None:
            result_flag = True

            # Bonus code to store the overlay
            # Result image will look black in places where the two images match

    return result_flag
