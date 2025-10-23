first_image = 0x1FCC30

with open(r"C:\games\Fatal_Frame_PS2_NTSC_USA-NSDOTHACK\IMG_BD.BIN", 'rb') as file:

    while True:
        x = file.tell()

        if x >= first_image:
            break

        y = int.from_bytes(file.read(4), 'little')
        print(x, y)

        if y == (first_image - x):
            print('FIND!!!')
            break

    print("Относительных смещений не найдено...")