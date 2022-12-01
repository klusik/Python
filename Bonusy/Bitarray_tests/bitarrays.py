# DBC
byte_list = [0 for _ in range(64)]
data = 10
lsb = 14

# Another approach
data_shifted = data << (len(byte_list) * 8 - lsb)

print(list(data_shifted.to_bytes(len(byte_list), "little")))



