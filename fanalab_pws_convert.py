#!/usr/bin/env python

import xml.etree.ElementTree
import glob
import os
import json
import argparse
import pathlib
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("src", type=pathlib.Path, help="source directory for copy and scale")
parser.add_argument("dst", type=pathlib.Path, help="destination directory for copy and scale")
parser.add_argument("-s", "--scale_factor", type=float, help="the scaling factor to convert the FF to", default=1.25)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()

src_path = args.src.resolve()
dst_path = args.dst.resolve()

print("Converting \"" + str(src_path) + "\" to \"" + str(dst_path) + "\" with a scaling factor of " + str(args.scale_factor))

if (not os.path.exists(src_path)):
    print("src directory doesn't exist")
    exit(1)
    
if (os.path.exists(dst_path)):
    print("dst directory already exists")
    exit(1)
    
shutil.copytree(src_path, dst_path)
    
os.chdir(dst_path)

for file in glob.glob("**/*.pws", recursive=True):
    et = xml.etree.ElementTree.parse(file)
    root = et.getroot()
    
    if (args.verbose):
        print(file)

    for profile in root.iter('TuningMenuProfile'):
        for json_settings_node in profile.iter('JSON'):
            if (args.verbose):
                print(json_settings_node.text)
            json_settings = json.loads(json_settings_node.text)
            json_settings["FF"] = int(float(json_settings["FF"]) * args.scale_factor)
            json_settings_node.text = json.dumps(json_settings, separators=(',', ':'))
            if (args.verbose):
                print(json_settings["FF"])

    et.write(file)
