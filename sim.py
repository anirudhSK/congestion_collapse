from numpy.random import poisson
import sys

if (len(sys.argv) < 4):
  print("Usage: python3 ", sys.argv[0], " load num_sources buffer_size ")
  sys.exit(1)
else:
  load             = float(sys.argv[1])
  assert(load < 1)
  num_sources      = int(sys.argv[2])
  buffer_size      = int(sys.argv[3])
  ticks            = 100000
  input_rates      = [load] * num_sources # initialize to user-specified load
  queue_size       = 0

# Simulate tick by tick
for t in range(0, ticks):
  # Arrival process for each source
  for j in range(0, num_sources):
    packet_arrivals = poisson(input_rates[j]) # Poisson arrivals
    assert(queue_size <= buffer_size)
    if queue_size + packet_arrivals <= buffer_size: # space in buffer
      queue_size += packet_arrivals
      assert(queue_size <= buffer_size)
      input_rates[j] = min(input_rates[j] + 0.02, load) # additive increase
    else:
      queue_size = buffer_size
      input_rates[j] = input_rates[j] / 2.0 # multiplicative decrease

  # Deterministic departure process
  queue_size = max(0, queue_size - num_sources)
print("Input rate at the end is ", sum(input_rates)/num_sources)
