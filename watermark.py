from argparse import ArgumentParser
import ast


def make_backup():
    pass

def list_directory(path):
    pass

def find_proper_font_sizeto_fit_image_width(image_width):
    pass

def add_watermark_to_image():
    pass

def save_image():
    pass


def main():
    parser = ArgumentParser(description='Add watermark on images from dir')
    parser.add_argument('directory', nargs='?', default='.',
                        help='A directory with images to add watermark on')
    parser.add_argument('-f', '--font-family', default='Arial.ttf',
                        help='Choose font family for watermark text')
    parser.add_argument('-s', '--font-size', default=None, type=int,
                        help='Font size. Trying to fit if left empty')
    parser.add_argument('-c', '--font-color', type=ast.literal_eval,
                        help='Sets the color of the text watermark to <color>. \
                        Expects the <color> in RGBA or RGB tuple format')
    parser.add_argument('-o', '--opacity', type=int,
                        help='Set text opacity. Replaces `--font-color` \
                        RGBA value if it sets')
    parser.add_argument('-p', '--position', type=ast.literal_eval,
                        help='Set watermark position in (x, y) tuple format')
    parser.add_argument('-t', '--text', type=str, help='Watermark text')

    parser.add_argument('-r', '--recursive', action='store_true',
                        default=False,
                        help='Process all files in directory and in all \
                        subdirectories')
    parser.add_argument('--no-backup', action='store_true', default=False,
                        help='Do not make any backup')
    parser.add_argument('-b', '--use-backup', action='store_true',
                        default=False, help='Use backuped files to process')

    args = parser.parse_args()

if __name__ == '__main__':
    main()
