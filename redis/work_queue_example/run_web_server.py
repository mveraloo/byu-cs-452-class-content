# import the necessary packages
#from keras.preprocessing.image import img_to_array
from email.mime import image
from tensorflow.keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import settings
import helpers
import flask
import redis
import uuid
import time
import json
import io
from logger import log


# initialize our Flask application and Redis server
app = flask.Flask(__name__)
db = redis.StrictRedis(host=settings.REDIS_HOST,
	port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)


#Enable Redis notifications
try:
    db.config_set('notify-keyspace-events', 'KEA')
    log("WEB_SERVER", "Redis notifications enabled")
except Exception as e:
    log("WEB_SERVER", f"Redis notification setup failed: {e}")



def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

@app.route("/")
def homepage():
	return "Welcome to the PyImageSearch Keras REST API!"

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    log("WEB_SERVER", "Started prediction")

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format and prepare it for
            # classification
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image,
                                 (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))

            # ensure our NumPy array is C-contiguous as well,
            # otherwise we won't be able to serialize it
            image = image.copy(order="C")

            # generate an ID for the classification then add the
            # classification ID + image to the queue
            k = str(uuid.uuid4())
             
            image_encoded = helpers.base64_encode_image(image)
            d = {"id": k, "image": image_encoded}

            print(f"Starting job: {k}")

            # NOTIFICATION CODE
            p = db.pubsub()

            # Subscribe BEFORE queueing work
            p.psubscribe(f"__keyspace@0__:{k}")

            # Get the subscription confirmation message
            p.get_message()

            # Push work to queue
            db.rpush(settings.IMAGE_QUEUE, json.dumps(d))
            print(f"Job queued: {k}")

            # Wait for notification
            print("Waiting for notification...")
            notification_received = False

            # Wait for notification with timeout
            start_time = time.time()
            while (time.time() - start_time) < 30:  # 30 second timeout
                message = p.get_message(timeout=10.0)
                if message and message['type'] == 'pmessage':
                    print(f"✅ Notification received: {message}")
                    notification_received = True
                    break
                time.sleep(0.1)

            # Get the result
            output = db.get(k)
            if output:
                data["predictions"] = json.loads(output.decode("utf-8"))
                data["success"] = True
                print(f"Success! Got predictions")
                db.delete(k)
                log("WEB_SERVER", f"Finished job {k}")
            else:
                print("No result found")
                log("WEB_SERVER", f"Job failed {k}")

            # POLLING BACKUP if notification failed
            if not data["success"]:
                print("Using polling backup...")
                for i in range(30):  # Try for 3 seconds
                    output = db.get(k)
                    if output:
                        data["predictions"] = json.loads(output.decode("utf-8"))
                        data["success"] = True
                        db.delete(k)
                        print("Success via polling backup!")
                        log("WEB_SERVER", f"Finished job {k}")
                        break
                    time.sleep(0.1)

            p.close()
            

    # return the response as JSON
    return flask.jsonify(data)



# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production
if __name__ == "__main__":
	print("* Starting web service...")
	app.run()
