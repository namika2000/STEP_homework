import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################


# Multiply the ASKⅡ code of a character with randomly generated integer so that
# anagrams have different hash values.
def calculate_hash(key):
    assert type(key) == str
    hash = 0
    random.seed(key)
    for i in key:
        num = random.randint(0, 100)
        hash += num * ord(i)
    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    # |previous|: The previous item in linked list. If this is the last item in the
    #         linked list, |previous| is None. (optional)  #added
    def __init__(self, key, value, next, previous=None):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next
        self.previous = previous


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:
    # Initialize the hash table.
    def __init__(self, bucket_size=97, item_count=0):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = bucket_size
        self.buckets = [None] * self.bucket_size
        self.item_count = item_count

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1

        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        # ------------------------#
        # Write your code here!  #
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                # Assign (key, value, next) of the next item to the item
                if item.next:
                    item.key = item.next.key
                    item.value = item.next.value
                    item.next = item.next.next
                else:
                    self.buckets[bucket_index] = None
                self.item_count -= 1

                return True
            item = item.next
        return False
        # ------------------------#

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert self.bucket_size < 100 or self.item_count >= self.bucket_size * 0.3


# A cache object that represents retained caches in the hash table.
# It contains items which represents each cache and their sequential relationship
#
# |last|: The oldest cache
# |newest|: The newest cache
# |memory_size|: The number of caches to be stored
class Cache:
    def __init__(self, memory_size, item_count=0):
        self.last = None
        self.newest = None
        self.memory_size = memory_size
        self.item_count = item_count

    # Update retained caches in the hash table
    # If (key, value) exist in the hash table,
    # reorder caches in the order in which they were added.
    # If (key, value) doesn't exist in it and
    # the number of caches retained is lower than memory size,
    # simply add (key, value) as the newest cache.
    # Otherwise, delete the oldest cache among the retained caches and
    # add (key, value) as the newest cache.
    #
    # |key|: The key of cache newly added
    # |value|: The value of cache newly added
    # |hash_table|: the hash table that contains caches
    def cache_update(self, key, value, hash_table):
        self.check_count(hash_table)
        new_item = Item(key, value, self.newest)
        if hash_table.get(key)[0]:
            # Reorder caches
            self.reorder_cache(new_item)
        else:
            if self.item_count < self.memory_size:
                # Simply add new_item as the newest cache
                # Add new_item to the hash table too
                self.put_first(new_item)
                hash_table.put(key, value)
            else:
                # Delete the oldest cache from both cache object and hash table
                # Add new_item to both cache object and hash table as the newest cache
                self.delete_old_cache()
                hash_table.delete(self.last.key)
                self.put_first(new_item)
                hash_table.put(new_item.key, new_item.value)
        return True

    def put_first(self, new_item):
        if not self.newest:
            self.last = new_item
        if self.newest:
            self.newest.previous = new_item
        self.newest = new_item
        self.item_count += 1
        return True

    def reorder_cache(self, key):
        item = self.newest
        if item.key == key:
            return False
        flag = True
        while item:
            if item.key == key:
                flag = False
                current_item = item
                next_item = item.next
                previous_item = item.previous
                break
            item = item.next
        if flag:
            return
        previous_item.next = next_item
        next_item.previous = previous_item
        current_item.next = self.newest
        current_item.previous = None
        self.newest.previous = current_item
        return True

    def delete_old_cache(self):
        last_item = self.last
        if last_item is None:
            return False
        last_item.previous.next = None
        last_item = last_item.previous
        self.item_count -= 1
        return True

    def check_count(self, hash_table):
        assert self.item_count == hash_table.item_count


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable(bucket_size=11)
    cache_container = Cache(3)

    cache_container.cache_update("aaa", 1, hash_table)
    cache_container.cache_update("aaa", 1, hash_table)
    cache_container.cache_update("bbb", 2, hash_table)
    cache_container.cache_update("ccc", 3, hash_table)
    cache_container.cache_update("ddd", 4, hash_table)
    cache_container.cache_update("eee", 4, hash_table)

    print("Functional tests passed!")


if __name__ == "__main__":
    functional_test()
