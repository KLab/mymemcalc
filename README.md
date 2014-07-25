mymemcalc.py
===========
calculate minimum required memory for mysql from my.cnf

(tested on python2.7)

usage
------
    $ python mymemcalc.py path_to_mycnf
or

    $ mysql -e 'show variables' | python mymemcalc.py -v 5.6

example
------

    $ mysql -e 'show variables' | python mymemcalc.py -v 5.6

    *** minimum memory requirement fomula ***
    [required_memory] = [global_total] + ([thread_total] * max_connections) + ([slave_total] * slave_parallel_workers)
    
    *** result ***
    [required_memory] = 622.4M(652607488)
    
    [global_total] = 192937984
      query_cache_size = 16M(16777216)
      innodb_buffer_pool_size = 128M(134217728)
      innodb_log_buffer_size = 8M(8388608)
      max_heap_table_size = 16M(16777216)
      key_buffer_size = 16M(16777216)
    
    [thread_total] = 19628032
      binlog_cache_size = 32K(32768)
      sort_buffer_size = 2M(2097152)
      max_allowed_packet = 16M(16777216)
      thread_stack = 192K(196608)
      read_rnd_buffer_size = 256K(262144)
      read_buffer_size = 128K(131072)
      join_buffer_size = 128K(131072)
    
    [slave_total] = 33554432
      slave_pending_jobs_size_max = 32M(33554432)
    
    [cardinal_variables]
      slave_parallel_workers = 2
      max_connections = 20

