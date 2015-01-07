

# relstorage monkey patch for zodbupdate compatibility
#  BIG caveat: FileStoreage record_iternext() is only current records; this
#              will only ever work on a history-free or zero-day-packed
#              RelStorage, and as such it is a hack.

import itertools
from relstorage.storage import RelStorage


def record_iternext(self, next=None):
    record_iterator = next
    if not isinstance(record_iterator, itertools.chain):
        record_iterator = itertools.chain(*self.iterator())
    record = record_iterator.next()
    return (
        record.oid,
        record.tid,
        record.data,
        record_iterator  # next usally oid, we cheat here, pass caller iterator
        )

RelStorage.record_iternext = record_iternext  # patch

# /relstorage patch
