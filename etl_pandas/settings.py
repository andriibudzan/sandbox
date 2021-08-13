CONFIG_TABLES = {
    "brand": ['brand'],
    "model": ['model'],
    "fuel": ['fuel'],
    "kind": ['kind'],
    "bodytype": ['body'],
    "purpose": ['purpose'],
    "license_plates": ['license_plates'],
    "owners": ['person'],
    "employee": ['employee', 'dep'],
    "dep": ['dep', 'reg_addr_koatuu'],
    "engine": ['capacity', 'fuel'],
    "operations": ['oper_code', 'oper_name', 'dep', 'reg_addr_koatuu'],
    "cars_for_registration": [
        'brand', 'model', 'capacity', 'fuel', 'kind', 'body', 'purpose',
        'own_weight', 'total_weight', 'vin', 'make_year', 'color'
    ],
    "vehicle": [
        'brand', 'model', 'capacity', 'fuel', 'kind',
        'body', 'purpose', 'own_weight', 'total_weight'
    ],
    "registration_activities": [
        'oper_code', 'oper_name', 'dep', 'reg_addr_koatuu', 'brand',
        'model', 'capacity', 'fuel', 'kind', 'body', 'purpose',
        'own_weight', 'total_weight', 'vin', 'make_year',
        'color', 'person', 'license_plates'
    ]
}

MAPPER_DTYPES = {
    'person': 'category',
    'fuel': 'category',
    'kind': 'category',
    'purpose': 'category',
    'reg_addr_koatuu': 'Int64',
    'oper_code': 'Int64',
    'employee': 'Int64',
    'make_year': 'Int64',
    'capacity': 'Int64',
    # 'own_weight': 'Int64',
    # 'total_weight': 'Int64'
}

MAPPER_COLUMNS = {
    'dep_code': 'employee',
    'n_reg_new': 'license_plates'
}

MAPPER_TABLES = {
    'registration_activities': [
        'cars_for_registration',
        'operations',
        'owners',
        'license_plates'
    ],
    'vehicle': [
        'brand',
        'model',
        'engine',
        'kind',
        'bodytype',
        'purpose'
    ],
    'operations': [
        'dep'
    ],
    'employee': [
        'dep'
    ],
    'dep': [
        'employee'
    ],
    'engine': [
        'fuel'
    ],
    'cars_for_registration': [
        'vehicle'
    ]
}
