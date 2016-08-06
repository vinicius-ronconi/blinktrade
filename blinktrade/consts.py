NONCE_PRECISION = 1000000  # 6 zeros
SATOSHI_PRECISION = 100000000  # 8 zeros


class Environment:
    PRODUCTION = 'PROD'
    TEST = 'TEST'

ENVIRONMENTS_CHOICES = {
    Environment.PRODUCTION: 'Production',
    Environment.TEST: 'Test',
}

ENVIRONMENT_TO_SERVER_MAP = {
    Environment.PRODUCTION: 'https://blinktrade.blinktrade.com',
    Environment.TEST: 'https://blinktrade.testnet.blinktrade.com',
}


class Currency:
    AMERICAN_DOLLAR = 'USD'
    BRAZILIAN_REAIS = 'BRL'
    CHILEAN_PESOS = 'CLP'
    PAKISTANI_RUPEE = 'PKR'
    VENEZUELAN_BOLIVARES = 'VEF'
    VIETNAMESE_DONGS = 'VND'

CURRENCIES_CHOICES = {
    Currency.BRAZILIAN_REAIS: 'Brazilian Reais',
    Currency.CHILEAN_PESOS: 'Chilean Pesos',
    Currency.PAKISTANI_RUPEE: 'Pakistani Rupee',
    Currency.VENEZUELAN_BOLIVARES: 'Venezuelan Bolivares',
    Currency.VIETNAMESE_DONGS: 'Vietnamese Dongs',
}


class Broker:
    SURBITCOIN = '1'
    VBTC = '3'
    FOXBIT = '4'
    TESTNET = '5'
    URDUBIT = '8'
    CHILEBIT = '9'

BROKERS_CHOICES = {
    Broker.SURBITCOIN: 'Sur Bitcoin',
    Broker.VBTC: 'VBTC',
    Broker.FOXBIT: 'Foxbit',
    Broker.TESTNET: 'Testnet',
    Broker.URDUBIT: 'Urbubit',
    Broker.CHILEBIT: 'Chilebit.net',
}


class MarketInformation:
    TICKER = 'ticker'
    ORDER_BOOK = 'orderbook'
    TRADES = 'trades'


class MessageType:
    BALANCE = 'U2'
    BALANCE_RESPONSE = 'U3'
    CANCEL_ORDER = 'F'
    GET_ORDERS = 'U4'
    POSITION = 'U42'
    PLACE_ORDER = 'D'
    PLACE_ORDER_RESPONSE = '8'
    ORDER_STATUS_RESPONSE = 'U5'
    TRADE_HISTORY = 'U32'
    TRADERS_RANK = 'U36'


class OrderSide:
    BUY = '1'
    SELL = '2'


class OrderStatus:
    NEW = '0'
    PARTIALLY_FILL = '1'
    FILL = '2'
    CANCELLED = '4'
    REJECTED = '8'
    PENDING_NEW = 'A'


class OrderType:
    MARKET = '1'
    LIMITED_ORDER = '2'


class Symbol:
    BTCUSD = 'BTCUSD'
    BTCBRL = 'BTCBRL'
    BTCCLP = 'BTCCLP'
    BTCPKR = 'BTCPKR'
    BTCVEF = 'BTCVEF'
    BTCVND = 'BTCVND'

CURRENCY_TO_SYMBOL_MAP = {
    Currency.AMERICAN_DOLLAR: Symbol.BTCUSD,
    Currency.BRAZILIAN_REAIS: Symbol.BTCBRL,
    Currency.CHILEAN_PESOS: Symbol.BTCCLP,
    Currency.PAKISTANI_RUPEE: Symbol.BTCPKR,
    Currency.VENEZUELAN_BOLIVARES: Symbol.BTCVEF,
    Currency.VIETNAMESE_DONGS: Symbol.BTCVND,
}
