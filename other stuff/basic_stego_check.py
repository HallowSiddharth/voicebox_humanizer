from stegano import lsb

# Retrieving the hidden message from the image
message = lsb.reveal("output_image.png")
print("Hidden message:", message)
