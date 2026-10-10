# (c) University of Sussex 2026
# Created by David Seery
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
What a ``RayWorkPool`` needs of the pool it is handed.
"""

from typing import Protocol

from ray import ObjectRef


class DatastorePool(Protocol):
    """
    The datastore pool a ``RayWorkPool`` is handed, described by the one method the pool calls.

    ``RayWorkPool`` keeps the pool it is given and otherwise does not use it: the pool is passed
    through, as the second argument, to the store handler and to the persist handler. Only the
    default persist handler, ``_default_persist_handler``, calls anything on it, and that is
    ``object_store(obj)``, with the single object a compute task has just populated; it expects
    back the ``ObjectRef`` of the datastore write, which the pool then waits on.

    So this protocol states what ``_default_persist_handler`` needs, and no more. A datastore pool
    whose ``object_store`` also accepts a list or tuple of objects satisfies it; the pool never
    passes one. A caller whose own store and persist handlers need more of the pool, or need none
    of it, or whose pool has no compute handler, and so uses neither default, may pass any object
    at all.

    It is a type hint only. It is not ``runtime_checkable``, and nothing checks it at run time.
    """

    def object_store(self, objects) -> ObjectRef: ...
