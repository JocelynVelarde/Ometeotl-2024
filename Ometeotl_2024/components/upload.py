import reflex as rx

class ImageUploadComponent(rx.Component):
    def render(self):
        return rx.div(
            rx.h1("Upload Image"),
            rx.form(
                rx.input(type="file", name="file"),
                rx.button("Upload", type="submit"),
                method="post",
                action="/upload",
                enctype="multipart/form-data"
            )
        )