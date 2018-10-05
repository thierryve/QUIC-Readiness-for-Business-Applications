from test import Test, TestObject
from network import Network


testObjects = [TestObject('https://crm.thierryve.nl/index.php?action=Login&module=Users', 'http://crm.thierryve.nl')]

Network().reset()

Test('log/none.json', 'none').run(testObjects)

Network().reset()
Network().delay(200)
Test('log/latency.json', 'latency_200').run(testObjects)

Network().reset()
Network().packetloss(1)
Test('results/packetloss.json', 'packetloss_1').run(testObjects)

Network().reset()
Network().packetlossburst(1, 25)
Test('results/packetlossburst.json', 'packetlossburst_125').run(testObjects)

Network().reset()
Network().duplication(10)
Test('results/duplication.json', 'duplication_10').run(testObjects)

Network().reset()
Network().corruption(1)
Test('results/corruption.json', 'corruption_1').run(testObjects)

Network().reset()
Network().reordering(10, 25, 50)
Test('results/reordering.json', 'reordering2550').run(testObjects)

Network().reset()
