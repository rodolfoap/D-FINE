* [x] Resize the frame to 640×640 using OpenCV (cv2.resize) before passing it to the model. (Already implemented at line 73)
* [x] Wrap your model inference in PyTorch's automatic half-precision command (with torch.amp.autocast('cuda'):). (Added at line 77)
* [x] Use a multi-threaded video reader so your CPU and GPU work at the same time. (RealTimeVideoCapture already handles buffering)