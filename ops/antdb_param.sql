-- mgr:
export mgrdata=""
cat  >> ${mgrdata}/postgresql.conf << EOF
port = 18610
listen_addresses = '*'
log_directory = 'pg_log'
log_destination ='csvlog'
logging_collector = on
log_min_messages = error
max_wal_senders = 3
hot_standby = on
wal_level = hot_standby
EOF

cat  >> ${mgrdata}/pg_hba.conf << EOF
host    replication     shboss        10.0.0.0/8                 trust
host    all             all          10.0.0.0/8               trust
EOF

--coord:
--Modify according to actual situation
SET COORDINATOR ALL (shared_buffers = '4GB' );
SET COORDINATOR ALL (maintenance_work_mem = '1024MB');
SET COORDINATOR ALL (work_mem = '128MB' );
SET COORDINATOR ALL (max_connections = 1000 );
SET COORDINATOR ALL (max_prepared_transactions = 1000 );
SET COORDINATOR ALL (max_parallel_workers = 10 );
SET COORDINATOR ALL (max_parallel_workers_per_gather = 10 );
----
SET COORDINATOR ALL (log_truncate_on_rotation = on);
SET COORDINATOR ALL (log_rotation_age = '7d');
SET COORDINATOR ALL (log_rotation_size = '100MB');
SET COORDINATOR ALL (log_min_messages = error );
SET COORDINATOR ALL (log_min_duration_statement = 50 );
SET COORDINATOR ALL (log_connections = on );
SET COORDINATOR ALL (log_disconnections = on);
SET COORDINATOR ALL (log_duration = off);
SET COORDINATOR ALL (log_statement = 'ddl' );
SET COORDINATOR ALL (log_checkpoints = on );
SET COORDINATOR ALL (adb_log_query = on );
SET COORDINATOR ALL (unix_socket_permissions = '0700');
SET COORDINATOR ALL (listen_addresses = '*' );
SET COORDINATOR ALL (superuser_reserved_connections = 13);
SET COORDINATOR ALL (tcp_keepalives_idle = 180);
SET COORDINATOR ALL (tcp_keepalives_interval = 10 );
SET COORDINATOR ALL (tcp_keepalives_count = 3 );
SET COORDINATOR ALL (track_counts = on);
SET COORDINATOR ALL (track_activity_query_size = 2048 );
SET COORDINATOR ALL (max_locks_per_transaction = 128);
SET COORDINATOR ALL (constraint_exclusion = on);
SET COORDINATOR ALL (wal_level='replica');
SET COORDINATOR ALL (max_wal_senders = 3);
SET COORDINATOR ALL (hot_standby = on);
SET COORDINATOR ALL (autovacuum_max_workers = 5 );
SET COORDINATOR ALL (autovacuum_naptime = '60min');
SET COORDINATOR ALL (autovacuum_vacuum_threshold = 500);
SET COORDINATOR ALL (autovacuum_analyze_threshold = 500 );
SET COORDINATOR ALL (autovacuum_vacuum_scale_factor = 0.5 );
SET COORDINATOR ALL (autovacuum_vacuum_cost_limit = -1);
SET COORDINATOR ALL (autovacuum_vacuum_cost_delay = '30ms');
SET COORDINATOR ALL (lock_timeout = '180s');
SET COORDINATOR ALL (fsync = off);
SET COORDINATOR ALL (synchronous_commit = off );
SET COORDINATOR ALL (wal_sync_method = open_datasync);
SET COORDINATOR ALL (full_page_writes = off );
SET COORDINATOR ALL (commit_delay = 10);
SET COORDINATOR ALL (commit_siblings = 10 );
--SET COORDINATOR ALL (checkpoint_segments = 256); #only for 2.x version
SET COORDINATOR ALL (checkpoint_timeout = '15min'); 
SET COORDINATOR ALL (checkpoint_completion_target=0.9 );
SET COORDINATOR ALL (max_wal_size = 10240);
SET COORDINATOR ALL (archive_mode = on);
SET COORDINATOR ALL (archive_command = '/bin/date');
--SET COORDINATOR ALL (max_stack_depth = '8MB');
SET COORDINATOR ALL (bgwriter_delay = '10ms');
SET COORDINATOR ALL (bgwriter_lru_maxpages = 1000 );
SET COORDINATOR ALL (bgwriter_lru_multiplier = 10.0 );
SET COORDINATOR ALL (pool_time_out = 300);
SET COORDINATOR ALL (enable_pushdown_art = on );

