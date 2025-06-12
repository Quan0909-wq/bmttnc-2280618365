import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    # Lặp qua từng pixel và kênh màu để trích xuất các bit
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3): # Duyệt qua các kênh màu R, G, B
                # Trích xuất bit ít quan trọng nhất (LSB)
                # và thêm nó vào chuỗi nhị phân
                binary_message += format(pixel[color_channel], '08b')[-1]
    
    message = ""
    # Lặp qua chuỗi nhị phân, từng 8 bit một, để chuyển đổi thành ký tự
    for i in range(0, len(binary_message), 8):
        char_binary = binary_message[i:i+8]
        char = chr(int(char_binary, 2)) # Chuyển đổi chuỗi nhị phân 8 bit thành ký tự

        # Kiểm tra đánh dấu kết thúc thông điệp
        # Dựa trên encrypt.py trước đó, dấu kết thúc là '1111111111111110'
        # Do đó, khi ta thấy 16 bit cuối là '1111111111111110', ta biết thông điệp đã kết thúc.
        # Hoặc như trong code này, nó kiểm tra ký tự null ('\0') hoặc một giá trị không mong muốn
        # Tuy nhiên, theo logic của encrypt.py, chúng ta nên kiểm tra chuỗi 16 bit cuối.
        # Ở đây tôi sẽ bám theo logic của hình ảnh (nếu gặp '\0' thì dừng)
        # và cũng đề cập đến cách kiểm tra dấu kết thúc từ encrypt.py.
        
        # Nếu chúng ta gặp một ký tự null hoặc một ký tự đặc biệt được sử dụng làm điểm dừng
        # thì thông điệp đã kết thúc.
        # Nếu encrypt.py dùng '1111111111111110' làm dấu kết thúc
        # thì chúng ta cần kiểm tra 16 bit cuối.
        # Đây là đoạn mã để kiểm tra dấu kết thúc thông điệp (16 bit cuối)
        # if i + 16 <= len(binary_message) and binary_message[i:i+16] == '1111111111111110':
        #     # Remove the end-of-message marker before returning the message
        #     message = message[:-2] # If the marker was part of the character conversion
        #     break

        # Theo code trong ảnh, nó chỉ kiểm tra ký tự '\0'
        if char == '\0': # Có thể đây là cách họ đánh dấu kết thúc thông điệp
            break
        
        message += char
    
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == '__main__':
    main()