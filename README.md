mymemcalc.py
===========
calculate minimum required memory for mysql from my.cnf

(tested on python2.7)

usage
------
    $ python mymemcalc.py path_to_mycnf
or

    $ mysql -e 'show variables' | python mymemcalc.py

example
------

    $ mysql -e 'show variables' | python mymemcalc.py
    [required_memory] = [global_buffers] + ([thread_buffers] * [max_connections])
    
    *** result ***
    [required_memory] = 1.7G(1784676352)
    
    [global_total] = 1044381696
      query_cache_size = 64.0M(67108864)
      innodb_buffer_pool_size = 512.0M(536870912)
      innodb_additional_mem_pool_size = 20.0M(20971520)
      innodb_log_buffer_size = 16.0M(16777216)
      max_heap_table_size = 128.0M(134217728)
      key_buffer_size = 256.0M(268435456)

    [thread_total] = 11567104
      binlog_cache_size = 32.0K(32768)
      sort_buffer_size = 256.0K(262144)
      max_allowed_packet = 8.0M(8388608)
      thread_stack = 256.0K(262144)
      read_rnd_buffer_size = 2.0M(2097152)
      read_buffer_size = 256.0K(262144)
      join_buffer_size = 256.0K(262144)
    
    [max_connections] = 64
    
