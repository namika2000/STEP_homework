import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################


# Hash function.
#
# |key|: string
# Return value: a hash value
def original_calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    # why: hash of anagrams is same, so hash conflicts may occur.
    hash = 0
    for i in key:
        hash += ord(i)
    return hash


# a hash function that occurred to me at first
# Multiply the ASKⅡ code of a character with the number of the character in strings so that
# anagrams have different hash values.
def first_calculate_hash(key):
    assert type(key) == str
    hash = 0
    for idx, s in enumerate(key):
        hash += idx * ord(s)
    return hash


# The updated hash function
# Cannot be used with performance_test function (I'm not sure why)
# Maybe because both function use random.seed, so different random numbers are created with the same key?
#
# Multiply the ASKⅡ code of a character with randomly generated integer so that
# anagrams have different hash values.
def updated_calculate_hash(key):
    assert type(key) == str
    hash = 0
    random.seed(key)
    for i in key:
        num = random.randint(0, 1000)
        hash += num * ord(i)
    return hash


# The hash function, which is used in the code
def calculate_hash(key):
    assert type(key) == str
    hash = 0
    for i in key:
        hash = int(hash * 128 + ord(i))
    return hash


# Determine if the number is prime or not
#
# |num|: number to check
# Return value: True or False
# True if |num| is prime number
# Otherwise, False
def is_prime(num):
    square_num = int(num**0.5)
    if num == 1:
        return False
    for i in range(2, square_num + 1, 2):
        if num % i == 0:
            return False
    return True


# Return the nearest prime number that is less than or equal to the number
def prime_before(num):
    while num >= 2:
        if is_prime(num):
            return num
        num -= 1
    return None


# Return the nearest prime number that is more than or equal to the number
def prime_next(num):
    while True:
        if is_prime(num):
            return num
        num += 1


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
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
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added.
    # False if the key already exists
    # and the value is updated.
    def put(self, key, value, not_rehash=True):
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
        if self.buckets[bucket_index]:
            self.buckets[bucket_index].previous = new_item
        self.buckets[bucket_index] = new_item
        if not_rehash:
            self.item_count += 1

        # Rehash
        if self.item_count > self.bucket_size * 0.7:
            new_bucket_size = prime_next(self.bucket_size * 2)
            self.rehashing(new_bucket_size)
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
                # Connect item's next and previous with a pointer and skip the item
                if item.previous:
                    if item.next:
                        item.next.previous = item.previous
                    item.previous.next = item.next
                else:
                    if item.next:
                        item.next.previous = None
                    self.buckets[bucket_index] = item.next
                self.item_count -= 1

                # Rehash
                if (self.item_count < self.bucket_size * 0.3) and (self.bucket_size >= 100):
                    new_bucket_size = prime_before(self.bucket_size // 2)
                    if new_bucket_size % 2 == 0:
                        new_bucket_size -= 1
                    self.rehashing(new_bucket_size)

                return True
            else:
                item = item.next
        return False
        # ------------------------#

    # Rehash the current hash table
    # Double the size of it if the buckets are 70% or more used
    # Half the size of it if they are 30% or less used
    #
    # |new_bucket_size|: the bucket_size of the new hash table
    def rehashing(self, new_bucket_size):
        item_list = []
        for idx in range(self.bucket_size):
            item = self.buckets[idx]
            while item:
                item_list.append([item.key, item.value])
                item = item.next

        self.buckets = [None] * new_bucket_size
        self.bucket_size = new_bucket_size
        for item in item_list:
            key, value = item
            self.put(key, value, not_rehash=False)

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


# Test the performance of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))
        print("%d %.6f" % (iteration, end - begin))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
