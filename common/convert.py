#!/usr/bin/env python

# Copyright 2022 daohu527 <daohu527@gmail.com>
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


def convert(py_object, pb_object):
  pb_attrs = pb_object.DESCRIPTOR.fields_by_name.keys()
  for attr in dir(py_object):
    if attr not in pb_attrs:
      # print("{} not in {}".format(attr, pb_object.__class__))
      continue

    py_child = getattr(py_object, attr)
    cls = type(py_child)
    # print(attr)
    # print(cls)
    if cls in (int, float, bool, str, bytes):
      setattr(pb_object, attr, py_child)
    elif isinstance(py_child, (tuple, list)):
      for py_one in py_child:
        pb_one = getattr(pb_object, attr).add()
        convert(py_one, pb_one)
    elif isinstance(cls, type):
      pb_child = getattr(pb_object, attr)
      convert(py_child, pb_child)
    else:
      pass
