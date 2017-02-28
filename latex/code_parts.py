with open(secret_name, 'rb') as f:
    secret = f.read()

import getpass
geslo = getpass.getpass('Vpišite geslo: ')

key = crypto.create_key(getpass.getpass('Password: '))

self.label1 = tk.Label(self, text="Password:")
self.password = tk.Entry(self, show="*")

password = self.password.get()
self.password.delete(0, tk.END)
key = crypto.create_key(password)
del(password)

def encrypt(message, key):
    AESchiper = AES.new(key)
    return AESchiper.encrypt(message)

def create_key(string):
    hashed = sha256(bytes(string, 'utf8')).digest()
    return hashed

def hide_core(image_data, secret, size):
    ''' Zaradi preglednosti je v tej funkciji izpuščenih več
    vrstic, ki za samo razumevanje koncepta niso pomembne. '''
    new_image = Image.new('RGBA', size)
    new_image_data = new_image.getdata()

    index = 0
    for y in range(size[1]):
        for x in range(size[0]):
            r, g, b, a = image_data.getpixel((x, y))

            if index < len(secret):
                r &= ~3
                g &= ~3
                b &= ~3
                a &= ~3
                r |= secret[index] & 3
                g |= (secret[index] & 12) >> 2
                b |= (secret[index] & 48) >> 4
                a |= (secret[index] & 192) >> 6
                index += 1

            new_image_data.putpixel((x,y), (r, g, b, a))

    return new_image

r &= ~3

g |= (secret[index] & 12) >> 2

def find_core(image_data, size, key):
    ''' Zaradi preglednosti je v tej funkciji izpuščenih več
    vrstic, ki za samo razumevanje koncepta niso pomembne. '''
    secret = bytearray()
    index = 0
    real_index = 0
    num = 4
    finished = False

    for y in range(size[1]):
        for x in range(size[0]):
            if index > 0 or num > 0:
                r, g, b, a = image_data.getpixel((x, y))

                value = a & 3
                value <<= 2
                value |= b & 3
                value <<= 2
                value |= g & 3
                value <<= 2
                value |= r & 3

                if num > 0:
                    num -= 1
                    index <<= 8
                    index |= value
                else:
                    secret.append(value)
                    index -= 1
            else: break

    secret = crypto.decrypt(bytes(secret), key)
    return secret
