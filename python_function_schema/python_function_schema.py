#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from pulsar import Function

from pulsar.schema import *


class Person(Record):
    name = String()
    phone = String()


class Schema:
    schema = None

    def __init__(self, *args):
        self.schema = args[0]

    def __call__(self, f):
        def wrapped(*args):
            args = list(args)
            args[1] = self.schema.decode(args[1].encode())
            return self.schema.encode(f(*tuple(args))).decode("utf-8")

        return wrapped

# Function that deals with custom objects
class CustomObjectFunction(Function):
  def __init__(self):
    pass

  @Schema(JsonSchema(Person))
  def process(self, input, context):
    logger = context.get_logger()
    logger.info("Message: {0}".format(input))
    logger.info("Name: {0}".format(input.name))
    return input
