import cv2

print(cv2.getBuildInformation())
print('CUDA available:', cv2.cuda.getCudaEnabledDeviceCount() > 0)