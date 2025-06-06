import numpy as np
import SimpleITK as sitk
import cv2
import glob
import os

DATA_PATH = 'images'  # Configure este caminho

def load_ct_scan(seriesuid):
    """Carrega um exame de TC completo do dataset LIDC-IDRI"""
    mhd_list = glob.glob(f'{DATA_PATH}/{seriesuid}.mhd', recursive=True)
    if not mhd_list:
        raise FileNotFoundError(f"Arquivo .mhd para seriesuid {seriesuid} não encontrado.")
    
    mhd_path = mhd_list[0]
    ct_scan = sitk.ReadImage(mhd_path)
    return {
        'image': sitk.GetArrayFromImage(ct_scan),
        'origin': np.array(ct_scan.GetOrigin()),
        'spacing': np.array(ct_scan.GetSpacing()),   
        'direction': np.array(ct_scan.GetDirection()).reshape(3,3),
        'size': np.array(ct_scan.GetSize())
    }

def world_to_voxel(world_coord, origin, spacing, direction):
    """Converte coordenadas mundiais para voxel"""
    voxel_coord = np.linalg.inv(direction) @ (world_coord - origin)
    return (voxel_coord / spacing).astype(int)

def apply_window(image, level=-600, width=1500):
    """Aplica janelamento de densidade óptica"""
    min_val = level - width//2
    max_val = level + width//2
    windowed = np.clip(image, min_val, max_val)
    return cv2.normalize(windowed, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def normalize_hu(image):
    """Normaliza as unidades Hounsfield para 0-255"""
    hu_min = -1000
    hu_max = 1000
    image = np.clip(image, hu_min, hu_max)
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)