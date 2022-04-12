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


class Record:
  '''
  The record file
  '''
  def __init__(self, file_name, mode='r'):
    pass

  def __iter__(self):
    return self.read_messages()

  def __enter__(self):
    pass

  def __exit__(self):
    pass

  @property
  def options(self):
    pass

  @property
  def filename(self):
    pass

  @property
  def version(self):
    pass

  @property
  def mode(self):
    pass

  @property
  def size(self):
    pass

  def _get_chunk_threshold(self):
    pass

  def _set_chunk_threshold(self, chunk_threshold):
    pass

  def read_messages(self, topics=None, duration=None):
    pass

  def flush(self):
    pass

  def write(self, topic, msg, t=None, raw=False, proto_descriptor=None):
    pass

  def reindex(self):
    pass

  def close(self):
    pass

  def get_message_count(self, topic_filters=None):
    pass

  def __str__(self):
    pass


  # internal interface
  def _read_message(self, position, raw=False, return_proto_descriptor=False):
    pass

  def _get_descriptors(self, topics=None, descriptor_filter=None):
    pass

  def _get_entries(self, descriptors=None, start_time=None, end_time=None):
    pass

  def _get_entry(self, t, descriptors=None):
    pass

  def _clear_index(self):
    pass

  def _open(self, f, mode, allow_unindexed):
    pass

  def _close_file(self):
    pass

  def _write_file_header_record(self):
    pass

  def _write_connection_record(self):
    pass

  def _write_message_data_record(self):
    pass

  def _write_chunk_header(self):
    pass

  def _write_connection_index_record(self):
    pass

  def _write_chunk_info_record(self):
    pass
