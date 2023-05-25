# Data structure for O(1) management of cache

Prepare a HashTable class for searching, deleting, and adding caches in O(1) and a Cache class for expressing order relationships among caches.
A Cache class has as many caches as the number of memories as items, and each cache has a next property and a previous property.

* next property:
   * cache.next refers to the cache added before that cache
* previous property:
   * cache.previous refers to the cache added after that cache

For more information on cache management, please refer to the Google Document on the programs implemented in homework4