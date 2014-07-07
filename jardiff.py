#!/usr/bin/env python

import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile


def _unzip(name):
  destination = tempfile.mkdtemp()
  with zipfile.ZipFile(name) as f:
    f.extractall(destination)
  return destination


def _class_files(path):
  classes = []
  for root, dirs, files in os.walk(path):
    for file in files:
      if file.endswith('.class'):
        classes.append(os.path.join(root, file))
  return classes


def _javap_public(files):
  return subprocess.check_output(['javap', '-public'] + files)


def _only_public_classes(info):
  return re.sub(r'Compiled from ".*?\.java"\n(?!public).*?\n(?:  .*\n)*}\n', '', info, flags=re.MULTILINE)


def _remove_compiled_from(info):
  return re.sub(r'Compiled from ".*?\.java"\n', '', info, flags=re.MULTILINE)


def write_to_temp(data):
  _, destination = tempfile.mkstemp()
  with open(destination, 'w') as f:
    f.write(data)
  return destination


def _exec_diff(one_label, one_file, two_label, two_file):
  subprocess.call(['diff', '-uN', '--label', one_label, one_file, '--label', two_label, two_file])


def process_archive(jar):
  if jar.endswith('.aar'):
    unaar = _unzip(jar)
    aarjar = os.path.join(unaar, 'classes.jar')
    temp = process_archive(aarjar)
    shutil.rmtree(unaar)
    return temp

  unjar = _unzip(jar)
  classes = _class_files(unjar)
  info = _javap_public(classes)
  info = _only_public_classes(info)
  info = _remove_compiled_from(info)
  temp = write_to_temp(info)
  shutil.rmtree(unjar)
  return temp

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: %s old.jar new.jar' % sys.argv[0])
    sys.exit(1)


  old_archive = sys.argv[1]
  old_info_file = process_archive(old_archive)
  old_label = os.path.basename(old_archive)

  new_archive = sys.argv[2]
  new_info_file = process_archive(new_archive)
  new_label = os.path.basename(new_archive)

  _exec_diff(old_label, old_info_file, new_label, new_info_file)

  os.remove(old_info_file)
  os.remove(new_info_file)
