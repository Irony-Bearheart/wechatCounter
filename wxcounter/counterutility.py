# -*- encoding: utf-8 -*-
from collections.abc import Sequence
from functools import cache
from typing import NamedTuple

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

import cv2
import numpy as np

from wxcounter import CHAT_WINDOW_AREA, PROFILE_RANGE, PROFILE_SIZE

THRESHOLD = 50
PROFILE_FORMATS = ("jpeg",)  # Format of WeChat Profile

# Utilities for matching

SIFT = cv2.SIFT()
BF = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)


class Feature(NamedTuple):
    keypoints: Sequence[cv2.KeyPoint]  # noqa
    descriptors: np.ndarray


def count_rows(pic: Image.Image) -> tuple[int, int]:
    rows = get_profile_row(pic)

    def _count_row(image_row: Image.Image, num: int) -> int:
        array_row = np.array(image_row)
        feature = Feature(
            *SIFT.detectAndCompute(
                array_row,
                np.ones_like(array_row, dtype=np.bool_),
            )
        )

        matches = BF.match(
            queryDescriptors=feature.descriptors,
            trainDescriptors=FEATURES[num].descriptors
        )

        def judge(match_object: cv2.DMatch) -> bool:
            """
            Judge if a `DMatch` object could be counted

            Judge if it's similar enough and lies on this page
            """
            Y_LIMIT = (  # noqa. If the upper side of the profile falls in this area, we'll classify it into this page
                # Otherwise, it should be classified into the previous page (if upper_size < Y_LIMIT[0]) or
                # the next page (if upper_size >= Y_LIMIT[1])
                CHAT_WINDOW_AREA[1] - PROFILE_SIZE // 2,
                CHAT_WINDOW_AREA[3] - PROFILE_SIZE // 2
            )

            return bool(
                match_object.distance < THRESHOLD
                and (
                    Y_LIMIT[0]
                    <= (
                        feature.keypoints[match_object.trainIdx].pt[1]
                        - feature.keypoints[match_object.trainIdx].pt[1]
                    )
                    < Y_LIMIT[1]
                )
                # pt: cv2.typing.Point2f, which is defined as
                # Sequence[x: float, y: float] and marks all points that are matched
            )

        return sum(map(judge, matches))

    left_count = _count_row(rows[0], 0)
    right_count = _count_row(rows[1], 1)
    return left_count, right_count


def get_profile_row(pic: Image.Image) -> tuple[Image.Image, Image.Image]:
    PROFILE_ROWS = (  # noqa
        # in the order of (left, upper, right, lower), the same as the argument `box` in PIL.Image.crop
        (PROFILE_RANGE[0], CHAT_WINDOW_AREA[1], PROFILE_RANGE[0] + PROFILE_SIZE, CHAT_WINDOW_AREA[3]),
        (PROFILE_RANGE[1], CHAT_WINDOW_AREA[1], PROFILE_RANGE[1] + PROFILE_SIZE, CHAT_WINDOW_AREA[3])
    )
    return pic.crop(PROFILE_ROWS[0]), pic.crop(PROFILE_ROWS[1])


@cache
def load_profile_ext_feature() -> tuple[Feature, Feature]:
    profiles = (
        input("Path to the other's profile\n对方头像的路径:\n"),
        input("Path to your own profile \n您头像的路径:\n")
    )

    def _load_profile_ext_feature(path) -> Feature:
        return Feature(
            *SIFT.detectAndCompute(
                cv2.resize(
                    cv2.imread(path, cv2.IMREAD_GRAYSCALE),
                    (PROFILE_SIZE, PROFILE_SIZE)
                ),
                mask=  # All pixels for profile pictures
                np.ones(
                    (PROFILE_SIZE, PROFILE_SIZE), dtype=np.bool_
                )
            )
        )

    return _load_profile_ext_feature(profiles[0]), _load_profile_ext_feature(profiles[1])


FEATURES = load_profile_ext_feature()
