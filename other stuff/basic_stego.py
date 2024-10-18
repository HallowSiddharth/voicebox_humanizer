from stegano import lsb

# Hiding a message in an image
secret = lsb.hide("image.png", "This is my hidden message")
secret.save("output_image.png")  # Saves the image with the hidden message
