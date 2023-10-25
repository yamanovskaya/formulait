import skimage.exposure as exposure  # модуль применяемый для увеличения экспозиции избражения
import os
import cv2 as cv
import numpy as np
import json
import io

OUTPUT_DIR_TEMP = 'TEMP'
OUTPUT_DIR_PREVIEW = 'PREVIEW'
OUTPUT_DIR_DATA = 'PROCESSED'
def get_data_file_path(id):
    filename_new = f'{OUTPUT_DIR_DATA}//{id}.json'
    return filename_new

def get_preview_from_file(filename):
    if not os.path.exists(OUTPUT_DIR_PREVIEW):
        os.makedirs(OUTPUT_DIR_PREVIEW)
    imgs = cv.imreadmulti(os.path.join(OUTPUT_DIR_PREVIEW, filename), flags=cv.IMREAD_GRAYSCALE + cv.IMREAD_ANYDEPTH)[1]
    for _, img in enumerate(imgs):
        # повысили экспозицию изображения (не меняя при этом глубину (также 16 бит осталось))
        img_norm = exposure.rescale_intensity(img, in_range='image', out_range='dtype').astype(np.uint16)
        cv.imwrite(f'{OUTPUT_DIR_PREVIEW}\\{filename}.tif',
                   img_norm)
    img = cv.imread(os.path.join(OUTPUT_DIR_PREVIEW, filename), 0)
    filename_new = f'{OUTPUT_DIR_PREVIEW}\\{filename}.png'
    # сохранение изображения в папку
    is_success, buffer = cv.imencode(".png", img)
    io_buf = io.BytesIO(buffer)
    os.remove(f'{OUTPUT_DIR_PREVIEW}\\{filename}')
    return io_buf.read()
def do_processing_image(dir, filename):
    id = filename
    filename += '.tif'
    image_dir = dir  # папка с исходными изображениями
    if not os.path.exists(OUTPUT_DIR_TEMP):
        os.makedirs(OUTPUT_DIR_TEMP)
    if not os.path.exists(OUTPUT_DIR_DATA):
        os.makedirs(OUTPUT_DIR_DATA)
    imgs = cv.imreadmulti(os.path.join(image_dir, id), flags=cv.IMREAD_GRAYSCALE + cv.IMREAD_ANYDEPTH)[1]

    for _, img in enumerate(imgs):
        # повысили экспозицию изображения (не меняя при этом глубину (также 16 бит осталось))
        img_norm = exposure.rescale_intensity(img, in_range='image', out_range='dtype').astype(np.uint16)
        cv.imwrite(f'{OUTPUT_DIR_TEMP}\\{filename}',
                   img_norm)  # сохранили изображения после экспозиции в новую папку

    piece_whole_count = 0  # счетчик количества кусочков на всех картинках
    cluster_whole_count = 0  # счетчик количества контуров на всех картинках
    # Load
    img = cv.imread(os.path.join(OUTPUT_DIR_TEMP, filename), 0)

    # обводим контуры на изображени вокруг белых пятен, толщина обводки по умолчанию 1 пиксель
    img_normalized = cv.Canny(img, 1, 2)

    # Apply thresholding to the normalized image to create a binary image (возвращает нижний порог и матрицу)
    _, thresh = cv.threshold(img_normalized, 1, 2, cv.THRESH_BINARY)

    # Find contours in binary image
    contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store contour areas
    contour_areas = []

    # Initialize a counter for the number of pieces
    piece_count = 0
    cluster_count = 0

    # Iterate through the detected contours
    for contour in contours:
        # Calculate the area of each contour
        area = cv.contourArea(contour)
        contour_areas.append(area)

    # Calculate the mean and standard deviation of contour areas
    mean_area = np.mean(contour_areas)
    std_deviation = np.std(contour_areas)

    # Define a threshold for distinguishing between pieces and clusters
    piece_threshold = mean_area - 0.5 * std_deviation
    cluster_threshold = mean_area + 0.5 * std_deviation

    for contour_area in contour_areas:
        # Compare mean_area with every area in image
        if contour_area > cluster_threshold:
            cluster_count += 1
            cluster_whole_count += 1
        elif contour_area >= piece_threshold:
            piece_count += 1
            piece_whole_count += 1

    h = img_normalized.shape[1]  # высота исходного изображения
    w = img_normalized.shape[0]  # ширина исходного изображения
    img_normalized = img_normalized[w // 2: w // 2 + 20,
                     h // 2:h // 2 + 20]  # вырезали кусочек изображения из центра (20*20 пикселей)
    img_normalized_big = cv.resize(img_normalized,
                                   (200, 200))  # увеличили размер изображения (было 20*20 стало 200*200)
    filename_new = f'{OUTPUT_DIR_DATA}\\{h // 2}_{h // 2 + 20}_{w // 2}_{w // 2 + 20}_{filename}.png'
    # сохранение изображения в папку
    cv.imwrite(filename_new, img_normalized)
    #         cv.imshow('result', img_normalized_big) # вывод этого кусочка на экран
    #         cv.waitKey(0) # метод с аргументом 0, показывающий, что изображение будет открыто всегда, пока пользователь его не закроет

    in_file = open(filename_new, "rb")  # opening for [r]eading as [b]inary
    data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    img_info = {'filename': filename_new,
                'contours': len(contours),
                'pieces': piece_count,
                'clusters': cluster_count,
                'pieces_while_count': piece_whole_count,
                'cluster_whole_count': cluster_whole_count
                }

    with open(get_data_file_path(id), 'w') as f:
        json.dump(img_info, f)
    return img_info
    print(f"picture: {filename}")
    print(f'{len(contours)} contour(s) found')
    print(f"Number of pieces: {piece_count}")
    print(f"Number of clasters: {cluster_count}", end='\n\n')
    print(f"Number of pieces all images: {piece_whole_count}")
    print(f"Number of clasters all images: {cluster_whole_count}")