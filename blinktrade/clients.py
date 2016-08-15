from datetime import datetime
import hashlib
import hmac
import time
from abc import ABCMeta
from functools import partial

import requests

from blinktrade import consts, exceptions


class AbstractClient(object):
    __metaclass__ = ABCMeta

    API_VERSION = 'v1'

    def __init__(self, environment_type, currency, broker):
        """
        :type environment_type: basestring
        :type currency: basestring
        :type broker: basestring
        """
        self.environment_type = self.validate_environment_type(environment_type)
        self.environment_server = consts.ENVIRONMENT_TO_SERVER_MAP[self.environment_type]
        self.currency = self.validate_currency(currency)
        self.broker = self.validate_broker(broker)

    @staticmethod
    def validate_environment_type(env):
        if env.upper() not in consts.ENVIRONMENTS_CHOICES:
            raise ValueError('Invalid environment. Valid options are: {}'.format(consts.ENVIRONMENTS_CHOICES))
        return env

    @staticmethod
    def validate_currency(currency):
        if currency.upper() not in consts.CURRENCIES_CHOICES:
            raise ValueError('Invalid currency. Valid options are: {}'.format(consts.CURRENCIES_CHOICES))
        return currency

    @staticmethod
    def validate_broker(broker):
        if str(broker) not in consts.BROKERS_CHOICES:
            raise ValueError('Invalid Broker. Valid options are: {}'.format(consts.BROKERS_CHOICES))
        return broker


class OpenClient(AbstractClient):
    def get_ticker(self):
        """
        :rtype: dict
        """
        return self._get_market_data(consts.MarketInformation.TICKER)

    def get_order_book(self):
        """
        :rtype: dict
        """
        return self._get_market_data(consts.MarketInformation.ORDER_BOOK)

    def get_trade_list(self, since_ts=0):
        """
        :type: long
        :rtype: list[dict]
        """
        return self._get_market_data(consts.MarketInformation.TRADES, '?since={}'.format(since_ts))

    def _get_market_data(self, requested_info, params=''):
        url = '{domain}/blinktrade/{version}/{currency}/{type}{params}'.format(
            domain=self.environment_server,
            version=self.API_VERSION,
            currency=self.currency,
            type=requested_info,
            params=params,
        )
        return requests.get(url).json()


