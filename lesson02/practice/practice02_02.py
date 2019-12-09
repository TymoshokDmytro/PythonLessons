import traceback

class Store:

    _overall_sold_items = 0

    def __init__(self, store_name, sold_items):
        self._store_name = store_name
        self._sold_items = sold_items
        Store._overall_sold_items += sold_items

    def _inc_sold_items(self, count):
        self._sold_items += count
        Store._overall_sold_items += count

    def _dec_sold_items(self, count):
        if (self._sold_items - count) < 0:
            raise Exception('Cannot refund items. Someone trying to refund thing that was not in store')
        self._sold_items -= count
        Store._overall_sold_items -= count

    def sell(self, count):
        self._inc_sold_items(count)

    def refund(self, count):
        self._dec_sold_items(count)

    def get_store_name(self):
        return self._store_name

    def get_store_sold_count(self):
        return self._sold_items

    def get_overall_sold_count(self):
        return Store._overall_sold_items

    def __str__(self):
        return 'StoreName: ' + self._store_name + \
              "\n Store sold items: " + str(self.get_store_sold_count()) + \
              "\n Overall sold items: " + str(self.get_overall_sold_count())


def printStores():
    print(store_1)
    print(store_2)
    print()

try:
    store_1 = Store('1 store', 4)
    store_2 = Store('2 store', 2)
    printStores()

    print('store 1 sell 2')
    store_1.sell(2)
    printStores()

    print('store 1 refund 4')
    store_1.refund(4)
    printStores()

    print('store 2 sell 3')
    store_2.sell(3)
    printStores()

    print('store 2 refund 5')
    store_2.refund(5)
    printStores()

    print('store 2 refund 1')
    store_2.refund(1)
    printStores()
except:
    print(traceback.format_exc())