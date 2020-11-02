TICK_PATTERNS = {
        'tick_mean' : '''
var info float
var warn float
var crit float
stream
    |from()
        .measurement('{}')
        .groupBy('host')

    |window()
        .period(1m)
        .every(1m)
    |mean('usage_idle')
    |eval(lambda: 100.0 - "mean")
        .as('used')
        .keep()
    |alert()
        .id('{{ index .Tags {}}}/{}_used')

        .id('{{ index .Tags "host"}}/{}_used')
        .message('{{ .ID }}:{{ index .Fields "used" }}')
        .info(lambda: "used" > info)
        .warn(lambda: "used" > warn)
        .crit(lambda: "used" > crit)
        .post('http://alert_system:42000/alert')
''',

'tick_deriv' : '''
var info float
var warn float
var crit float
stream
    |from()
        .measurement({})
        .groupBy({})
    |derivative('io_time')
        .unit(1s)
        .nonNegative()
        .as('diff')
    |influxDBOut
        .database('calculated')
        .create()
    |alert
        .id('{{ index .Tags {}}}/{}_used')
        .message('{{ .ID }}:{{ index .Fields "diff" }}')
        .info(lambda: "used" > info)
        .warn(lambda: "used" > warn)
        .crit(lambda: "used" > crit)
        .post('http://server:5000/alert')
''',
'tick_sum': '''
var info float
var warn float
var crit float
stream
    |from()
        .measurement({})
        .groupBy({})
    |window()
        .period(10s)
        .every(10s)
    |sum('usage_idle')
        .as('sum')
    |alert
        .id('{{ index .Tags {}}}/{}_used')
        .message('{{ .ID }}:{{ index .Fields "sum" }}')
        .info(lambda: "used" > info)
        .warn(lambda: "used" > warn)
        .crit(lambda: "used" > crit)
        .post('http://server:5000/alert')
''',
}

URL = 'http://localhost:8086'

TYPES = {'mean': TICK_PATTERNS['tick_mean'],
         'derivative': TICK_PATTERNS['tick_deriv'],
         'maximum': TICK_PATTERNS['tick_sum']}
kapacitor_urls = ['http://kapacitor:8087']
alert_system_url = 'http://alert_system:9091'

SIZE = 10
