class HashItem:
    def __init__(self, key, value):
        self.key = key  # key is now task_id
        self.value = value # value is (task_id, description, priority, completed)

class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.size = 0

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._hash(key)

        if self.items[index] is None:
            self.items[index] = HashItem(key, value)
            self.size += 1
        else:
            if self.items[index].key == key:
                self.items[index].value = value  # Update existing task
            else:
                # Linear Probing
                next_index = (index + 1) % self.capacity
                while next_index != index:
                    if self.items[next_index] is None:
                        self.items[next_index] = HashItem(key, value)
                        self.size += 1
                        return
                    if self.items[next_index].key == key:
                        self.items[next_index].value = value
                        return
                    next_index = (next_index + 1) % self.capacity
                raise Exception("HashTable is full") # Handle full table.

    def get(self, key):
        index = self._hash(key)
        if self.items[index] is not None and self.items[index].key == key:
            return self.items[index].value
        else:  # Linear Probing
            next_index = (index + 1) % self.capacity
            while next_index != index:
                if (
                    self.items[next_index] is not None
                    and self.items[next_index].key == key
                ):
                    return self.items[next_index].value
                next_index = (next_index + 1) % self.capacity
            return None

    def delete(self, key):
        index = self._hash(key)

        if self.items[index] is not None and self.items[index].key == key:
            self.items[index] = None  # Simple deletion (lazy deletion)
            self.size -= 1
        else:  # Linear Probing
            next_index = (index + 1) % self.capacity
            while next_index != index:
                if (
                    self.items[next_index] is not None
                    and self.items[next_index].key == key
                ):
                    self.items[next_index] = None
                    self.size -= 1
                    return  # Exit after deleting
                next_index = (next_index + 1) % self.capacity

    def get_all_values(self):
        values = []
        for item in self.items:
            if item is not None:
                values.append(item.value)
        return values
    
    def search_by_description(self, description):
        tasks = []
        for task in self.get_all_values():
            if description in task[1]:
                tasks.append(task)
        return tasks