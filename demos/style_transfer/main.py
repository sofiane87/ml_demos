from pathlib import Path
import json
from notebook.selector import ImageSelector
from ipywidgets import HBox, VBox, Layout, ToggleButton, Image, HTML
from core import load_img, stylise, to_binary

current_folder = Path(__file__).parent

with (current_folder / 'images.json').open('r') as fr:
    IMAGES = {
        name: load_img(path)
        for name, path in json.load(fr).items()
        }

with (current_folder / 'styles.json').open('r') as fr:
    STYLES = {
        name: load_img(path)
        for name, path in json.load(fr).items()
        }


def start_demo():
    images_widget = ImageSelector(IMAGES, max_width=450)
    images_box = VBox(children=[
        HTML('<h1>Select Image</h1>'),
        images_widget.widget
    ])
    styles_widget = ImageSelector(STYLES, max_width=450)
    styles_box = VBox(children=[
        HTML('<h1>Select Style</h1>'),
        styles_widget.widget
    ])
    selectors = HBox(children=[images_box, styles_box],
                     layout=Layout(justify_content="space-between"))

    confirm_button = ToggleButton(
                                value=False,
                                description='Stylise',
                                disabled=False,
                                button_style='success',
                                tooltip='Description',
                                icon='check')

    confirm_box = HBox(children=[confirm_button], layout=Layout(justify_content='space-around'))

    def on_click(change):
        stylised_img = stylise(image=images_widget.image, style=styles_widget.image)
        stylised_widget = Image(
                value=to_binary(stylised_img),
                width=stylised_img.size[0],
                height=stylised_img.size[1],
                format='png')
        stylised_box = HBox(children=[stylised_widget], layout=Layout(justify_content='space-around'))
        full_display.children = [selectors, confirm_box, stylised_box]

    confirm_button.observe(on_click, 'value')
    full_display = VBox(children=[selectors, confirm_box])
    return full_display
