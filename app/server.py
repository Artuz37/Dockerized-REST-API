from fastapi import FastAPI, Body,HTTPException
from pydantic import BaseModel
from PIL import Image
import requests
import io


from classifier.pred_model import ClassificationModel

app = FastAPI()
model = ClassificationModel('classifier/models/better_model.pth')


class ImgRequest(BaseModel):
    img_url: str

    class Config:
        schema_extra = {
            "examples": {
                "Hotdog picture":{"img_url": "https://img.wprost.pl/img/hot-dog/07/04/19f55c7a40414dd770057f122818.jpeg"},
                "Not a hotdog picture": {
                    "img_url": "https://img.wprost.pl/img/hot-dog/07/04/19f55c7a40414dd770057f122818.jpeg"}
            }
        }


@app.get("/")
def home():
    return {'data' : 'hej'}

@app.post("/classify")
def classify(request: ImgRequest=Body(
        ...,
        examples={
            "Hotdog picture": {
                "summary": "A usual hotdog",
                "description": "Typical hotdog, classifies correctly.",
                "value": {
                    "img_url": "https://img.wprost.pl/img/hot-dog/07/04/19f55c7a40414dd770057f122818.jpeg"
                },
            },
            "Not a hotdog picture": {
                "summary": "A dog",
                "description": "A dog that's not hot, classifies correctly.",
                "value": {
                    "img_url": "https://www.zoo-mar.pl/wp-content/uploads/2019/10/dog-niemiecki.jpg"
                },
            },
            "Wrong format of picture": {
                "summary": "Hotdog in png",
                "description": "Url linking to photo of not implemented format. Return error message.",
                "value": {
                    "img_url": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Hot_dog_with_mustard.png"
                },
            },
            "Wrong url": {
                "summary": "Not a valid url",
                "description": "img_url not being proper url, causing image load to fail.",
                "value": {
                    "img_url": "hotdog"
                },
            },
        },
    ),):

    if request.img_url.split(".")[-1] == 'png':
        return {"error_message":"png format not implemented!"}

    try:
        response = requests.get(request.img_url)
    except:
        raise HTTPException(status_code=400, detail="Provide valid url!")

    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)

    probability_of_hotdog = model.predict_image(img)

    return {'probability_of_hotdog' : probability_of_hotdog,
            'probability_of_not_hotdog': 1-probability_of_hotdog}