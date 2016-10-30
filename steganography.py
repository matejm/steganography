from PIL import Image

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

def hide(image_name, new_image_name, secret_name):
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    with open(secret_name, 'rb') as f:
        secret = f.read()

    # in first four pixels is length of a  message
    len_of_secret = len(secret)
    length_data = bytearray()
    while len(length_data) < 4:
        length_data = bytearray([len_of_secret % 256]) + length_data
        len_of_secret >>= 8
    secret = length_data + secret

    new_image = hide_core(image_data, secret, image.size)
    new_image.save(new_image_name)

def find_core(image_data, size):
    secret = bytearray()
    index = 0
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
                else:
                    secret.append(value)
                    index -= 1
            else:
                break
    return secret

def find(image_name):
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    secret = find_core(image_data, image.size)

    return secret.decode('utf8')

if __name__ == '__main__':
    # TODO: parse command line arguments
    image_name = 'image.png'
    new_image_name = 'image2.png'
    secret_name = 'secret.txt'
    hide(image_name, new_image_name, secret_name)

    print(find(new_image_name))