--datanode:
--Modify according to actual situation
SET DATANODE ALL (shared_buffers = '10GB' );
SET DATANODE ALL (maintenance_work_mem = '1024MB');
SET DATANODE ALL (work_mem = '128MB' );
SET DATANODE ALL (max_connections = 3000 );
SET DATANODE ALL (max_prepared_transactions = 3000 );
SET DATANODE ALL (wal_keep_segments = 128 );
SET DATANODE ALL (effective_cache_size = '15GB' );
SET DATANODE ALL (max_parallel_workers = 10 );
SET DATANODE ALL (max_parallel_workers_per_gather = 10 );
----
SET DATANODE ALL (log_truncate_on_rotation = on);
SET DATANODE ALL (log_rotation_age = '7d' );
SET DATANODE ALL (log_rotation_size = '100MB' );
SET DATANODE ALL (log_min_messages = error);
SET DATANODE ALL (log_min_error_statement = error );
SET DATANODE ALL (log_duration = off);
SET DATANODE ALL (log_statement = 'ddl' );
SET DATANODE ALL (unix_socket_permissions = '0700' );
SET DATANODE ALL (listen_addresses = '*');
SET DATANODE ALL (superuser_reserved_connections = 13 );
SET DATANODE ALL (track_counts = on );
SET DATANODE ALL (track_activity_query_size = 2048);
SET DATANODE ALL (max_locks_per_transaction = 64);
SET DATANODE ALL (constraint_exclusion = on );
set DATANODE ALL (wal_level='replica');
SET DATANODE ALL (max_wal_senders = 5 );
set DATANODE all (wal_log_hints = on);
SET DATANODE ALL (autovacuum = on );
SET DATANODE ALL (autovacuum_max_workers = 5);
SET DATANODE ALL (autovacuum_naptime = '60min' );
SET DATANODE ALL (autovacuum_vacuum_threshold = 500 );
SET DATANODE ALL (autovacuum_analyze_threshold = 500);
SET DATANODE ALL (autovacuum_vacuum_scale_factor = 0.5);
SET DATANODE ALL (autovacuum_vacuum_cost_limit = -1 );
SET DATANODE ALL (autovacuum_vacuum_cost_delay = '30ms' );
SET DATANODE ALL (statement_timeout = 0 );
SET DATANODE ALL (lock_timeout = '180s' );
SET DATANODE ALL (fsync = off);
SET DATANODE ALL (synchronous_commit = off);
SET DATANODE ALL (wal_sync_method = open_datasync );
SET DATANODE ALL (full_page_writes = off);
SET DATANODE ALL (wal_writer_delay = '200ms');
SET DATANODE ALL (commit_delay = 10 );
SET DATANODE ALL (commit_siblings = 10);
SET DATANODE ALL (checkpoint_timeout = '15min' );
SET DATANODE ALL (checkpoint_completion_target = 0.9);
SET DATANODE ALL (max_wal_size = 10240);
SET DATANODE ALL (archive_mode = on );
SET DATANODE ALL (archive_command = '/bin/date' );
--SET DATANODE ALL (max_stack_depth = '8MB' );
SET DATANODE ALL (max_prepared_transactions = 4800);
SET DATANODE ALL (bgwriter_delay = '10ms' );
SET DATANODE ALL (bgwriter_lru_maxpages = 1000);
SET DATANODE ALL (bgwriter_lru_multiplier = 10.0);


--gtm:
SET GTM ALL (shared_buffers = '2GB' );
SET GTM ALL(max_connections = 3000);
SET GTM ALL(max_prepared_transactions = 3000);
SET GTM ALL (fsync = off);
set GTM ALL (wal_level='replica');
SET GTM ALL (max_wal_senders = 5 );
