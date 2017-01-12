from PIL import Image
import getpass
import sys
import crypto

def progress(current, total):
    """Simple terminal progress bar. Be careful when printing other things (use ``\\r``).
    """
    if current == total:
        print('\rProgress: |' + 20 * '█' + '| 100%')
        return
    perc = (100 * current) // total
    bar = '█' * (20 * perc // 100) + '-' * (20 - 20 * perc // 100)
    print('\rProgress: |{}| {}%'.format(bar, perc), end=' ')

def hide_core(image_data, secret, size):
    """
    Hides secret data in image. The actual thing happens in :func:`steganography.hide_core`.

    :param image_data: PIL Image object.
    :param secret: ``bytearray`` object wwhich is to be hidden in the image.
    :param size: Tuple, x and y size of the image.
    :returns: New PIL Image with hidden and encrypted ``secret``.
    """
    new_image = Image.new('RGBA', size)
    new_image_data = new_image.getdata()

    index = 0
    for y in range(size[1]):
        if y % 10 == 0:
            progress(y, size[1])
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
    """
    Hides secret data in image. The actual thing happens in :func:`steganography.hide_core`.

    :param image_name: Name of the image where data will be hidden.
    :param new_image_name: Name of the output image.
    :param secret_name: Name of file which will be hidden in image.
    :param key: Hash of encryption password. Use :func:`crypto.create_key`.
    :returns: ``True`` if everything was successful, else ``False``.
    """
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    with open(secret_name, 'rb') as f:
        secret = f.read()

    len_of_secret = len(secret)

    if len(secret) != 0:  # length of secret must be a multiple of 16 for AES
        secret += b'*' * (16 - len(secret) % 16)
        # TODO: could be a random char

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

    progress(0, 1)
    new_image = hide_core(image_data, secret, image.size)
    new_image.save(new_image_name)
    progress(1, 1)
    return True

def find_core(image_data, size):
    """
    Finds hidden data in image.

    :param image_data: PIL Image file.
    :param size: Tuple, x and y size of the image.
    :returns: Decrypted found data.
    """
    secret = bytearray()
    index = 0
    real_index = 0
    num = 4
    found = 0
    finished = False

    for y in range(size[1]):
        if y % 10 == 9:
            progress(found, found + index)
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
                    secret.append(value)
                    index -= 1
                    found += 1
            else:
                finished = True
                break
        if finished:
            break

    if not finished:
        pass
        # TODO
        # raise InvalidInputImage or something like that
        # (no data was hidden in this image)

    secret = crypto.decrypt(bytes(secret), key)
    secret = secret[:real_index]

    return secret

def find(image_name, secret_name, key):
    """
    Finds secret data in image. The actual thing happens in :func:`steganography.find_core`.

    :param image_name: Name of an image with hidden data.
    :param secret_name: Name of output file where decrypted data is stored.
    :param key: Hash of encrypted file password. Use :func:`crypto.create_key`.
    """
    progress(0, 1)
    image = Image.open(image_name)
    image_data = image.convert('RGBA').getdata()

    secret = find_core(image_data, image.size)

    with open(secret_name, 'wb') as f:
        f.write(secret)
    progress(1, 1)


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
