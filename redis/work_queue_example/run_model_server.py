# import the necessary packages
from tensorflow.keras.applications import ResNet50
from keras.applications import imagenet_utils
import numpy as np
import settings
import helpers
import redis
import time
import json

import os
from logger import log

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# connect to Redis server
db = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_DB
)


def classify_process():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    print("* Loading model...")
    model = ResNet50(weights="imagenet")
    print("* Model loaded")
    log("MODEL_SERVER", "Started model server")

    # continually poll for new images to classify
    while True:
        # ✅ FIXED: Use BRPOP for atomic queue popping
        # This will block until a job is available and pop it atomically
        queue_result = db.brpop(settings.IMAGE_QUEUE, timeout=30)

        if queue_result:
            # queue_result is (queue_name, job_data)
            _, serialized_job = queue_result

            try:
                # Deserialize the job
                job_data = json.loads(serialized_job.decode("utf-8"))
                imageID = job_data["id"]
                log("MODEL_SERVER", f"Processing {imageID}")

                print(f"* Processing job: {imageID}")

                # Decode and prepare the image
                image = helpers.base64_decode_image(
                    job_data["image"],
                    settings.IMAGE_DTYPE,
                    (1, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH, settings.IMAGE_CHANS)
                )

                # Classify the image (single image, not batch)
                preds = model.predict(image)
                results = imagenet_utils.decode_predictions(preds)

                # Prepare output
                output = []
                for (imagenetID, label, prob) in results[0]:
                    output.append({"label": label, "probability": float(prob)})

                # Store the result
                db.set(imageID, json.dumps(output))
                log("MODEL_SERVER", f"Finished {imageID}")
                print(f"✅ Completed job: {imageID}")

            except Exception as e:
                print(f"Error processing job {imageID}: {e}!!")
                # On error, you might want to push back to queue or handle differently

        else:
            # No jobs available, sleep briefly
            time.sleep(settings.SERVER_SLEEP)


# if this is the main thread of execution start the model server
# process
if __name__ == "__main__":
    classify_process()
