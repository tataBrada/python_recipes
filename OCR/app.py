import cv2
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
import streamlit as st

FONT = 'fonts/simfang.ttf'

# Streamlit app
st.title("Optical Character Recognition (OCR) using PaddleOCR")

# Language selection dropdown menu
# Add more languages if needed
language = st.sidebar.selectbox("Select Language", ["English", "Serbian(latin)", "Croatian", "Serbian(cyrillic)"])

if language == "Serbian(latin)":
    language_code = "rs_latin"
elif language == "Serbian(cyrillic)":
    language_code = "rs_cyrillic"
elif language == "Croatian":
    language_code = "hr"
elif language == "English":
    language_code = "en"


# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang=language_code)

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB color space

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform OCR on the image
    with st.spinner("Performing OCR..."):
        results = ocr.ocr(image, cls=True)

    # Display the OCR result
    st.subheader("OCR Result")
    result = results[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]

    im_show = draw_ocr(image, boxes, txts, scores, font_path=FONT)
    st.image(im_show)
