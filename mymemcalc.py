#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

global_buffers = {
                  'key_buffer_size'                 : '8M',
                  'innodb_additional_mem_pool_size' : '8M',
                  'innodb_buffer_pool_size'         : '128M',
                  'innodb_log_buffer_size'          : '8M',
                  'max_heap_table_size'             : '16M',
                  'query_cache_size'                : '0',
                  } 

# not included: myisam_sort_buffer_size
thread_buffers = {
                  'binlog_cache_size'       : '32K',
                  'join_buffer_size'        : '128K',
                  'max_allowed_packet'      : '1M',
                  'read_buffer_size'        : '128K',
                  'read_rnd_buffer_size'    : '256K',
                  'sort_buffer_size'        : '2M',
                  'thread_stack'            : '256K',
                  }

slave_buffers = {}

cardinal_vars = {
              'max_connections' : '20',
             }

K = 1024.0
M = 1024.0 ** 2
G = 1024.0 ** 3
T = 1024.0 ** 4
P = 1024.0 ** 5

def _read_from_cnf(mycnf):
    # change values from default to my.cnf
    with open(mycnf) as cnf:
        parser = configparser.SafeConfigParser(allow_no_value=True)
        parser.readfp(cnf)
        if not parser.has_section('mysqld'):
            sys.exit('mysqld section does not exit. invalid my.cnf.')

        for k in global_buffers.keys():
             if parser.has_option('mysqld', k):
                  global_buffers[k] = parser.get('mysqld', k)
             elif parser.has_option('mysqld', k.rstrip('_size')):
                  global_buffers[k] = parser.get('mysqld', k.rstrip('_size'))

        for k in thread_buffers.keys():
             if parser.has_option('mysqld', k):
                  thread_buffers[k] = parser.get('mysqld', k)
             elif parser.has_option('mysqld', k.rstrip('_size')):
                  thread_buffers[k] = parser.get('mysqld', k.rstrip('_size'))
                 
        for k in slave_buffers.keys():
             if parser.has_option('mysqld', k):
                  slave_buffers[k] = parser.get('mysqld', k)
             elif parser.has_option('mysqld', k.rstrip('_size')):
                  slave_buffers[k] = parser.get('mysqld', k.rstrip('_size'))
                 
        for k in cardinal_vars.keys():
             if parser.has_option('mysqld', k):
                  cardinal_vars[k] = parser.get('mysqld', k)
                 
def _read_from_vars():
    # change values from default to stdin(show variables)
    for line in sys.stdin:
        var = line.split()
        if var[0] in global_buffers:
            global_buffers[var[0]] = var[1]
        elif var[0] in thread_buffers:
            thread_buffers[var[0]] = var[1]
        elif var[0] in slave_buffers:
            slave_buffers[var[0]] = var[1]
        elif var[0] in cardinal_vars:
            cardinal_vars[var[0]] = var[1]

def _show_global_buffers():
    for k,v in sorted(global_buffers.items(), key=lambda x: x[0]): 
        if v.endswith(('K', 'M', 'G', 'T')):
            print('  ' + k + ' = ' + v + '(' + str(_SI_to_int(v)) + ')')
        else:
            print('  ' + k + ' = ' + _digit_to_SI(v) + '(' + v + ')')
    print('')

def _show_thread_buffers():
    for k,v in sorted(thread_buffers.items(), key=lambda x: x[0]):
        if v.endswith(('K', 'M', 'G', 'T')):
            print('  ' + k + ' = ' + v + '(' + str(_SI_to_int(v)) + ')')
        else:
            print('  ' + k + ' = ' + _digit_to_SI(v) + '(' + v + ')')
    print('')

def _show_slave_buffers():
    for k,v in slave_buffers.items():
        if v.endswith(('K', 'M', 'G', 'T')):
            print('  ' + k + ' = ' + v + '(' + str(_SI_to_int(v)) + ')')
        else:
            print('  ' + k + ' = ' + _digit_to_SI(v) + '(' + v + ')')
    print('')

def _show_cardinal_vars():
    print('[cardinal_variables]')
    for k,v in cardinal_vars.items():
        print('  ' + k + ' = ' + v)
    print('')

def _SI_to_int(val):
    if val.endswith('K'):
        return int(val.rstrip('K')) * int(K)
    elif val.endswith('M'):
        return int(val.rstrip('M')) * int(M)
    elif val.endswith('G'):
        return int(val.rstrip('G')) * int(G)
    elif val.endswith('T'):
        return int(val.rstrip('T')) * int(T)
    else:
        return int(val)

def _digit_to_SI(val):
    if val.endswith(('K', 'M', 'G', 'T')):
        return val

    d = int(val)

    if d < 0:
        return '0'
    if d < K:
        return val
    if d < M:
        return str(round(d / K, 1)) + 'K'
    if d < G:
        return str(round(d / M, 1)) + 'M'
    if d < T:
        return str(round(d / G, 1)) + 'G'
    if d < P:
        return str(round(d / T, 1)) + 'T'

def _show_calc():
    global_total = 0
    thread_total = 0

    for v in global_buffers.values():
        global_total += _SI_to_int(v)

    for v in thread_buffers.values():
        thread_total += _SI_to_int(v)

    total = global_total + (thread_total * int(cardinal_vars['max_connections']))

    slave_total = 0
    if options.version == '5.6':
        for v in slave_buffers.values():
            slave_total += _SI_to_int(v)
        total += slave_total * int(cardinal_vars['slave_parallel_workers'])
   
    print('[required_memory] = ' + _digit_to_SI(str(total)) + '(' + str(total) + ')')
    print('')
    print('[global_total] = ' + str(global_total))
    _show_global_buffers()
    print('[thread_total] = ' + str(thread_total))
    _show_thread_buffers()
    if options.version == '5.6':
        print('[slave_total] = ' + str(slave_total))
        _show_slave_buffers()
    _show_cardinal_vars()


if __name__ == '__main__':
    usage = "usage: %prog [options] my_cnf_file\n"
    usage += "     : mysql -e 'show variables' | %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-v", dest="version", help="Mysql version. support 5.5 or 5.6. default=5.5(=5.1).")
    options, args = parser.parse_args()

    if options.version == '5.6':
        del global_buffers['innodb_additional_mem_pool_size']
        global_buffers['query_cache_size'] = '1M'
        cardinal_vars['slave_parallel_workers'] = '0'
        slave_buffers['slave_pending_jobs_size_max'] = '16M'

    if len(args) > 1:
        parser.print_help()

    try:
        if len(args) == 1:
            _read_from_cnf(args[0])
        else:
            _read_from_vars()
    except Exception as e:
        sys.exit(e)

    print('*** minimum memory requirement fomula ***')
    if options.version == '5.6':
        print('[required_memory] = [global_total] + ([thread_total] * max_connections) + ([slave_total] * slave_parallel_workers)')
    else:
        print('[required_memory] = [global_total] + ([thread_total] * max_connections)')
    print('')

    print('*** result ***')
    try:
        _show_calc()
    except (ValueError, TypeError) as e:
        print('value is invalid.')
        sys.exit(e)

