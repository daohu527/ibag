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


from modules.map.proto import map_pb2
from common.convert import convert


class RosbagToRecord:
  def __init__(self) -> None:
    pass


class Map:
  def __init__(self):
    self.parking_space = []


class Projection:
  def __init__(self, proj):
    self.proj = proj

class Header:
  def __init__(self, version, date, projection, left, right):
    self.version = version.encode()
    self.date = date.encode()
    self.projection = projection
    self.left = left
    self.right = right

class Id:
  def __init__(self, id):
    self.id = id

class ParkingSpace:
  def __init__(self, id, polygon, overlap_id, heading):
    self.id = id
    self.polygon = polygon
    self.overlap_id = overlap_id
    self.heading = heading

obj_map = Map()

obj_map.header = Header("v1.0", "2022", Projection("proj"), 1.0, 2.0)

pk1 = ParkingSpace(Id("1"), None, [Id("o1"), Id("o2")], 1.0)
pk2 = ParkingSpace(Id("2"), None, [Id("o3"), Id("o4")], 2.0)
obj_map.parking_space.append(pk1)
obj_map.parking_space.append(pk2)

if __name__ == '__main__':
  pb_map = map_pb2.Map()

  # print(dir(obj_map))
  # print(dir(pb_map))

  convert(obj_map, pb_map)

  print(pb_map)
