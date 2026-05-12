import hashlib
import hmac
import time


class WayForPayService:
    def __init__(self, merchant_id, secret_key, domain):
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.domain = domain  # Например: https://your-site.com

    def _generate_signature(self, data_list):
        """Создает HMAC-MD5 подпись для безопасности"""
        base_string = ";".join(map(str, data_list))
        return hmac.new(
            self.secret_key.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.md5
        ).hexdigest()

    def prepare_payment_data(self, order_id, amount, user_email, product_name="Полный анализ личности"):
        order_time = int(time.time())

        # Поля, которые требует WayForPay для формирования подписи (строгий порядок!)
        data_to_sign = [
            self.merchant_id,
            self.domain,
            order_id,
            order_time,
            amount,
            "UAH",
            product_name,
            1,  # Количество
            amount  # Цена за единицу
        ]

        signature = self._generate_signature(data_to_sign)

        # Возвращаем словарь параметров для HTML-формы
        return {
            "merchantAccount": self.merchant_id,
            "merchantDomainName": self.domain,
            "merchantSignature": signature,
            "orderReference": order_id,
            "orderDate": order_time,
            "amount": amount,
            "currency": "UAH",
            "productName[]": product_name,
            "productPrice[]": amount,
            "productCount[]": 1,
            "clientEmail": user_email,
            "serviceUrl": f"{self.domain}/payment/callback"  # Сюда банк пришлет подтверждение
        }