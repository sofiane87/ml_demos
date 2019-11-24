import requests
from PIL import Image
from io import BytesIO
import os
import tensorflow_hub as hub



# Tensorflow Model
HUB_MODULE = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
API_KEY = os.environ.get("DEEPAI_API", "quickstart-QUdJIGlzIGNvbWluZy4uLi4K")


def to_binary(image):
    im_binary = BytesIO()
    image.save(im_binary, format='JPEG')
    return im_binary.getvalue()


def load_img(path_to_img):
    return Image.open(path_to_img)


def stylise(image, style):
    # stylized_image = HUB_MODULE(tf.constant(image), tf.constant(style))[0]
    r = requests.post(
        "https://api.deepai.org/api/fast-style-transfer",
        files={
            'content': to_binary(image),
            'style': to_binary(style),
        },
        headers={'api-key': API_KEY}).json()
    url = r['output_url']
    data = requests.get(url).content
    img = Image.open(BytesIO(data))
    return img
