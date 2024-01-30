# hash table class to model hash table
# source: WGU - W-1_chaininghashtable_zybooks_key-value.py
class HashTable:
    # initiates table
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # insert and/or update items in hash table
    def insert(self, key, item):
        # find the bucket list for item
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # search for items in hash table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # loop over items in bucket
        for kv in bucket_list:
            # return item if found, if not then return null
            if key == kv[0]:
                return kv[1]
        return None

    # removes an item from hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # if the key is found remove the item
        if key in bucket_list:
            bucket_list.remove(key)