# Copyright (c) 2022, Kirill Ivanov, Anastasiia Kornilova and Dmitrii Iarosh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pytest

from src.metrics.detection.structural.constants import EVALUATION_RESOLUTION
from src.metrics.detection.structural.distance.tp_indicator import (
    __calculate_structural_tp_indicators,
    __calculate_orthogonal_tp_indicators,
    __calculate_tp_indicators,
)


@pytest.mark.parametrize(
    "pred_lines, gt_lines, expected",
    [
        (
            np.array([[1, 0, 2, 0], [2, 0, 1, 0], [5, 9, 11, 13]]),
            np.array([[1, 0, 2, 0], [5, 10, 11, 12]]),
            np.array([True, False, True]),
        ),
        (
            np.array([[1, 0, 2, 0]]),
            np.array([[1, 2, 2, 2]]),
            np.array([False]),
        ),
    ],
)
def test_calculate_structural_tp_indicators(pred_lines, gt_lines, expected):
    actual = __calculate_structural_tp_indicators(pred_lines, gt_lines)
    assert (actual == expected).all()


@pytest.mark.parametrize(
    "pred_lines, gt_lines, expected",
    [
        (
            np.array([[0, 0, 5, 0]]),
            np.array([[0, 2, 5, 2]]),
            np.array([True]),
        ),
        (
            np.array([[0, 0, 5, 0]]),
            np.array([[0, 5, 5, 5]]),
            np.array([False]),
        ),
    ],
)
def test_calculate_orthogonal_tp_indicators(pred_lines, gt_lines, expected):
    actual = __calculate_orthogonal_tp_indicators(pred_lines, gt_lines)
    assert (actual == expected).all()


@pytest.mark.parametrize(
    "pred_lines, gt_lines",
    [
        (
            np.array([[0, 0, 0, 0]]),
            np.array([[1, 1, 2, 2]]),
        ),
        (
            np.array([[1, 1, 2, 2]]),
            np.array([[0, 0, 0, 0]]),
        ),
    ],
)
def test_zero_length_line(pred_lines, gt_lines):
    with pytest.raises(ValueError):
        __calculate_tp_indicators(pred_lines, gt_lines, 5)


@pytest.mark.parametrize(
    "pred_lines, gt_lines",
    [
        (
            np.array([[1, 1, 2, 2]]),
            np.array([[1, 1, 2, 2]]) * EVALUATION_RESOLUTION,
        ),
        (
            np.array([[1, 1, 2, 2]]) * EVALUATION_RESOLUTION,
            np.array([[1, 1, 2, 2]]),
        ),
    ],
)
def test_length_line_greater_than_resolution(pred_lines, gt_lines):
    with pytest.raises(ValueError):
        __calculate_tp_indicators(pred_lines, gt_lines, 5)