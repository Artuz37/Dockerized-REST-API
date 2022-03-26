import pytest
import requests


def test_hotdog():
  r = requests.post('http://0.0.0.1:8000/predict', json={
    "img_url": "https://img.wprost.pl/img/hot-dog/07/04/19f55c7a40414dd770057f122818.jpeg"
  })
  print(r.json())
  assert r.json()["probability_of_hotdog"]>0.5


def test_wrong_url():
  r = requests.post('http://0.0.0.1:8000/predict', json={
    "img_url": "hot-dog"
  })

  assert r.json()["detail"] == "Provide valid url!"

