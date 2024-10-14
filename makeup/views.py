import cv2
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .make_up import MakeupApplication
import base64

def index(request):
    """Render the main page."""
    return render(request, 'makeup/video.html')


def receive_frame(request):
    """Receive a frame from the client, process it, and return the processed image."""
    if request.method == 'POST':
        # Get the base64-encoded frame sent from the client
        frame_data = request.POST.get('frame')
        
        # Decode the base64 image
        frame_data = frame_data.split(',')[1]  # Remove the data URL prefix
        frame_bytes = base64.b64decode(frame_data)
        
        # Convert the image bytes into a NumPy array
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Process the frame with the MakeupApplication class
        makeup_app = MakeupApplication()
        processed_frame = makeup_app.process_frame(frame)

        # Encode the processed frame to JPEG
        _, jpeg = cv2.imencode('.jpg', processed_frame)
        processed_frame_bytes = jpeg.tobytes()

        # Convert the image to base64 to send back to the client
        processed_frame_b64 = base64.b64encode(processed_frame_bytes).decode('utf-8')

        # Send the processed frame back to the client
        return JsonResponse({'processed_frame': 'data:image/jpeg;base64,' + processed_frame_b64})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
