import unittest

from xyz.algorithm.kpm import KPM


class TestCaseKPM(unittest.TestCase):
    def test_kpm0(self):
        n = None
        t = None
        r = KPM(n, t)
        self.assertEqual(r, -1)

    def test_kpm1(self):
        n = 'asdf'
        t = None
        r = KPM(n, t)
        self.assertEqual(r, 0)

    def test_kpm2(self):
        n = None
        t = 'asdf'
        r = KPM(n, t)
        self.assertEqual(r, -1)

    def test_kpm3(self):
        n = ''
        t = ''
        r = KPM(n, t)
        self.assertEqual(r, 0)

    def test_kpm4(self):
        n = 'asdf'
        t = ''
        r = KPM(n, t)
        self.assertEqual(r, 0)

    def test_kpm5(self):
        n = ''
        t = 'asdf'
        r = KPM(n, t)
        self.assertEqual(r, -1)

    def test_kpm6(self):
        n = 'asdfasdf'
        t = 'fa'
        r = KPM(n, t)
        self.assertTrue(r, 0)

    def test_kpm7(self):
        n = 'asdfasdf'
        t = 'fa'
        r = KPM(n, t)
        self.assertTrue(r, 0)

    def test_kpm8(self):
        n = 'asdfasdf'
        t = '12x'
        r = KPM(n, t)
        self.assertTrue(r, -1)

    def test_kpm9(self):
        n = 'asdasdfqweoitrujzoixchgfuqawhsertkp:DZfkahsdurhwerikopzsjdfiojasdfuqweprrrrrqweuzsdfkqweoruzioxjdfasdjfa' \
            'pasdfqioweuryokzmx;dlfkoaihuishgtioqw94051yu3285hjpasdrf891782y3h5uiahsd90rfyu98wyh45rtoiqjhw30954rur092' \
            'oisjdasdf9j98243785tiusdhfr87weyrh982y3h58oiujspodtuijr09w7ue48956yhoi23h45ropjzsp9eidru809qa7e5r923j2fs' \
            'fasdqw2039uj0jijziserut898yhphdgpioqjweooZJAS094EU5JP234J5[P]ZXCVB/AWSERMN98Y98Q234U5-00-KASdofpj[09UW0f' \
            'AS809Y43985Y08hgb87y87yh98zxhdf98y1h23845hoikhoyu98Y98HOI134HOy89hnH89YHOTH987ay9r134jm;jsloidfjroiywrt8ya'
        t = 'r87weyrh98'
        r = KPM(n, t)
        self.assertTrue(r, 0)

    def test_kpm10(self):
        n = 'asdasdfqweoitrujzoixchgfuqawhsertkp:DZfkahsdurhwerikopzsjdfiojasdfuqweprrrrrqweuzsdfkqweoruzioxjdfasdjfa' \
            'pasdfqioweuryokzmx;dlfkoaihuishgtioqw94051yu3285hjpasdrf891782y3h5uiahsd90rfyu98wyh45rtoiqjhw30954rur092' \
            'oisjdasdf9j98243785tiusdhfr87weyrh982y3h58oiujspodtuijr09w7ue48956yhoi23h45ropjzsp9eidru809qa7e5r923j2fs' \
            'fasdqw2039uj0jijziserut898yhphdgpioqjweooZJAS094EU5JP234J5[P]ZXCVB/AWSERMN98Y98Q234U5-00-KASdofpj[09UW0f' \
            'AS809Y43985Y08hgb87y87yh98zxhdf98y1h23845hoikhoyu98Y98HOI134HOy89hnH89YHOTH987ay9r134jm;jsloidfjroiywrt8ya'
        t = 'r87weyrh9wser09tu9082j34oi5jm;lxk0p9orutig8'
        r = KPM(n, t)
        self.assertTrue(r, -1)


if __name__ == '__main__':
    unittest.main()
