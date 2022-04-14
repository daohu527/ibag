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


from google.protobuf import message_factory, descriptor_pb2
from cyber.proto import record_pb2, proto_desc_pb2



SECTION_LENGTH = 16
HEADER_LENGTH = 2048


class Section:
  def __init__(self, section_type=None, data_size=0) -> None:
    self.type = section_type
    self.size = data_size

  def __str__(self):
    return "Section type: {}, size: {}".format(self.type, self.size)


class Reader:
  def __init__(self, bag) -> None:
    self.bag = bag
    self.chunk_header_indexs = []
    self.chunk_body_indexs = []
    self.channels = {}


  def start_reading(self):
    header = self.read_header()
    self.bag._size = header.size
    print(header)

    indexs = self.read_indexs(header)
    for single_index in indexs.indexes:
      if single_index.type == record_pb2.SECTION_CHUNK_HEADER:
        self.chunk_header_indexs.append(single_index)
      elif single_index.type == record_pb2.SECTION_CHUNK_BODY:
        self.chunk_body_indexs.append(single_index)
      elif single_index.type == record_pb2.SECTION_CHANNEL:
        name = single_index.channel_cache.name
        self.channels[name] = single_index.channel_cache
      else:
        print("Unknown Index type!")

    print(indexs)

    self.read_records()

    # for chunk_body_index in self.chunk_body_indexs:
    #   chunk_body = self.read_chunk_body(chunk_body_index)


  def reindex(self):
    pass

  def read_messages(self):
    pass

  def _read_section(self, section):
    section.type = int.from_bytes(self.bag._file.read(4), byteorder='little')
    self.bag._file.seek(4, 1)
    section.size = int.from_bytes(self.bag._file.read(8), byteorder='little')
    print(section)

  def read_header(self):
    self.bag._file_header_pos = self.bag._file.seek(0, 0)

    section = Section()
    self._read_section(section)

    if section.type != record_pb2.SECTION_HEADER:
      return None

    proto_header = record_pb2.Header()
    data = self.bag._file.read(section.size)
    if len(data) != section.size:
      print("Header is incomplete, \
          actual size: {}, required size: {}".format(len(data), section.size))
      return None

    proto_header.ParseFromString(data)
    self.bag._file.seek(HEADER_LENGTH + SECTION_LENGTH, 0)
    return proto_header


  def read_indexs(self, header):
    self.bag._file.seek(header.index_position, 0)

    section = Section()
    self._read_section(section)

    if section.type != record_pb2.SECTION_INDEX:
      return None

    proto_indexs = record_pb2.Index()
    data = self.bag._file.read(section.size)
    if len(data) != section.size:
      print("Index is incomplete, \
          actual size: {}, required size: {}".format(len(data), section.size))
      return None

    proto_indexs.ParseFromString(data)
    return proto_indexs

  def read_chunk_body(self, chunk_body_index):
    self.bag._file.seek(chunk_body_index.position, 0)
    section = Section()
    self._read_section(section)

    if section.type != record_pb2.SECTION_CHUNK_BODY:
      return None

    chunk_body = record_pb2.ChunkBody()
    data = self.bag._file.read(section.size)
    if len(data) != section.size:
      print("ChunkBody is incomplete, \
          actual size: {}, required size: {}".format(len(data), section.size))
      return None

    chunk_body.ParseFromString(data)
    return chunk_body


  def read_chunk_header(self):
    pass

  def read_records(self):
    self.bag._file.seek(HEADER_LENGTH + SECTION_LENGTH, 0)

    while self.bag._file.tell() != self.bag._size:
      section = Section()
      self._read_section(section)
      data = self.bag._file.read(section.size)

      if section.type == record_pb2.SECTION_CHUNK_HEADER:
        proto_chunk_header = record_pb2.ChunkHeader()
        proto_chunk_header.ParseFromString(data)
      elif section.type == record_pb2.SECTION_INDEX:
        proto_indexs = record_pb2.Index()
        proto_indexs.ParseFromString(data)
      elif section.type == record_pb2.SECTION_CHUNK_BODY:
        proto_chunk_body = record_pb2.ChunkBody()
        proto_chunk_body.ParseFromString(data)
        for message in proto_chunk_body.messages:
          self.create_message(message)
          # Todo(zero): need to delete
          break
      else:
        pass

  def create_message(self, single_message):
    channel_cache = self.channels[single_message.channel_name]

    proto_desc = proto_desc_pb2.ProtoDesc()
    proto_desc.ParseFromString(channel_cache.proto_desc)
    # print(proto_desc)

    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.ParseFromString(proto_desc.desc)

    proto_type = message_factory.MessageFactory().GetPrototype(file_proto.DESCRIPTOR)
    proto_message = proto_type()
    print(type(proto_message))
    # proto_message.ParseFromString(single_message.content)

