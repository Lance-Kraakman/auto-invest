import unittest
from Classes.BusinessModel import Bar, Business


def generateBar(barClose):
    return Bar.Bar(close=barClose)


class SupportResistanceTest(unittest.TestCase):

    def test_SR_bracketRange(self):
        # Test detect support
        data = [1, 2, 20, 1, 5, 20, 1, 4, 5, 20]
        barData = [generateBar(item) for item in data]
        support = Business.SupportResistance(isActive=False, barList=barData, srType=Business.SupportResistance.SUPPORT, percent=0.05)
        support.updateBracketRange()

        resistance = Business.SupportResistance(isActive=False, barList=barData, srType=Business.SupportResistance.RESISTANCE, percent=0.05)
        resistance.updateBracketRange()

        print(support.lowBracket, support.highBracket)
        print(resistance.lowBracket, resistance.highBracket)

        self.assertAlmostEqual(support.lowBracket, 0.995)
        self.assertAlmostEqual(support.highBracket, 1.005)

        self.assertAlmostEqual(resistance.lowBracket, 19.9)
        self.assertAlmostEqual(resistance.highBracket, 20.1)



    def test_SR_detect_and_loop(self):
        pass

    def detectSR(self, data, type):
        pass