from io import BytesIO
from PIL import Image as PImage
from ipywidgets import FileUpload, Image, Dropdown, Text, ToggleButton, HBox, VBox, Layout
from core import to_binary


class ImageSelector():
    def __init__(self, image_dict, max_width=None):
        self.max_width = max_width
        self.image_dict = image_dict
        self.default_image = list(image_dict.keys())[0]
        self.image = self.image_dict[self.default_image]
        # Image Selector
        self.image_selector = Dropdown(options=list(self.image_dict) + ['+ Add new image'])
        self.image_selector.observe(self.on_selector_change, 'value')
        self.selector_box = HBox(children=[self.image_selector], layout=Layout(justify_content='space-around'))
        # Image Display
        width, height = self.get_size(*self.image.size)
        self.image_display = Image(value=to_binary(self.image),
                                   format='png',
                                   width=width,
                                   height=height)
        self.display_box = HBox(children=[self.image_display], layout=Layout(justify_content='center'))
        self.widget = VBox(children=[self.selector_box, self.display_box],
                           layout=Layout(align_content='inherit'))

    def get_size(self, width, height):
        if self.max_width is not None:
            new_width = min(self.max_width, width)
            height = int((new_width/width) * height)
            return new_width, height
        return width, height

    def change_image(self, image):
        self.image = image
        self.image_display.width, self.image_display.height = self.get_size(*image.size)
        self.image_display.value = to_binary(image)

    def on_selector_change(self, change):
        if self.image_selector.value in self.image_dict:
            self.change_image(self.image_dict[self.image_selector.value])
            self.widget.children = [self.selector_box, self.display_box]
        else:
            self.upload_widget = FileUpload(accept='image/*', multiple=False)
            self.name_widget = Text(description='<b>Image Name</b>', style={'description_width': 'initial'})
            self.ok_widget = ToggleButton(
                            value=False,
                            description='Add',
                            disabled=False,
                            button_style='success',
                            tooltip='Description',
                            icon='check')

            self.add_widget = HBox(children=[self.upload_widget, self.name_widget, self.ok_widget],
                                   layout=Layout(justify_content='space-around'))

            self.widget.children = [self.selector_box, self.add_widget]
            self.upload_widget.observe(self.on_upload, 'value')
            self.ok_widget.observe(self.on_add, 'value')
    #

    def on_upload(self, change):
        image_binary = list(self.upload_widget.value.values())[0]['content']
        image = PImage.open(BytesIO(image_binary))
        self.change_image(image)
        self.widget.children = [self.selector_box, self.add_widget, self.display_box]

    def on_add(self, change):
        if self.upload_widget.value:
            image_binary = list(self.upload_widget.value.values())[0]['content']
            self.image_dict[self.name_widget.value] = PImage.open(BytesIO(image_binary))
            self.image_selector.options = list(self.image_dict) + ['+ Add new image']
            self.image_selector.value = self.name_widget.value
