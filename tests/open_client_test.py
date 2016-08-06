from unittest import TestCase

import mock

from blinktrade import clients
from blinktrade import consts


class OpenClientTestCase(TestCase):
    def setUp(self):
        self.client = clients.OpenClient(
            consts.Environment.PRODUCTION, consts.Currency.BRAZILIAN_REAIS, consts.Broker.FOXBIT
        )

    def test_it_creates_an_open_client(self):
        self.assertIsInstance(self.client, clients.OpenClient)
        self.assertEqual(
            self.client.environment_server, consts.ENVIRONMENT_TO_SERVER_MAP[consts.Environment.PRODUCTION]
        )
        self.assertEqual(self.client.currency, consts.Currency.BRAZILIAN_REAIS)
        self.assertEqual(self.client.broker, consts.Broker.FOXBIT)

    @mock.patch(
        'blinktrade.clients.OpenClient._get_market_data',
        return_value={
            'vol': 100.0,
            'pair': 'BTCBRL',
            'low': 2000.00,
            'vol_brl': 25000.00000005,
            'sell': 2200.00,
            'high': 2500.00,
            'buy': 2100.0,
            'last': 2150.0,
        }
    )
    def test_it_gets_ticker(self, _):
        ticker = self.client.get_ticker()
        self.assertIsInstance(ticker, dict)
        self.assertEqual(ticker.get('vol'), 100.0)
        self.assertEqual(ticker.get('pair'), 'BTCBRL')
        self.assertEqual(ticker.get('low'), 2000.0)
        self.assertEqual(ticker.get('vol_brl'), 25000.00000005)
        self.assertEqual(ticker.get('sell'), 2200.0)
        self.assertEqual(ticker.get('high'), 2500.0)
        self.assertEqual(ticker.get('buy'), 2100.0)
        self.assertEqual(ticker.get('last'), 2150.0)

    @mock.patch(
        'blinktrade.clients.OpenClient._get_market_data',
        return_value={
            'bids': [[2100.0, 1.50000005, 1], [2096.07, 12.0, 90824262], [2096.06, 4.8612554, 90803493]],
            'pair': 'BTCBRL',
            'asks': [[2200.0, 2.50000005, 2], [2125.9, 0.708, 90824262], [2125.91, 4.55290567, 90800515]]
        }
    )
    def test_it_gets_order_book(self, _):
        order_book = self.client.get_order_book()
        self.assertIsInstance(order_book, dict)
        self.assertIsInstance(order_book.get('bids'), list)
        self.assertIsInstance(order_book['bids'][0], list)
        self.assertEqual(order_book['bids'][0][0], 2100.0)
        self.assertEqual(order_book['bids'][0][1], 1.50000005)
        self.assertEqual(order_book['bids'][0][2], 1)

        self.assertIsInstance(order_book.get('pair'), str)
        self.assertEqual(order_book.get('pair'), 'BTCBRL')

        self.assertIsInstance(order_book.get('asks'), list)
        self.assertIsInstance(order_book['asks'][0], list)
        self.assertEqual(order_book['asks'][0][0], 2200.0)
        self.assertEqual(order_book['asks'][0][1], 2.50000005)
        self.assertEqual(order_book['asks'][0][2], 2)

    @mock.patch(
        'blinktrade.clients.OpenClient._get_market_data',
        return_value=[
            {'tid': 1, 'date': 1467037014, 'price': 2300.0, 'amount': 1.0, 'side': 'sell'},
            {'tid': 2, 'date': 1467037288, 'price': 2302.5, 'amount': 1.0, 'side': 'buy'},
        ]
    )
    def test_it_gets_trades(self, _):
        trades = self.client.get_trade_list(since_ts=0)
        self.assertIsInstance(trades, list)

        trade = trades[0]
        self.assertIsInstance(trade, dict)
        self.assertEqual(trade.get('tid'), 1)
        self.assertEqual(trade.get('date'), 1467037014)
        self.assertEqual(trade.get('price'), 2300.0)
        self.assertEqual(trade.get('amount'), 1)
        self.assertEqual(trade.get('side'), 'sell')

    def test_it_rejects_invalid_parameters(self):
        self.assertRaises(
            ValueError,
            clients.OpenClient,
            'invalid_env',
            consts.Currency.BRAZILIAN_REAIS,
            consts.Broker.FOXBIT
        )

        self.assertRaises(
            ValueError,
            clients.OpenClient,
            consts.Environment.PRODUCTION,
            'invalid_currency',
            consts.Broker.FOXBIT
        )

        self.assertRaises(
            ValueError,
            clients.OpenClient,
            consts.Environment.PRODUCTION,
            consts.Currency.BRAZILIAN_REAIS,
            'invalid_broker'
        )

    @mock.patch('blinktrade.clients.requests')
    def test_it_gets_market_data(self, mocked_request):
        mocked_request.get = mock.MagicMock()
        client = clients.OpenClient(
            consts.Environment.PRODUCTION, consts.Currency.BRAZILIAN_REAIS, consts.Broker.FOXBIT
        )
        trades_since_param = '?since=0'
        client._get_market_data(consts.MarketInformation.TRADES, trades_since_param)
        self.assertIn(
            consts.ENVIRONMENT_TO_SERVER_MAP[consts.Environment.PRODUCTION], mocked_request.get.call_args[0][0]
        )
        self.assertIn(clients.OpenClient.API_VERSION, mocked_request.get.call_args[0][0])
        self.assertIn(consts.Currency.BRAZILIAN_REAIS, mocked_request.get.call_args[0][0])
        self.assertIn(consts.MarketInformation.TRADES, mocked_request.get.call_args[0][0])
        self.assertIn(trades_since_param, mocked_request.get.call_args[0][0])
