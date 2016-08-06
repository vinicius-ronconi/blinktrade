from unittest import TestCase

import mock
import time
from datetime import datetime
from blinktrade import clients, consts, exceptions


class AuthClientTestCase(TestCase):
    def setUp(self):
        self.client = clients.AuthClient(
            consts.Environment.PRODUCTION, consts.Currency.BRAZILIAN_REAIS, consts.Broker.FOXBIT, 'key', 'secret'
        )

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [{
            u'MsgType': u'U3',
            u'4': {u'BRL': 100000000, u'BRL_locked': 200000000, u'BTC': 300000000, u'BTC_locked': 400000000},
            u'ClientID': 90856083,
            u'BalanceReqID': 1467403164
        }]
    })
    def test_it_get_balance(self, _):
        balance = self.client.get_balance()
        self.assertIsInstance(balance, dict)
        self.assertIn('BTC', balance)
        self.assertIn('BTC_locked', balance)
        self.assertIn('BRL', balance)
        self.assertIn('BRL_locked', balance)
        self.assertEqual(balance.get('BRL'), 1.0)
        self.assertEqual(balance.get('BRL_locked'), 2.0)
        self.assertEqual(balance.get('BTC'), 3.0)
        self.assertEqual(balance.get('BTC_locked'), 4.0)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': 1459144180001,
                u'ExecID': 202294,
                u'ExecType': u'0',
                u'OrdStatus': u'0',
                u'CumQty': 0,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 3130000,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 0,
                u'TimeInForce': u'1',
                u'LeavesQty': 3130000,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'Price': 217500000000,
                u'Side': u'1',
                u'ClOrdID': 1467403664,
                u'AvgPx': 0
            },
            {
                u'MsgType': u'U3',
                u'4': {u'BRL_locked': 5500000000},
                u'ClientID': 90856083
            }
        ]
    })
    def test_it_places_a_limited_buy_order(self, _):
        order_response = self.client.buy_bitcoins_with_limited_order(2000, 5)
        self._assert_buy_orders_responses(order_response)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': 1459144180001,
                u'ExecID': 202294,
                u'ExecType': u'0',
                u'OrdStatus': u'0',
                u'CumQty': 0,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 3130000,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 0,
                u'TimeInForce': u'1',
                u'LeavesQty': 3130000,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'Price': 217500000000,
                u'Side': u'1',
                u'ClOrdID': 1467403664,
                u'AvgPx': 0
            },
            {
                u'MsgType': u'U3',
                u'4': {u'BRL_locked': 5500000000},
                u'ClientID': 90856083
            }
        ]
    })
    def test_it_places_a_market_buy_order(self, _):
        order_response = self.client.buy_bitcoins_with_market_order(2000, 5)
        self._assert_buy_orders_responses(order_response)

    def _assert_buy_orders_responses(self, order_response):
        self.assertIsInstance(order_response, list)

        order_data = order_response[0]
        balance_data = order_response[1]

        self.assertIsInstance(order_data, dict)
        self.assertEqual(order_data.get('OrderQty'), 0.0313)
        self.assertEqual(order_data.get('LeavesQty'), 0.0313)
        self.assertEqual(order_data.get('Price'), 2175.0)
        self.assertIsInstance(balance_data, dict)
        self.assertEqual(balance_data.get('BRL_locked'), 55.0)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': 1459144180001,
                u'ExecID': 202294,
                u'ExecType': u'0',
                u'OrdStatus': u'0',
                u'CumQty': 0,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 3130000,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 0,
                u'TimeInForce': u'1',
                u'LeavesQty': 3130000,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'Price': 217500000000,
                u'Side': u'2',
                u'ClOrdID': 1467403664,
                u'AvgPx': 0
            },
            {
                u'MsgType': u'U3',
                u'4': {u'BTC_locked': 3130000},
                u'ClientID': 90856083
            }
        ]
    })
    def test_it_places_a_limited_sell_order(self, _):
        order_response = self.client.sell_bitcoins_with_limited_order(2000, 5)
        self._assert_sell_orders_responses(order_response)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': 1459144180001,
                u'ExecID': 202294,
                u'ExecType': u'0',
                u'OrdStatus': u'0',
                u'CumQty': 0,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 3130000,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 0,
                u'TimeInForce': u'1',
                u'LeavesQty': 3130000,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'Price': 217500000000,
                u'Side': u'2',
                u'ClOrdID': 1467403664,
                u'AvgPx': 0
            },
            {
                u'MsgType': u'U3',
                u'4': {u'BTC_locked': 3130000},
                u'ClientID': 90856083
            }
        ]
    })
    def test_it_places_a_market_sell_order(self, _):
        order_response = self.client.sell_bitcoins_with_market_order(2000, 5)
        self._assert_sell_orders_responses(order_response)

    def _assert_sell_orders_responses(self, order_response):
        self.assertIsInstance(order_response, list)

        order_data = order_response[0]
        balance_data = order_response[1]

        self.assertIsInstance(order_data, dict)
        self.assertEqual(order_data.get('OrderQty'), 0.0313)
        self.assertEqual(order_data.get('LeavesQty'), 0.0313)
        self.assertEqual(order_data.get('Price'), 2175.0)
        self.assertIsInstance(balance_data, dict)
        self.assertEqual(balance_data.get('BTC_locked'), 0.0313)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': None,
                u'TimeInForce': u'1',
                u'ExecID': None,
                u'ExecType': u'8',
                u'OrdStatus': u'8',
                u'CumQty': 0,
                u'Price': 1000000,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 10,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 0,
                u'Volume': 0,
                u'LeavesQty': 0,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'OrdRejReason': u'3',
                u'Side': u'1',
                u'ClOrdID': 1467406237,
                u'AvgPx': 0
            }
        ]
    })
    def test_it_raises_exception_for_rejected_order(self, _):
        self.assertRaises(
            exceptions.OrderRejectedException,
            self.client.buy_bitcoins_with_limited_order,
            price=0.01,
            quantity=0.00000001,
        )

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrderID': 1459144180001,
                u'ExecID': 202543,
                u'ExecType': u'4',
                u'OrdStatus': u'4',
                u'CumQty': 0,
                u'Symbol': u'BTCBRL',
                u'OrderQty': 3130000,
                u'LastShares': 0,
                u'LastPx': 0,
                u'CxlQty': 3130000,
                u'TimeInForce': u'1',
                u'LeavesQty': 0,
                u'MsgType': u'8',
                u'ExecSide': u'1',
                u'OrdType': u'2',
                u'Price': 217500000000,
                u'Side': u'1',
                u'ClOrdID': u'1467403664',
                u'AvgPx': 0
            },
            {
                u'MsgType': u'U3',
                u'4': {u'BRL_locked': 5000000000},
                u'ClientID': 90856083
            }
        ]
    })
    def test_it_cancels_an_order(self, _):
        order_response = self.client.cancel_order(order_id='1467403664')
        self.assertIsInstance(order_response, list)

        order_data = order_response[0]
        balance_data = order_response[1]

        self.assertIsInstance(order_data, dict)
        self.assertEqual(order_data.get('OrderQty'), 0.0313)
        self.assertEqual(order_data.get('LeavesQty'), 0.0)
        self.assertEqual(order_data.get('Price'), 2175.0)
        self.assertIsInstance(balance_data, dict)
        self.assertEqual(balance_data.get('BRL_locked'), 50.0)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrdListGrp': [
                    [
                        u'2961106',
                        1459144231834,
                        0,
                        u'0',
                        3130000,
                        0,
                        0,
                        u'BTCBRL',
                        u'1',
                        u'2',
                        3130000,
                        217500000000,
                        u'2016-07-06 13:44:53',
                        0,
                        u'1'
                    ]
                ],
                u'PageSize': 20,
                u'OrdersReqID': 1467837196,
                u'MsgType': u'U5',
                u'Page': 0,
                u'Columns': [
                    u'ClOrdID',
                    u'OrderID',
                    u'CumQty',
                    u'OrdStatus',
                    u'LeavesQty',
                    u'CxlQty',
                    u'AvgPx',
                    u'Symbol',
                    u'Side',
                    u'OrdType',
                    u'OrderQty',
                    u'Price',
                    u'OrderDate',
                    u'Volume',
                    u'TimeInForce',
                ]
            }
        ]
    })
    def test_it_get_pending_orders(self, _):
        order_response = self.client.get_pending_orders()
        self.assertIsInstance(order_response, list)

        order_data = order_response[0]

        self.assertIsInstance(order_data, dict)
        self.assertEqual(order_data.get('OrderQty'), 0.0313)
        self.assertEqual(order_data.get('LeavesQty'), 0.0313)
        self.assertEqual(order_data.get('Price'), 2175.0)

    @mock.patch('blinktrade.clients.AuthClient._send_request', return_value={
        u'Status': 200,
        u'Description': u'OK',
        u'Responses': [
            {
                u'OrdListGrp': [
                    [
                        u'2961106',
                        1459144231834,
                        0,
                        u'0',
                        3130000,
                        0,
                        0,
                        u'BTCBRL',
                        u'1',
                        u'2',
                        3130000,
                        217500000000,
                        u'2016-07-06 13:44:53',
                        0,
                        u'1'
                    ]
                ],
                u'PageSize': 20,
                u'OrdersReqID': 1467837196,
                u'MsgType': u'U5',
                u'Page': 0,
                u'Columns': [
                    u'ClOrdID',
                    u'OrderID',
                    u'CumQty',
                    u'OrdStatus',
                    u'LeavesQty',
                    u'CxlQty',
                    u'AvgPx',
                    u'Symbol',
                    u'Side',
                    u'OrdType',
                    u'OrderQty',
                    u'Price',
                    u'OrderDate',
                    u'Volume',
                    u'TimeInForce'
                ]
            }
        ]
    })
    def test_it_get_executed_orders(self, _):
        order_response = self.client.get_executed_orders()
        self.assertIsInstance(order_response, list)

        order_data = order_response[0]

        self.assertIsInstance(order_data, dict)
        self.assertEqual(order_data.get('OrderQty'), 0.0313)
        self.assertEqual(order_data.get('LeavesQty'), 0.0313)
        self.assertEqual(order_data.get('Price'), 2175.0)

    def test_it_converts_satoshi_to_currency(self):
        satoshi = 123456789
        currency = self.client._get_decimal_value(satoshi)
        self.assertIsInstance(currency, float)
        self.assertEqual(currency, float(satoshi) / consts.SATOSHI_PRECISION)

    def test_it_returns_none_for_none_satoshi(self):
        satoshi = None
        currency = self.client._get_decimal_value(satoshi)
        self.assertIsNone(currency)

    def test_it_converts_currency_to_satoshi(self):
        value = 1234
        satoshi = self.client._get_satoshi_value(value)
        self.assertIsInstance(satoshi, int)
        self.assertEqual(satoshi, int(value * consts.SATOSHI_PRECISION))

    def test_it_returns_none_for_none_value(self):
        value = None
        satoshi = self.client._get_satoshi_value(value)
        self.assertIsNone(satoshi)

    def test_it_creates_an_int_unique_id(self):
        value = self.client._get_unique_id()
        self.assertIsInstance(value, int)
        self.assertGreater(value, 0)

    @mock.patch('blinktrade.clients.requests')
    @mock.patch('blinktrade.clients.datetime')
    def test_it_sends_request(self, mocked_datetime, mocked_request):
        dt = datetime(2016, 8, 1, 15, 0, 0)
        mocked_datetime.utcnow.return_value = dt
        nonce = str(int(
                (time.mktime(dt.utctimetuple()) + dt.microsecond / float(consts.NONCE_PRECISION)) *
                consts.NONCE_PRECISION
        ))
        self.assertIsInstance(nonce, str)

        mocked_request.post = mock.MagicMock()
        client = clients.AuthClient(
            consts.Environment.PRODUCTION, consts.Currency.BRAZILIAN_REAIS, consts.Broker.FOXBIT, 'key', 'secret',
        )
        msg = {'msg_key': 'msg_value'}
        client._send_request(msg)
        self.assertIn(
            consts.ENVIRONMENT_TO_SERVER_MAP[consts.Environment.PRODUCTION], mocked_request.post.call_args[0][0]
        )
        self.assertEqual(msg, mocked_request.post.call_args[1]['json'])
        self.assertEqual('key', mocked_request.post.call_args[1]['headers']['APIKey'])
        self.assertEqual(nonce, mocked_request.post.call_args[1]['headers']['Nonce'])
        self.assertIn(
            consts.ENVIRONMENT_TO_SERVER_MAP[consts.Environment.PRODUCTION], mocked_request.post.call_args[0][0]
        )
