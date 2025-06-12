import sys
from PIL import Image # Đảm bảo rằng bạn đã cài đặt Pillow: pip install Pillow

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    pixel_index = 0

    # Chuyển đổi thông điệp thành chuỗi nhị phân
    # '08b' định dạng mỗi ký tự thành 8 bit nhị phân (ví dụ: 'a' -> '01100001')
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110' # Đánh dấu kết thúc thông điệp (16 bit)

    data_index = 0
    # Lặp qua từng pixel và kênh màu để nhúng thông điệp
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row))) # Lấy giá trị RGB của pixel

            for color_channel in range(3): # Duyệt qua các kênh màu R, G, B
                if data_index < len(binary_message):
                    # Sửa đổi bit ít quan trọng nhất (LSB) của kênh màu
                    # Lấy bit thứ 'data_index' từ 'binary_message'
                    # Đặt LSB của 'pixel[color_channel]' thành bit này
                    pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_message[data_index])
                    data_index += 1
            
            # Đặt pixel đã sửa đổi trở lại hình ảnh
            img.putpixel((col, row), tuple(pixel))
        
        # Nếu tất cả các bit của thông điệp đã được nhúng, thoát vòng lặp
        if data_index >= len(binary_message):
            break

    encoded_image_path = "encoded_image.png"
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)
    return encoded_image_path

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == '__main__':
    main()