from argparse import ArgumentParser
import ast
import os
import sys

def is_backup_there():
    pass

def revert_backup():
    pass

def make_backup():
    pass

def list_directory(path):
    pass

def find_proper_font_size_to_fit_image_width(image_width):
    pass

def add_watermark_to_image():
    pass

def save_image():
    pass

def is_dir_exists(dir_path):
    return os.path.exists(path) and os.path.isdir(path)

def validate_args(args):
    args.directory = os.path.abspath(os.path.realpath(args.directory))

    if not is_dir_exists(args.directory):
        print('Каталог не найден. Попробуйте ещё раз')
        sys.exit(-1)

    if not isinstance(args.font_color, tuple):
        print('Цвет должен быть задан кортежем вида (255, 255, 255) для \
              RGB формата, или в виде (255, 255, 255, 255) для RGBA.')
        sys.exit(-1)

    if len(args.font_color) not in (3, 4):
        print('Цвет должен быть задан в формате RGB или RGBA')
        sys.exit(-1)

    if args.opacity:
        args.font_color = args.font_color[:3] + (args.opacity,)

    if not isinstance(args.position, tuple) or 
           len(args.position) != 2:
        print('Позиция текста должна быть задана в формате (x, y)')
        sys.exit(-1)

    if args.use_backup and not is_backup_there(args.directory):
        print('Бекап не найден!')
        sys.exit(-1)

    return args


def init_args():
    parser = ArgumentParser(description='Add watermark on images from dir')
    parser.add_argument('directory', nargs='?', default='.',
                        help='A directory with images to add watermark on')
    parser.add_argument('-f', '--font-family', default='Arial.ttf',
                        help='Choose font family for watermark text')
    parser.add_argument('-s', '--font-size', default=None, type=int,
                        help='Font size. Trying to fit if left empty')
    parser.add_argument('-c', '--font-color', type=ast.literal_eval,
                        default=(255,255,255),
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
    return args


def main():
    args = init_args()
    args = validate_args(args)

if __name__ == '__main__':
    main()
