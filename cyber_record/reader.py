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
  def __init__(self, section_type=None, data_size=None) -> None:
    self.type = section_type
    self.size = data_size


class Reader:
  def __init__(self, bag) -> None:
    self.bag = bag

  def start_reading(self):
    header = self.read_file_header_record()


  def reindex(self):
    pass

  def read_messages(self):
    pass

  def _read_section(self, section):
    section.type = self.bag._file.read(4)
    section.size = self.bag._file.read(8)

  def _read_message(self, proto_message):
    section = Section()
    self._read_section(section)

    if section.type != type(proto_message):
      return False

    data = self.bag._file.read(section.size)
    proto_message.ParseFromString(data)
    return True

  def read_file_header_record(self):
    self.bag._file_header_pos = self.bag._file.seek(0, 0)

    proto_header = record_pb2.Header()

    r = self._read_message(proto_header)

    if r:
      return proto_header
    else:
      return None

  def read_connection_record(self):
    pass

  def read_chunk_info_record(self):
    pass

  def read_chunk_header(self):
    pass

