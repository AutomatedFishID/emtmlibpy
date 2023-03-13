import os
import sys
from collections import namedtuple
from pathlib import Path

import cv2

sys.path.append("..")

import emtmlibpy.emtmlibpy as emtm

import numpy as np
import pandas as pd
from argparse import ArgumentParser


def point_to_df():
    """
    Convert EvemtMeasure points to a dataframe
    :return: Pandas dataframe
    """
    dtype_template = 'object'
    point_count, box_count = emtm.em_point_count()
    print(f'number of points :: {point_count}')
    print(f'number of boxes :: {box_count}')

    p = emtm.em_get_point(0)
    index = [attr for attr in dir(p) if (not attr.startswith('__') and not attr.startswith('_'))]
    data = np.empty(shape=[point_count, len(index)], dtype=dtype_template)  # change these

    for jj in range(point_count):
        p = emtm.em_get_point(jj)
        for ii, ind in enumerate(index):
            tmp = p.__getattribute__(ind)
            data[jj][ii] = tmp

    xpdf = pd.DataFrame(data=data, columns=index)
    xpdf = xpdf.convert_dtypes().infer_objects()
    return xpdf


def em_box_coords_to_yolo(x: float, y: float, box_width: float, box_height: float, image_width: float = 1920,
                          image_height: float = 1080) -> namedtuple:
    """
    Helper function to transform the EventMeasure coord to yolo coords.
    YOLO coordinates are x, y, centre of the box and all coords normalised by image width and height
    :param image_height:
    :param image_width:
    :param box_height:
    :param box_width:
    :param x: Pixel column
    :param y: Pixel row
    :return: namedtuple (x, y, width, height)
    """

    XYWH = namedtuple('XYHW', 'x y width height')

    yolo_x = (x + box_width / 2) / image_width
    yolo_y = (y + box_height / 2) / image_height
    yolo_box_width = box_width / image_width
    yolo_box_height = box_height / image_height

    return XYWH(yolo_x, yolo_y, yolo_box_width, yolo_box_height)


def df_to_yolo(df: pd.DataFrame, out_dir='train', image_width=1920, image_height=1080):
    """
    Given a data frame write out a directory with training data in the YOLO format
    <object-class> <x> <y> <width> <height>

    integer number of object from 0 to (classes-1) - float values relative to width and height of image, it can be equal from (0.0 to 1.0] for example: <x> = <absolute_x> / <image_width> or <height> = <absolute_height> / <image_height> atention: <x> <y> - are center of rectangle (are not top-left corner)
    :param df:
    :return:
    """
    os.makedirs(out_dir, exist_ok=True)

    label = []
    for index, row in df.iterrows():
        # concatinate fgs for the label name
        label.append(
            f"{row['str_family'].decode('utf-8')}_{row['str_genus'].decode('utf-8')}_{row['str_species'].decode('utf-8')}")
    label = list(set(label))
    print(f'Unique Labels :: {label}')

    # Now we have the unique labels pull them out and create the string format.

    for index, row in df.iterrows():
        with open(os.path.join(out_dir,
                               f"{df['str_filename'].iloc[index].decode('utf-8')}_{df['n_frame'].iloc[index]}.txt"),
                  'ab') as f:
            row_label = []
            row_string = []
            r = em_box_coords_to_yolo(row['d_imx'], row['d_imy'], row['d_rectx'], row['d_recty'])
            # concatinate fgs for the label name
            row_label = f"{row['str_family'].decode('utf-8')}_{row['str_genus'].decode('utf-8')}_{row['str_species'].decode('utf-8')}"
            label_num = label.index(row_label)
            # Add the coordinates and boxes
            row_string.append(f"{label_num} {r.x} {r.y} {r.width} {r.height}")

            print(f'Writing :: {row_string}')
            f.write(f'{row_string[0]}\n'.encode())

    Path(args.output_directory).mkdir(parents=True, exist_ok=True)
    class_file = os.path.join(args.output_directory, 'classes.txt')

    with open(class_file, 'w') as f:
        for _class in label:
            f.write(f"{_class}\n")


def extract_frames_from_video(video, frame_number):
    """
    Given a BRUVS video, extract the frame as a jpg.
    :param video: The BRUVS video
    :param frame_number: The frame to extract from the video
    :return:
    """
    vid = cv2.VideoCapture(video)
    vid.set(1, frame_number)

    ret, image = vid.read()
    return image


def main(args):
    """
    Main entry point
    :return:
    """
    print('main')

    print(f'Using Version {emtm.emtm_version()} of emtmlib')

    r = emtm.em_load_data(args.emobs_path)
    n_fgs = emtm.em_unique_fgs()
    fgs = []

    for ii in range(n_fgs):
        fgs.append(emtm.em_get_unique_fgs(ii))

    print(f"Unique FGS :: {fgs}")



    pdf = point_to_df()
    boxdf = pdf[pdf['d_rectx'] >= 0]

    df_to_yolo(boxdf, out_dir=args.output_directory)

    # there might be many annotations per frame.  We just want the unique ones.
    boxdf['n_frame'].unique()

    for ii, frame in enumerate(boxdf['n_frame'].unique()):
        print(f'Extracting frame :: {frame} ')
        ii_loc = pd.Index(boxdf['n_frame']).get_loc(frame).start  # slice object

        img = extract_frames_from_video(
            os.path.join(os.path.dirname(args.emobs_path), boxdf['str_filename'].iloc[ii_loc].decode('utf-8')),
            boxdf['n_frame'].iloc[ii_loc])
        cv2.imwrite(f"{args.output_directory}/{boxdf['str_filename'].iloc[ii_loc].decode('utf-8')}_{boxdf['n_frame'].iloc[ii_loc]}.png",
                    img)


if __name__ == '__main__':
    parser = ArgumentParser('emobs')
    parser.add_argument('emobs_path',
                        help='Path to the EMObs annotation file. The EMObs file needs to be in the same directory as the videos')
    # parser.add_argument('-v', '--video-path', required=True, help='Path to the video to extract frames')
    parser.add_argument('-o', '--output-directory', required=True,
                        help='The output path to place the images and training files.')

    args = parser.parse_args()
    exit(main(args) or 0)
