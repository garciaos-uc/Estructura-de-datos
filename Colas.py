class Order:
    def __init__(self, qtty, customer):
        self._customer = customer
        self._qtty = qtty

    def print_order(self):
        print("     Customer:", self.get_customer())
        print("     Quantity:", self.get_qtty())
        print("     ------------")

    def get_qtty(self):
        return self._qtty

    def get_customer(self):
        return self._customer


class Node:
    def __init__(self, info, next_node=None):
        self._info = info
        self._next = next_node

    def get_info(self):
        return self._info

    def get_next(self):
        return self._next

    def set_next(self, node):
        self._next = node


class Queue:
    def __init__(self):
        self._top = None
        self._last = None
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def front(self):
        if self.is_empty():
            return None
        return self._top.get_info()

    def enqueue(self, info):
        new_node = Node(info)
        if self.is_empty():
            self._top = new_node
        else:
            self._last.set_next(new_node)
        self._last = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        info = self._top.get_info()
        self._top = self._top.get_next()
        self._size -= 1
        if self._top is None:
            self._last = None
        return info

    def get_nth(self, pos):
        if pos < 1 or pos > self._size:
            return None
        node = self._top
        for _ in range(pos - 1):
            node = node.get_next()
        return node.get_info()

    def print_info(self):
        print("********* QUEUE DUMP *********")
        print("   Size:", self._size)
        node = self._top
        i = 1
        while node is not None:
            print("   ** Element", i)
            node.get_info().print_order()
            node = node.get_next()
            i += 1
        print("******************************")


def main():
    cola = Queue()

    o1 = Order(20, "cust1")
    o2 = Order(30, "cust2")
    o3 = Order(40, "cust3")
    o4 = Order(50, "cust3")

    print(">> Cola recién creada")
    cola.print_info()

    print(">> Enqueue de 3 pedidos")
    cola.enqueue(o1)
    cola.print_info()
    cola.enqueue(o2)
    cola.print_info()
    cola.enqueue(o3)
    cola.print_info()

    print(">> Front")
    cola.front().print_order()
    cola.print_info()

    print(">> Dequeue")
    cola.dequeue().print_order()
    cola.print_info()

    print(">> Agrego dos pedidos más y pruebo get_nth(3)")
    cola.enqueue(o1)
    cola.enqueue(o4)
    cola.print_info()

    tercero = cola.get_nth(3)
    if tercero is not None:
        print(">> Tercer elemento:")
        tercero.print_order()

    print(">> Posición inválida (10):", cola.get_nth(10))


if __name__ == "__main__":
    main()