class AuthClient(AbstractClient):
    SATOSHI_COLUMNS = ['CumQty', 'OrderQty', 'CxlQty', 'LeavesQty', 'Price', 'Volume', 'LastPx', 'AvgPx']

    def __init__(self, environment_type, currency, broker, key, secret):
        super(AuthClient, self).__init__(environment_type, currency, broker)
        self.key = key
        self.secret = secret

    def get_balance(self):
        msg = {
            'MsgType': consts.MessageType.BALANCE,
            'BalanceReqID': self._get_unique_id(),
        }
        response = self._send_request(msg)
        broker = [broker[self.broker] for broker in response['Responses'] if broker.get(str(self.broker))]
        broker = broker[0] if broker else {}
        return self._make_balance_from_broker_dict(broker)

    def _make_balance_from_broker_dict(self, broker):
        """
        :type broker: dict
        :return: trading_system.blinktrade.beans.Balance
        """
        return {currency: self._get_decimal_value(value) for currency, value in broker.items()}

    def buy_bitcoins_with_limited_order(self, price, quantity):
        return self._place_order(consts.OrderSide.BUY, consts.OrderType.LIMITED_ORDER, price, quantity)

    def buy_bitcoins_with_market_order(self, price, quantity):
        return self._place_order(consts.OrderSide.BUY, consts.OrderType.MARKET, price, quantity)

    def sell_bitcoins_with_limited_order(self, price, quantity):
        return self._place_order(consts.OrderSide.SELL, consts.OrderType.LIMITED_ORDER, price, quantity)

    def sell_bitcoins_with_market_order(self, price, quantity):
        return self._place_order(consts.OrderSide.SELL, consts.OrderType.LIMITED_ORDER, price, quantity)

    def cancel_order(self, order_id):
        msg = {
            'MsgType': consts.MessageType.CANCEL_ORDER,
            'ClOrdID': order_id,
        }
        response = self._send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    def get_pending_orders(self, page=0, page_size=50):
        return self._get_orders(orders_filter=['has_leaves_qty eq 1'], page=page, page_size=page_size)

    def get_executed_orders(self, page=0, page_size=50):
        return self._get_orders(orders_filter=['has_cum_qty eq 1'], page=page, page_size=page_size)

    def _place_order(self, order_side, order_type, price, quantity):
        msg = {
            'MsgType': consts.MessageType.PLACE_ORDER,
            'ClOrdID': self._get_unique_id(),
            'Symbol': consts.CURRENCY_TO_SYMBOL_MAP[self.currency],
            'Side': order_side,
            'OrdType': order_type,
            'Price': self._get_satoshi_value(price),
            'OrderQty': self._get_satoshi_value(quantity),
            'BrokerID': self.broker,
        }
        response = self._send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    def _get_orders(self, orders_filter, page, page_size):
        msg = {
            'MsgType': consts.MessageType.GET_ORDERS,
            'OrdersReqID': self._get_unique_id(),
            'Page': page,
            'PageSize': page_size,
            'Filter': orders_filter,

        }
        response = self._send_request(msg)
        self._validate_response(response)
        return self._parse_order_response(response)

    @staticmethod
    def _validate_response(response):
        response_item = response['Responses'][0]
        if response_item.get('OrdStatus') == consts.OrderStatus.REJECTED:
            raise exceptions.OrderRejectedException('Unable to place the order', response_item)

    def _parse_order_response(self, response):
        order_list = self._get_orders_from_response(response)
        balance = self._get_balance_from_response(response)
        return order_list + [balance] if balance else order_list

    def _get_orders_from_response(self, response):
        placed_orders_list = self._get_placed_order_from_response(response)
        order_status_list = self._get_order_status_from_response(response)
        return placed_orders_list + order_status_list

    def _get_placed_order_from_response(self, response):
        order_list = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.PLACE_ORDER_RESPONSE]
        return [self._parse_satoshi_columns(order) for order in order_list]

    def _parse_satoshi_columns(self, order):
        for column in self.SATOSHI_COLUMNS:
            if column in order:
                order[column] = self._get_decimal_value(order[column])
        return order

    def _get_order_status_from_response(self, response):
        responses = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.ORDER_STATUS_RESPONSE]
        multilevel_order_list = [self._make_placed_order_from_order_status_response(item) for item in responses]
        flat_list = [item for sublist in multilevel_order_list for item in sublist]
        return flat_list

    def _make_placed_order_from_order_status_response(self, response):
        keys = response['Columns']
        values_list = response['OrdListGrp']
        partial_zip_func = partial(zip, keys)
        zipped_orders_list = map(partial_zip_func, values_list)
        dict_list = map(dict, zipped_orders_list)
        return map(self._parse_satoshi_columns, dict_list)

    def _get_balance_from_response(self, response):
        balance_list = [r for r in response['Responses'] if r['MsgType'] == consts.MessageType.BALANCE_RESPONSE]
        if not balance_list:
            return None
        balance = balance_list[0]
        broker = balance[str(self.broker)]
        return self._make_balance_from_broker_dict(broker)

    @staticmethod
    def _get_unique_id():
        return int(time.time())

    @staticmethod
    def _get_decimal_value(satoshi):
        if satoshi is None:
            return None
        return float(satoshi) / consts.SATOSHI_PRECISION

    @staticmethod
    def _get_satoshi_value(value):
        if value is None:
            return None
        return int(value * consts.SATOSHI_PRECISION)

    def _send_request(self, msg):
        nonce = self._get_nonce()
        signature = self._get_signature(nonce)

        headers = {
            'user-agent': 'blinktrade_tools/0.1',
            'Content-Type': 'application/json',
            'APIKey': self.key,
            'Nonce': nonce,
            'Signature': signature
        }
        url = '{domain}/tapi/{version}/message'.format(
            domain=self.environment_server, version=self.API_VERSION
        )
        return requests.post(url, json=msg, verify=True, headers=headers).json()

    @staticmethod
    def _get_nonce():
        dt = datetime.utcnow()
        nonce = str(int(
            (time.mktime(dt.utctimetuple()) + dt.microsecond / float(consts.NONCE_PRECISION)) *
            consts.NONCE_PRECISION
        ))
        return str(int(nonce))

    def _get_signature(self, nonce):
        return hmac.new(
            bytearray(self.secret, 'utf-8'), bytearray(nonce, 'utf-8'), digestmod=hashlib.sha256
        ).hexdigest()
