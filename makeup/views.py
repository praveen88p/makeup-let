import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .make_up import MakeupApplication


def index(request):
    return render(request, 'makeup/video.html')


def generate_video(makeup_app):
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = makeup_app.process_frame(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    makeup_app = MakeupApplication()
    return StreamingHttpResponse(generate_video(makeup_app), content_type='multipart/x-mixed-replace; boundary=frame')
