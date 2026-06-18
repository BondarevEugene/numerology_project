import hashlib
import hmac
import time


class PaymentService:
    def __init__(self, merchant_id, secret_key, domain):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.domain = domain

    def generate_signature(self, data_str):
        return hmac.new(self.secret_key.encode('utf-8'), data_str.encode('utf-8'), hashlib.md5).hexdigest()

    def create_payment_url(self, order_id, amount, user_email):
        # Формируем строку для подписи по протоколу банка
        order_time = int(time.time())
        product_name = "Полный нумерологический анализ"

        # Пример полей для WayForPay
        fields = [
            self.merchant_id, self.domain, str(order_id), str(order_time),
            str(amount), "UAH", product_name, "1", str(amount)
        ]

        signature_str = ";".join(fields)
        signature = self.generate_signature(signature_str)

        # Возвращаем данные для формы или готовую ссылку
        return {
            "url": "https://secure.wayforpay.com/pay",
            "params": {
                "merchantAccount": self.merchant_id,
                "merchantDomainName": self.domain,
                "orderReference": order_id,
                "orderDate": order_time,
                "amount": amount,
                "currency": "UAH",
                "productName[]": product_name,
                "productCount[]": "1",
                "productPrice[]": amount,
                "merchantSignature": signature,
                "serviceUrl": f"{self.domain}/payment/callback"  # Куда банк пришлет ответ
            }
        }