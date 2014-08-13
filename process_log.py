
import re
import sys


def Main():
  # Example line:
  #   'I   98.106s 04ae  [04ae]> LD_LIBRARY_PATH=/data/local/tmp/forwarder/  /data/local/tmp/forwarder/device_forwarder --kill-server; echo %$?'
  kill_initiated_re = re.compile('''
      I \s*
      (?P<timestamp> [0-9.]+)  # timestamp of the log message
      s
      \s
      (?P<thread_id> [0-9a-f]+)
      \s
      .*
      LD_LIBRARY_PATH=/data/local/tmp/forwarder/\s+
      /data/local/tmp/forwarder/device_forwarder
      \s
      --kill-server
      .*''', re.VERBOSE)

  # Example line:
  #   'I    9.385s b8bb  Forwarding device port: 8000 to host port: 8005.'
  forwarder_restarted_re = re.compile('''
      I \s*
      (?P<timestamp> [0-9.]+)  # timestamp of the log message
      s
      \s
      (?P<thread_id> [0-9a-f]+)
      \s+
      Forwarding\sdevice\sport:\s
      ([0-9]+)
      \s
      to\shost\sport:\s
      ([0-9]+)
      .*''', re.VERBOSE)

  # Measure the amount of time spent in starting the forwarder after being
  # killed.
  kill_times = {}
  total_restart_time = 0.0
  for line in sys.stdin:
    kill_match = kill_initiated_re.match(line)
    if kill_match:
      timestamp = kill_match.group('timestamp')
      thread_id = kill_match.group('thread_id')
      kill_times[thread_id] = float(timestamp)
    started_match = forwarder_restarted_re.match(line)
    if started_match:
      timestamp = started_match.group('timestamp')
      thread_id = started_match.group('thread_id')
      if thread_id in kill_times:
        restart_time = float(timestamp) - kill_times[thread_id]
        total_restart_time += restart_time
        kill_times.pop(thread_id, None)

  print 'Total forwarder restart time: %.3fs' % total_restart_time


if __name__ == '__main__':
  sys.exit(Main())
