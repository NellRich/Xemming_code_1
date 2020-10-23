import random

# длина блока кодирования
CHUNK_LENGTH = 8

# проверка длины блока (Длина блока должна быть кратна 8)
assert not CHUNK_LENGTH % 8

# вычисление контрольных бит
CHECK_BITS = [i for i in range(1, CHUNK_LENGTH + 1) if not i & (i - 1)]

# преобразование символов в бинарный формат
def chars_to_bin(chars):
    print('Преобразование исходных символов в ASCII:', [ord(c) for c in chars])
    assert not len(chars) * 8 % CHUNK_LENGTH, 'Длина кодируемых данных должна быть кратна длине блока кодирования'
    print('Преобразование символов в бинарный формат:')
    print('\n'.join([bin(ord(c))[2:].zfill(8) for c in chars]))
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])

# поблочный вывод бинарных данных
def chunk_iterator(text_bin, chunk_size=CHUNK_LENGTH):
    for i in range(len(text_bin)):
        if not i % chunk_size:
            yield text_bin[i:i + chunk_size]

# получение информации о контрольных битах из бинарного блока данных
def get_check_bits_data(value_bin):
    check_bits_count_map = {k: 0 for k in CHECK_BITS}
    for index, value in enumerate(value_bin, 1):
        if int(value):
            bin_char_list = list(bin(index)[2:].zfill(8))
            bin_char_list.reverse()
            for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
                check_bits_count_map[degree] += 1
    check_bits_value_map = {}
    for check_bit, count in check_bits_count_map.items():
        check_bits_value_map[check_bit] = 0 if not count % 2 else 1
    return check_bits_value_map

# добавить в бинарный блок "пустые" контрольные биты
def set_empty_check_bits(value_bin):
    for bit in CHECK_BITS:
        value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
    return value_bin

# установить значения контрольных бит
def set_check_bits(value_bin):
    value_bin = set_empty_check_bits(value_bin)
    check_bits_data = get_check_bits_data(value_bin)
    for check_bit, bit_value in check_bits_data.items():
        value_bin = '{0}{1}{2}'.format(
            value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
    return value_bin

# получить информацию о контрольных битах из блока бинарных данных
def get_check_bits(value_bin):
    check_bits = {}
    for index, value in enumerate(value_bin, 1):
        if index in CHECK_BITS:
            check_bits[index] = int(value)
    return check_bits

# исключить информацию о контрольных битах из блока бинарных данных
def exclude_check_bits(value_bin):
    clean_value_bin = ''
    for index, char_bin in enumerate(list(value_bin), 1):
        if index not in CHECK_BITS:
            clean_value_bin += char_bin

    return clean_value_bin

# допустить ошибку в блоках бинарных данных
def set_errors(encoded):
    result = ''
    for chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
        num_bit = random.randint(1, len(chunk))
        chunk = '{0}{1}{2}'.format(chunk[:num_bit - 1], int(chunk[num_bit - 1]) ^ 1, chunk[num_bit:])
        result += (chunk)
    return result

# проверка и исправление ошибки в блоке бинарных данных
def check_and_fix_error(encoded_chunk):
    check_bits_encoded = get_check_bits(encoded_chunk)
    check_item = exclude_check_bits(encoded_chunk)
    check_item = set_check_bits(check_item)
    check_bits = get_check_bits(check_item)
    if check_bits_encoded != check_bits:
        invalid_bits = []
        for check_bit_encoded, value in check_bits_encoded.items():
            if check_bits[check_bit_encoded] != value:
                invalid_bits.append(check_bit_encoded)
        num_bit = sum(invalid_bits)
        encoded_chunk = '{0}{1}{2}'.format(
            encoded_chunk[:num_bit - 1],
            int(encoded_chunk[num_bit - 1]) ^ 1,
            encoded_chunk[num_bit:])
    return encoded_chunk

# получить список индексов различающихся битов
def get_diff_index_list(value_bin1, value_bin2):
    diff_index_list = []
    for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
        if char_bin_items[0] != char_bin_items[1]:
            diff_index_list.append(index)
    return diff_index_list

# кодирование данных
def encode(source):
    text_bin = chars_to_bin(source)
    result = ''
    for chunk_bin in chunk_iterator(text_bin):
        chunk_bin = set_check_bits(chunk_bin)
        result += chunk_bin
    return result

# декодирование данных
def decode(encoded, fix_errors=True):
    decoded_value = ''
    fixed_encoded_list = []
    for encoded_chunk in chunk_iterator(encoded, CHUNK_LENGTH + len(CHECK_BITS)):
        if fix_errors:
            encoded_chunk = check_and_fix_error(encoded_chunk)
        fixed_encoded_list.append(encoded_chunk)

    clean_chunk_list = []
    for encoded_chunk in fixed_encoded_list:
        encoded_chunk = exclude_check_bits(encoded_chunk)
        clean_chunk_list.append(encoded_chunk)

    for clean_chunk in clean_chunk_list:
        for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
            decoded_value += chr(int(clean_char, 2))
    return decoded_value


if __name__ == '__main__':
    print('------Помехоустойчивое кодирование - Код Хемминга-----')
    source = input('Введите исходное слово:\n')
    print('Контрольные биты: {0}'.format(CHECK_BITS))
    encoded = encode(source)
    print('Закодированные данные:{0}'.format(encoded))
    decoded = decode(encoded)
    print('Результат декодирования: {0}\n'.format(decoded))
    encoded_with_error = set_errors(encoded)
    print('-----Кодирование с ошибкой-----')
    print('Допускаем ошибки в закодированных данных(50% на 50%): {0}'.format(encoded_with_error))
    diff_index_list = get_diff_index_list(encoded, encoded_with_error)
    print('Допущены ошибки в битах: {0}'.format(diff_index_list))
    decoded = decode(encoded_with_error, fix_errors=False)
    print('Результат декодирования ошибочных данных без исправления ошибок: {0}'.format(decoded))
    decoded = decode(encoded_with_error)
    print('Результат декодирования ошибочных данных с исправлением ошибок: {0}'.format(decoded))