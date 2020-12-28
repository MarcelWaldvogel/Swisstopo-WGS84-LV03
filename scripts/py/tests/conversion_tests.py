#!/usr/bin/python3
#
# The MIT License (MIT)
#
# Copyright (c) 2020 Marcel Waldvogel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv

from wgs84_ch1903 import GPSConverter


# Maximum allowed difference: About 2m
def deg_close(a, b):
    return abs(a - b) < 2 * 10 ** -5


def m_close(a, b):
    return abs(a - b) < 2


def match_deg(a, b):
    if deg_close(a[0], b[0]) and deg_close(a[1], b[1]) and m_close(a[2], b[2]):
        return None
    else:
        return AssertionError("(%f, %f, %f) too far off (%f, %f, %f)" % (*a, *b))


def match_m(a, b):
    if m_close(a[0], b[0]) and m_close(a[1], b[1]) and m_close(a[2], b[2]):
        return None
    else:
        return AssertionError("(%f, %f, %f) too far off (%f, %f, %f)" % (*a, *b))


def read_csv(fn):
    contents = []
    with open(fn, mode='r', newline='') as f:
        csvreader = csv.reader(f, delimiter='\t')
        for row in csvreader:
            contents.append(tuple(map(float, row)))
    return contents


def setup_module():
    global wgs84
    global lv03
    global lv95
    global convert
    wgs84 = read_csv('tests/wgs84.csv')
    lv03 = read_csv('tests/lv03.csv')
    lv95 = read_csv('tests/lv95.csv')
    convert = GPSConverter()


def test_lv03towgs84():
    for i in range(len(lv03)):
        c = convert.LV03toWGS84(*lv03[i], clip=True)
        match_deg(wgs84[i], c)


def test_lv95towgs84():
    for i in range(len(lv95)):
        c = convert.LV03toWGS84(lv95[i][0] - 2000000,
                                lv95[i][1] - 1000000,
                                lv95[i][2], clip=True)
        match_deg(wgs84[i], c)


def test_wgs84tolv03():
    for i in range(len(wgs84)):
        c = convert.WGS84toLV03(*wgs84[i], clip=True)
        match_deg(lv03[i], c)
