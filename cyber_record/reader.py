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


import google.protobuf.message_factory


from cyber.proto import record_pb2


class Section:
  def __init__(self, section_type=None, data_size=0) -> None:
    self.type = section_type
    self.size = data_size

  def __str__(self):
    return "Section type: {}, size: {}".format(self.type, self.size)


class Reader:
  def __init__(self, bag) -> None:
    self.bag = bag

  def start_reading(self):
    header = self.read_file_header_record()
    print(header)

  def reindex(self):
    pass

  def read_messages(self):
    pass

  def _read_section(self, section):
    section.type = int.from_bytes(self.bag._file.read(4), byteorder='little')
    self.bag._file.seek(4, 1)
    section.size = int.from_bytes(self.bag._file.read(8), byteorder='little')

  def read_file_header_record(self):
    self.bag._file_header_pos = self.bag._file.seek(0, 0)

    section = Section()
    self._read_section(section)

    print(section)

    if section.type != record_pb2.SECTION_HEADER:
      return None

    proto_header = record_pb2.Header()
    data = self.bag._file.read(section.size)
    if len(data) != section.size:
      print("Header is incomplete, actual required size is {}".format(section.size))
      return None

    proto_header.ParseFromString(data)
    return proto_header

  def read_connection_record(self):
    pass

  def read_chunk_info_record(self):
    pass

  def read_chunk_header(self):
    pass

