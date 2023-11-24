import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
import matplotlib.pyplot as pyplot


def crop_image(image, crop_percentage):
    height, width = image.shape[:2]
    crop_height = int(height * (1 - crop_percentage))
    crop_width = int(width * (1 - crop_percentage))

    cropped_image = image[:crop_height, :crop_width, :]

    return cropped_image


def normalized_rgb(img):
    return img[:, :, :3] / 255


def centralize(img, side=.06):
    img = img.real.astype(np.float64)
    thres = img.size * side

    l = img.min()
    r = img.max()
    while l + 1 <= r:
        m = (l + r) / 2.
        s = np.sum(img < m)
        if s < thres:
            l = m
        else:
            r = m
    low = l

    l = img.min()
    r = img.max()
    while l + 1 <= r:
        m = (l + r) / 2.
        s = np.sum(img > m)
        if s < thres:
            r = m
        else:
            l = m

    high = max(low + 1, r)
    img = (img - low) / (high - low)

    img = np.clip(img, 0, 1)

    return img, low, high


def x_gen(shape):
    xh, xw = np.arange(shape[0]), np.arange(shape[1])
    xh = xh.reshape((-1, 1))
    return xh, xw


def encode_image(image, text, xmap, margins=(1, 1)):
    normalized_image = normalized_rgb(image)
    normalized_text = normalized_rgb(text)
    fourier_image = np.fft.fft2(normalized_image, None, (0, 1))
    pixel_buffer = np.zeros(
        (normalized_image.shape[0] // 2 - margins[0] * 2, normalized_image.shape[1] - margins[1] * 2, 3))
    pixel_buffer[:normalized_text.shape[0], :normalized_text.shape[1]] = normalized_text
    alpha = 30

    xh, xw = xmap[:2]
    fourier_image[+margins[0] + xh, +margins[1] + xw] += pixel_buffer * alpha
    fourier_image[-margins[0] - xh, -margins[1] - xw] += pixel_buffer * alpha

    image_with_text = np.fft.ifft2(fourier_image, None, (0, 1))
    return image_with_text, fourier_image


def encode_text(image, text, *args, **kwargs):
    text_size = ImageFont.truetype(".\Consolas.ttf", image.shape[0] // 12)
    render_size = text_size.getsize(text)
    render_size = (render_size[0], render_size[1])
    text_img = Image.new('RGB', render_size, (0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), text, (255, 255, 255), font=text_size)
    rgb_pixel_text_array = np.asarray(text_img)
    return encode_image(image, rgb_pixel_text_array, *args, **kwargs)


def decode_image(encode_image, original_image):
    normalized_encode_image = normalized_rgb(encode_image)
    fourier_encode_image = np.fft.fft2(normalized_encode_image, None, (0, 1))

    normalized_original_image = normalized_rgb(original_image)
    fourier_original_image = np.fft.fft2(normalized_original_image, None, (0, 1))
    fourier_encode_image -= fourier_original_image

    return fourier_encode_image


def imsaveEx(fn, img, *args, **kwargs):
    img, _, _ = centralize(img)
    img = (img * 255).round().astype(np.uint8)

    pyplot.imsave(fn, img, *args, **kwargs)


def main(args):
    rgb_pixel_array = pyplot.imread(args.input)
    margins = (1, 1)
    xmap = x_gen((rgb_pixel_array.shape[0] // 2 - margins[0] * 2, rgb_pixel_array.shape[1] - margins[1] * 2))

    if args.decode:
        encode = pyplot.imread(args.decode)
        decode = decode_image(encode, rgb_pixel_array)
        cropped_ea = crop_image(decode, 0.20)
        imsaveEx(args.output or "decode.jpg", cropped_ea)
        print(f"Image saved in {args.output or 'decode.jpg'}")
    else:
        ea, fa = encode_text(rgb_pixel_array, args.text, xmap, margins)
        imsaveEx(args.output, ea)
        print(f"Image saved in {args.output}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", dest="input", default="photo.jpg", type=str, help="Original image filename")
    argparser.add_argument("-o", dest="output", type=str, help="Output image filename")
    argparser.add_argument("-t", dest="text", type=str, help="Encrypted text")
    argparser.add_argument("-d", dest="decode", type=str, help="Decoded image filename")
    args = argparser.parse_args()
    main(args)
