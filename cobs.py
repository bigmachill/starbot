#!/usr/bin/env python
# From https://www.embeddedrelated.com/showarticle/113.php
# 1  Output a 00, record a pointer to that byte, and initialize a length counter to 1.
# 2  If the raw input packet has no bytes remaining, end.
# 3  If the next byte in the raw input packet is zero, goto step 7.
# 4  The next byte in the raw input packet is nonzero: output that byte without changing it.
# 5  Increment the length counter.
# 6  Goto step 2.
# 7  The raw input packet contained a 00: overwrite the last output 00 with length counter value.
# 8  Goto step 1.

data = [0x07, 0x09, 0x00, 0x01, 0x00, 0x00, 0x02, 0x03, 0x04, 0x05, 0x06, 0x00, 0x18, 0x22]

def encode(data):
  ptr0 = 0
  dlen = 1
  encoded = [0]
  for b in data:
    if b == 0:
      encoded[ptr0] = dlen
      ptr0 = len(encoded)
      dlen = 1
      encoded.append(0)
    else:
      dlen += 1
      encoded.append(b)
  encoded[ptr0] = dlen
  encoded.append(0)
  return encoded

def decode(data):
  dlen = data[0]
  dptr = 0
  decoded = []
  while data[dptr + dlen] != 0:
    decoded.extend(data[dptr + 1:dptr + dlen])
    decoded.append(0)
    dptr += dlen
    dlen = data[dptr]
  decoded.extend(data[dptr + 1:dptr + dlen])
  return decoded

print(data)
encoded = encode(data)
print(encoded)
decoded = decode(encoded)
print(decoded)
