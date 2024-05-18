#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-06 23:30:26

import sys
import os
import glob
import re
import datetime
# from ExchangePackage import chart
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
データベースに辞書データを登録する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-i", "--input", metavar="directry", help="rateディレクトリ（NoneならBASE_DIR/data/rate）")
  parser.add_argument("-c", "--clean", action="store_true", help="初期化")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LerningProject.settings")
  import django
  django.setup()
  from django.conf import settings
  from english.models import PublicEn2JpDictionaryTable
  if options.clean:
    if "y" == input("Are you sure you want to delete all data? (y/n)"):
      PublicEn2JpDictionaryTable.objects.all().delete()
  obj_list = []
  with open(options.file, "r") as f:
    for line in f:
      row = line.strip().split("\t")
      if len(row) != 2:
        raise ValueError(f"line {x} is invalid.")
      div = row[0].split(",")
      if len(div)>1:
        div = [d.strip() for d in div]
        for d in div:
          obj = PublicEn2JpDictionaryTable(word=d, mean=row[1])
          obj_list.append(obj)
      else:
        obj = PublicEn2JpDictionaryTable(word=row[0], mean=row[1])
        obj_list.append(obj)
  PublicEn2JpDictionaryTable.objects.bulk_create(obj_list, ignore_conflicts=True)


if __name__ == '__main__':
  main()
