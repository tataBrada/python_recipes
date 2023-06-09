import cv2
import numpy as np
import streamlit as st

components_names = {
    "RGB Color Space": ["R Channel", "G Channel", "B Channel"],
    "HSV Color Space": ["H - Hue", "S - Saturation", "V - Value"],
    "Lab Color Space": ["L - Lightness", "a - Green to Magenta", "b - Blue to Yellow"],
    "YUV Color Space": ["Y - Luminance", "U component", "V component"],
    "YCbCr Color Space": ["Y", "Cb", "Cr"]
}

color_space_names = [
    "RGB Color Space",
    "HSV Color Space",
    "Lab Color Space",
    "YUV Color Space",
    "YCbCr Color Space"
]


class ColorSpaceConverter:
    def __init__(self, image):
        self.image = image

    def convert(self):
        pass


class RGBConverter(ColorSpaceConverter):
    def convert(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        b, g, r = cv2.split(self.image)
        return rgb_image, r, g, b


class HSVConverter(ColorSpaceConverter):
    def convert(self):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        return hsv_image, h, s, v


class LabConverter(ColorSpaceConverter):
    def convert(self):
        lab_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab_image)
        return lab_image, l, a, b


class YUVConverter(ColorSpaceConverter):
    def convert(self):
        yuv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(yuv_image)
        return yuv_image, y, u, v


class YCbCrConverter(ColorSpaceConverter):
    def convert(self):
        ycbcr_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCrCb)
        y, cb, cr = cv2.split(ycbcr_image)
        return ycbcr_image, y, cb, cr


def main():
    st.title("Color Space Visualizer")
    st.write("Upload two images and visualize their color space components.")

    uploaded_files = st.file_uploader("Choose two images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files is not None and len(uploaded_files) == 2:
        images = []

        for uploaded_file in uploaded_files:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            images.append(image)

        st.subheader("Original Images")
        st.image(np.concatenate(images, axis=1), channels="BGR", use_column_width=True)

        converters = [
            RGBConverter,
            HSVConverter,
            LabConverter,
            YUVConverter,
            YCbCrConverter
        ]

        for i, converter in enumerate(converters):
            if st.sidebar.checkbox(color_space_names[i]):
                st.header(color_space_names[i])
                converter_instance = converter(images[0])
                converter_instance1 = converter(images[1])
                converted_images = converter_instance.convert()
                converted_images1 = converter_instance1.convert()

                st.subheader("Image")
                st.image(np.hstack((converted_images[0], converted_images1[0])), use_column_width=True)

                for j in range(1, len(converted_images)):
                    component_name = components_names[color_space_names[i]][j-1]
                    st.subheader(component_name)
                    st.image(np.hstack((converted_images[j], converted_images1[j])), use_column_width=True)


if __name__ == "__main__":
    main()
