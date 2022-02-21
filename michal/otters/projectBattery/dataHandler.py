# this script is supposed to read data from LORA and write them to DB

# imported modules


# test input
LoraInputMessage = [
  {
    "content": "Hello, world!",
    "device_id": "ystremtest",
    "raw": "SGVsbG8sIHdvcmxkIQ==",
    "time": "2021-04-22T15:54:38.615313012Z"
  },
  {
    "content": "Hello, world!",
    "device_id": "ystremtest",
    "raw": "SGVsbG8sIHdvcmxkIQ==",
    "time": "2021-04-22T15:56:51.082528215Z"
  },
  {
    "content": "Kokote",
    "device_id": "ystremtest",
    "raw": "S29rb3Rl",
    "time": "2021-04-22T15:57:27.001104216Z"
  }
]

def handler(sOperation, lMessage):
    ''' ... Function for handling LORA messages ... 
        parameters:
        operation - enter string 'read' or string 'write'
            read - reads data from LORA
            write - write parsed data to DB
    
    '''
