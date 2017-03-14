#! python3
# marker.py - Automates basic image manipulation:  resize, watermark, and compress images.

import argparse
import shutil
import os
import os.path
import ast

from datetime import datetime

try:
    import tinify
except ImportError:
    exit("This script requires the tinify module.\nInstall with pip install tinify")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:    
    exit("This script requires the PIL module.\nInstall with pip install Pillow")

def compress_image(filename):    
    tinify.key = "YOUR_API_KEY"
    source = tinify.from_file(filename)
    source.to_file(filename)

def resize_image(filename, width, height):
    image = Image.open(filename)
    imageWidth, imageHeight = image.size

    if width is None and height is not None:
        imageWidth = (imageWidth * height) / imageHeight
        imageHeight = height
    elif width is not None and height is None:
        imageHeight = (imageHeight * width) / imageWidth
        imageWidth = width
    elif width is not None and height is not None:
        imageWidth = width
        imageHeight = width

    return image.resize((int(imageWidth), int(imageHeight)), Image.ANTIALIAS)
    

def watermark_image_with_text_old(filename, text, color, fontfamily):
    image = Image.open(filename).convert('RGBA')
    imageWatermark = Image.new('RGBA', image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(imageWatermark)
    
    width, height = image.size
    margin = 10
    font = ImageFont.truetype(fontfamily, int(height / 20))
    textWidth, textHeight = draw.textsize(text, font)
    x = width - textWidth - margin
    y = height - textHeight - margin

    draw.text((x, y), text, color, font)

    return Image.alpha_composite(image, imageWatermark)

def find_text_size_to_fit_image(image_width, text, fontfamily, margin=20):
    font_size=int(image_width/len(text)*2)
    font = ImageFont.truetype(fontfamily, size=font_size)


    if font.getsize(text)[0] > image_width:
        step = -1
    else:
        step = 1

    while font.getsize(text)[0] > image_width - margin*2:
        font_size += step
        font = ImageFont.truetype(fontfamily, size=font_size)

    return font


def watermark_image_with_text(filename, pos, text, color, fontfamily, fontsize):
    image = Image.open(filename).convert('RGBA')
    text_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    if fontsize:
        font = ImageFont.truetype(fontfamily, size=fontsize)
    else:
        font = find_text_size_to_fit_image(image.size[0], text, fontfamily)
    draw.text((pos[0]+2, pos[1]+1), text, fill='dimgray', font=font)  # draw shadow
    draw.text(pos, text, fill=color, font=font)
    
    return Image.alpha_composite(image, text_layer)



def main():
    parser = argparse.ArgumentParser(description='Automates basic image manipulation.')
    parser.add_argument('directory', nargs='?', default='.', help='A directory of images to process')
    parser.add_argument('-w', '--width', type=int, help='Resize the width of the image to <width>')
    parser.add_argument('--height', type=int, help='Resize the height of the images to <height>')
    parser.add_argument('-f', '--font-family', help='Sets the font family for the text watermark to <font family>')
    parser.add_argument('--font-style', choices=['bold', 'italic', 'underline', 'regular'], help="Sets the font style of the text watermark to <font style>. Valid options are: bold, italic, underline, regular.")
    parser.add_argument('--font-size', default=None, type=int, help="Sets the font size of the text watermark to <font size>")
    parser.add_argument('-o', '--opacity', type=float, help="Sets the opacity of the watermark to <opacity>. This is a number between 0 and 1.")
    parser.add_argument('-c', '--color', type=ast.literal_eval, help="Sets the color of the text watermark to <color>. Expects the <color> in RGBA tuple format.")
    parser.add_argument('-t', '--text', help="Sets the watermark to <text>")
    parser.add_argument('-p', '--position', type=ast.literal_eval, help='Set position on image for watermark text')
    parser.add_argument('-i', '--image-overlay', help="Sets an image overlay to <path>. (Watermark the image with an image instead of text)")
    parser.add_argument('--overlay-size', type=float, help="Sets the size of the image overlay to <size>. This is a number between 0 and 1. (What percentage of image should be covered by the image overlay?)")
    parser.add_argument('--no-backup', action='store_true', default=False, help='Don\'t make backup')    

    args = parser.parse_args()

    os.chdir(args.directory)
    if not args.no_backup:
        shutil.copytree(os.getcwd(), 'directory_backup_{1}'.format(args.directory, datetime.now().isoformat()).replace(':', '_'))
    
    files_amount = len(os.listdir())
    for file_num, filename in enumerate(os.listdir(), start=1):
        if filename.lower().endswith('.png') or filename.lower().endswith('.jpg'):
            print('[{1}/{2}] File: {0}'.format(filename, file_num, files_amount), end='...')
            resized_image = resize_image(filename, args.width, args.height)
            resized_image.save(filename, quality=90)
            
            if args.text is not None:
                watermarked_image = watermark_image_with_text(filename,
                                                              args.position,
                                                              args.text,
                                                              args.color,
                                                              args.font_family,
                                                              args.font_size)
                watermarked_image.save(filename)
            print('Done')
            # A Tinify API key is required to compress images
            # compress_image(filename)

if __name__ == '__main__':
    main()