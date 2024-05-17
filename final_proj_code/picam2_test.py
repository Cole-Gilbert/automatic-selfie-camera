from picamera2 import Picamera2, Preview
import time
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
picam2.capture_file(f"test2_{timestamp}.jpg")
