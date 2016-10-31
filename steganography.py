from PIL import Image
import getpass
import sys
import crypto

def hide_core(image_data, secret, size):
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

def hide(image_name, new_image_name, secret_name, key):
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    with open(secret_name, 'rb') as f:
        secret = f.read()

    len_of_secret = len(secret)

    if len(secret) != 0:  # length of secret mist be a multiple of 16 for AES
        secret += b'*' * (16 - len(secret) % 16)
        # could be a random char
    secret = crypto.encrypt(secret, key)

    # in first four pixels is length of a  message
    length_data = bytearray()
    while len(length_data) < 4:
        length_data = bytearray([len_of_secret % 256]) + length_data
        len_of_secret >>= 8
    secret = length_data + secret

    # if is not possible to fit all data into image
    if len(secret) > image.size[0] * image.size[1]:
        return False

    new_image = hide_core(image_data, secret, image.size)
    new_image.save(new_image_name)
    return True

def find_core(image_data, size):
    secret = bytes()
    index = 0
    real_index = 0
    num = 4

    for y in range(size[1]):
        for x in range(size[0]):
            r, g, b, a = image_data.getpixel((x, y))

            if index > 0 or num > 0:
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
                    if num == 0:
                        real_index = index
                        if index % 16 != 0:
                            index += 16 - (index % 16)
                else:
                    secret += bytes([value])
                    index -= 1
            else:
                break

    secret = crypto.decrypt(secret, key)
    secret = secret[:real_index]
    return secret

def find(image_name, secret_name, key):
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    secret = find_core(image_data, image.size)

    with open(secret_name, 'wb') as f:
        f.write(secret)


if __name__ == '__main__':
    args = sys.argv

    if len(args) == 5 and args[1] == 'hide':
        image_name = args[2]
        new_image_name = args[3]
        secret_name = args[4]

        key = crypto.create_key(getpass.getpass('Password:'))
        if not hide(image_name, new_image_name, secret_name, key):
            print('Could not fit all secret data into the image.')

    elif len(args) == 4 and args[1] == 'find':
        image_name = args[2]
        secret_name = args[3]

        key = crypto.create_key(getpass.getpass('Password:'))
        find(image_name, secret_name, key)

    else:
        print('usage:\n'
            + 'python3 steganography.py hide <input_image> <output_image> <secret_file>\n'
            + 'python3 steganography.py find <input_image> <secret_file_output>')
