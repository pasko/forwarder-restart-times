
import re
import sys


# example line:
#   'I   98.106s 04ae  [04ae]> LD_LIBRARY_PATH=/data/local/tmp/forwarder/  /data/local/tmp/forwarder/device_forwarder --kill-server; echo %$?'
def Main():
  forwarder_re = re.compile('''
      I \s*
      (?P<timestamp> [0-9.]+)  # timestamp of the log message
      s
      \s
      (?P<thread_id> [0-9a-f]+)
      \s
      .*
      LD_LIBRARY_PATH=/data/local/tmp/forwarder/\s+
      /data/local/tmp/forwarder/device_forwarder
      (?P<has_kill_server> \s --kill-server)?
      .*''', re.VERBOSE)

  # Measure the amount of time spent in starting the forwarder after being
  # killed.
  kill_times = {}
  total_restart_time = 0.0
  for line in sys.stdin:
    match = forwarder_re.match(line)
    if match:
      timestamp = match.group('timestamp')
      thread_id = match.group('thread_id')
      has_kill_server = match.group('has_kill_server')
      if has_kill_server:
        kill_times[thread_id] = float(timestamp)
      else:
        if thread_id in kill_times:
          restart_time = float(timestamp) - kill_times[thread_id]
          total_restart_time += restart_time
          kill_times.pop(thread_id, None)

  print 'Total forwarder restart time: %.3fs' % total_restart_time


if __name__ == '__main__':
  sys.exit(Main())
