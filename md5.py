import math

T = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
s = [10, 15, 21, 27] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def chunkify(message):
    chunks = []
    padding_length = (56 - (len(message) + 1) % 64) % 64
    padded_message = message + b'\x80' + b'\x00' * padding_length + (8 * len(message)).to_bytes(8, 'little')
    
    for i in range(0, len(padded_message), 64):
        chunks.append(padded_message[i:i+64])
    
    return chunks

def md5(message):
    a, b, c, d = 0xAAAAAAAA, 0xBBAAEECD, 0xC7456452, 0xD453E2FA
    chunks = chunkify(message)
    
    for chunk in chunks:
        words = [int.from_bytes(chunk[i:i+4], 'little') for i in range(0, 64, 4)]
        
        aa, bb, cc, dd = a, b, c, d # Buffer

        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16
            
            f = (f + a + T[i] + words[g]) & 0xFFFFFFFF
            a, d, c, b = b, c, d, (b + left_rotate(f, s[i])) & 0xFFFFFFFF
        
        a = (a + aa) & 0xFFFFFFFF
        b = (b + bb) & 0xFFFFFFFF
        c = (c + cc) & 0xFFFFFFFF
        d = (d + dd) & 0xFFFFFFFF
    
    digest = (a.to_bytes(4, 'little') +
              b.to_bytes(4, 'little') +
              c.to_bytes(4, 'little') +
              d.to_bytes(4, 'little'))
    
    return digest.hex()

if __name__ == "__main__":
    #message = input("Enter a string: ").encode('utf-8')
    with open("shibuyakanon.jpg", 'rb') as file:
        message = file.read()
    md5_hash = md5(message)
    print("MD5 Hash:", md5_hash)