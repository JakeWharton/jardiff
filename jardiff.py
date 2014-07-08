#!/usr/bin/env python

import os
import re
import shutil
import stat
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


def _split_info_into_infos(info):
  original = re.findall(r'Compiled from ".*?\.java"\n.*?\n(?:  .*\n)*}\n', info, flags=re.MULTILINE)
  infos = {}
  for info in original:
    lines = str(info).split('\n')[1:]
    header = lines[0]
    if not header.startswith('public '):
      continue
    match = re.match(r'(?:public |abstract |class |interface |final )+([^ ]+) .*', header)
    name = match.group(1)
    infos[name] = '\n'.join(lines)
  return infos


def _write_infos_to_temp(temp_folder, original_stat, infos):
  times = (original_stat[stat.ST_ATIME], original_stat[stat.ST_MTIME])

  for name, info in infos.items():
    out = os.path.join(temp_folder, name)
    with open(out, 'w') as f:
      f.write(info)
    os.utime(out, times)


def _exec_diff(dir, one_path, two_path):
  one_path = os.path.relpath(one_path, dir)
  two_path = os.path.relpath(two_path, dir)
  subprocess.call(['diff', '-U', '0', '-N', one_path, two_path], cwd=dir)


def process_archive(temp_folder, jar):
  name = os.path.splitext(os.path.basename(jar))[0]
  jar_stat = os.stat(jar)
  archive_folder = os.path.join(temp_folder, name)
  os.mkdir(archive_folder)

  unaar = None
  if jar.endswith('.aar'):
    unaar = _unzip(jar)
    jar = os.path.join(unaar, 'classes.jar')

  unjar = _unzip(jar)
  classes = _class_files(unjar)
  info = _javap_public(classes)
  infos = _split_info_into_infos(info)

  _write_infos_to_temp(archive_folder, jar_stat, infos)

  shutil.rmtree(unjar)
  if unaar is not None:
    shutil.rmtree(unaar)

  return archive_folder

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: %s old.jar new.jar' % sys.argv[0])
    sys.exit(1)

  temp_folder = tempfile.mkdtemp()

  old_archive = sys.argv[1]
  old_data = process_archive(temp_folder, old_archive)

  new_archive = sys.argv[2]
  new_data = process_archive(temp_folder, new_archive)

  _exec_diff(temp_folder, old_data, new_data)

  shutil.rmtree(temp_folder)
