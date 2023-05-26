import random

import QuanmSmsSDK

Sms = QuanmSmsSDK.SDK();
Code = random.randint(1000, 9999)
for i in range(100):
    jg = Sms.send('17526672912', 0, {'code': Code})
    print(jg)
    print('验证码是：' + str(Code))
