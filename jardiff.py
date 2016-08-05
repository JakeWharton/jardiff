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


def _chunks(items, chunk_size):
  for i in range(0, len(items), chunk_size):
    yield items[i:i + chunk_size]


def _javap_public(files):
  results = []
  for chunk in _chunks(files, 200):
    results.append(str(subprocess.check_output(['javap', '-public'] + chunk)))
  return '\n'.join(results)


def _split_info_into_infos(info):
  original = re.findall(r'Compiled from ".*?\.(?:java|groovy)"\n.*?\n(?:  .*\n)*}\n', info,
                        flags=re.MULTILINE)
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


def _exec_diff(base_path, one_path, two_path):
  one_path = os.path.relpath(one_path, base_path)
  two_path = os.path.relpath(two_path, base_path)
  subprocess.call(['diff', '-U', '0', '-N', one_path, two_path], cwd=base_path)


def process_archive(temp_folder, jar):
  jar_basename = os.path.splitext(os.path.basename(jar))[0]
  filepath_hash = hex(hash(jar))[-8:]
  name = '%s_%s' % (jar_basename, filepath_hash)

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


def _main(old_archive, new_archive, diff_script=None):
  temp_folder = tempfile.mkdtemp()

  old_data = process_archive(temp_folder, old_archive)
  new_data = process_archive(temp_folder, new_archive)

  if diff_script:
    subprocess.call('%s %s %s %s' % (diff_script, temp_folder, old_data, new_data), shell = True)
  else:
    _exec_diff(temp_folder, old_data, new_data)

  shutil.rmtree(temp_folder)


if __name__ == '__main__':
  if len(sys.argv) not in [3, 4]:
    print('Usage: %s old.aar new.aar [diff_script]' % sys.argv[0])
    sys.exit(1)
  _main(*sys.argv[1:])
