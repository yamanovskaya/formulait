# все в одном коде

import skimage.exposure as exposure # модуль применяемый для увеличения экспозиции избражения
import os 
import cv2 as cv
import numpy as np

image_dir = 'Formula_IT_2023_Images' # папка с исходными изображениями

for filename in os.listdir(image_dir):
    if filename.endswith('.tif'):
        imgs = cv.imreadmulti(os.path.join(image_dir, filename), flags = cv.IMREAD_GRAYSCALE + cv.IMREAD_ANYDEPTH)[1]

        for _,img in enumerate(imgs):
            # повысили экспозицию изображения (не меняя при этом глубину (также 16 бит осталось))
            img_norm = exposure.rescale_intensity(img, in_range='image', out_range = 'dtype').astype(np.uint16)
            cv.imwrite(f'Formula_IT_2023_Images_after\\{filename}', img_norm) # сохранили изображения после экспозиции в новую папку
            
            
image_dir = 'Formula_IT_2023_Images_after' # папка с изображениями с повышенной экспозицией

piece_whole_count = 0 # счетчик количества кусочков на всех картинках
cluster_whole_count = 0 # счетчик количества контуров на всех картинках
for filename in os.listdir(image_dir):
    if filename.endswith('.tif'):
        # Load 
        img = cv.imread(os.path.join(image_dir, filename), 0)
        
        # обводим контуры на изображени вокруг белых пятен, толщина обводки по умолчанию 1 пиксель
        img_normalized = cv.Canny(img, 1,2)
        
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
        w  = img_normalized.shape[0]  # ширина исходного изображения
        img_normalized = img_normalized[w // 2: w // 2 + 20, h // 2:h // 2 + 20] # вырезали кусочек изображения из центра (20*20 пикселей)
        img_normalized_big = cv.resize(img_normalized, (200, 200)) # увеличили размер изображения (было 20*20 стало 200*200)
        #сохранение изображения в папку
        cv.imwrite(f'part_of_imgs\\{h // 2}_{h // 2 + 20}_{w // 2}_{w // 2 + 20}_{filename}', img_normalized) 
#         cv.imshow('result', img_normalized_big) # вывод этого кусочка на экран
#         cv.waitKey(0) # метод с аргументом 0, показывающий, что изображение будет открыто всегда, пока пользователь его не закроет
        print(f"picture: {filename}")
        print(f'{len(contours)} contour(s) found')
        print(f"Number of pieces: {piece_count}")
        print(f"Number of clasters: {cluster_count}", end = '\n\n')
print(f"Number of pieces all images: {piece_whole_count}")
print(f"Number of clasters all images: {cluster_whole_count}")

