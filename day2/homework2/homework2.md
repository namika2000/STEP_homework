## why tree structures are used over hash tables in large databases

1. Because while hash tables require ingenuity in the creation of hash functions, tree structures are simple to create.
   * In order to perform an O(1) operation using a hash table, it is necessary to devise the hash function to reduce hash value collisions.
   * On the other hand, in a tree structure, O(logn) operations can be performed simply by adding data according to the conditions.

2. When data increases, a tree structure can handle the problem in a simpler way and with less computation.
   * When data increases, tree rotation is used in tree structures to search, delete, and add data with the same computational complexity(O(logn)). Its computational complexity is O(1).
   * On the other hand, there are two methods for hash tables to perform operations without changing the amount of computation when data increases: re-hashing and multi-stage hashing.
     * re-hashing: its computational complexity is O(n). Thus, the overall computational complexity, including re-hashing, is O(n), which is bigger than those of tree structures
     * Multi-stage hashing: it requires a large number of hash functions, and the hash functions themselves need to be devised, which can be difficult.