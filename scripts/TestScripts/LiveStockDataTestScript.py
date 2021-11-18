from Classes.BusinessModel import Business
import threading

condition = threading.Condition()
flag = False


def testScript():
    liveStockData = Business.LiveStockData(10)

    liveStockData.addTicker("BINANCE:BTCUSDT")
    liveStockData.startStockDataConnection()

    # bitCoinDataQueue = liveStockData.getStockQueue("BINANCE:BTCUSDT")
    print("Hi")

    global flag

    while True:
        print(flag)
        if flag:
            print("yeet")
            break


def checkExit():
    global flag
    while True:
        inp = input("Enter X to exit")
        if inp.lower() == "x":
            flag = True
            break


if __name__ == "__main__":
    thread1 = threading.Thread(target=testScript, args=())
    thread2 = threading.Thread(target=checkExit, args=())

    thread1.start()
    thread2.start()


