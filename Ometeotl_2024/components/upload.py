import reflex as rx

def ImageUploadComponent() -> rx.Component:
    """The image upload component.

    Returns:
        The UI for the image upload component.
    """
    return rx.upload(
        rx.text(
            "Drag and drop files here or click to select files"
        ),
        id="my_upload",
        border="1px dotted rgb(107,99,246)",
        padding="5em",
    )