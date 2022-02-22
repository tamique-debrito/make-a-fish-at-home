from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

app.mount("/img", StaticFiles(directory="img"), name="img")


class TestSubmission(BaseModel):
    name: str
    data: str


import random


def random_scale(alpha=0.25):
    return random.random() * alpha + (1 - alpha / 2)


class Fish:
    def __init__(self):
        self.body_img = f'b{random.randrange(1, 13)}.png'
        self.eye_img = f'e{random.randrange(1, 10)}.png'
        self.top_fin_img = f'tf{random.randrange(1, 8)}.png'
        self.bottom_fin_img = f'bf{random.randrange(1, 6)}.png'
        self.rear_fin_img = f'rf{random.randrange(1, 10)}.png'

        self.body_x_size = random_scale() * 150
        self.body_y_size = random_scale() * 100

        self.eye_x_size = self.eye_y_size = random_scale() * 20

        self.top_fin_x_size = random_scale() * 50
        self.top_fin_y_size = random_scale() * 50

        self.bottom_fin_x_size = random_scale() * 50
        self.bottom_fin_y_size = random_scale() * 50

        self.rear_fin_x_size = random_scale() * 50
        self.rear_fin_y_size = random_scale() * 50

        self.angle = random.random() * 6
        self.body_pos = (random.randint(10, 30), random.randint(10, 30))
        self.eye_pos = (self.body_pos[0] + 20 + random.gauss(0, 10), self.body_pos[1] + self.body_y_size/2 + random.gauss(0, 10))
        self.top_fin_pos = (self.body_pos[0] + 40 + random.gauss(0, 10), self.body_pos[1] + random.gauss(0, 5) - 10)
        self.bottom_fin_pos = (self.body_pos[0] + self.body_x_size/4 + random.gauss(0, 5),
                               self.body_pos[1] + self.body_y_size - 10 + random.gauss(0, 5))

        self.rear_fin_pos = (self.body_pos[0] + self.body_x_size * 0.9 + random.gauss(0, 5),
                             self.body_pos[1] + self.body_y_size / 3 + random.gauss(0, 5))

    def get_image_load_string(self):
        return f"[loadOneImage('img/{self.body_img}'), " \
               f"loadOneImage('img/{self.eye_img}'), " \
               f"loadOneImage('img/{self.top_fin_img}'), " \
               f"loadOneImage('img/{self.bottom_fin_img}'), " \
               f"loadOneImage('img/{self.rear_fin_img}')]"

    def get_draw_code(self):
        return (f"""
const body = imgs[0];
const eye = imgs[1];
const top_fin = imgs[2];
const bottom_fin = imgs[3];
const rear_fin = imgs[4];
var c = document.getElementById("the-canvas");
var ctx = c.getContext("2d");
ctx.translate({self.body_pos[0] + self.body_x_size/2}, {self.body_pos[1] + self.body_y_size/2});
ctx.rotate({self.angle});
ctx.translate(-{self.body_pos[0] + self.body_x_size/2}, -{self.body_pos[1] + self.body_y_size/2});
ctx.drawImage(body, {self.body_pos[0]}, {self.body_pos[1]}, {self.body_x_size}, {self.body_y_size});
ctx.drawImage(eye, {self.eye_pos[0]}, {self.eye_pos[1]}, {self.eye_x_size}, {self.eye_y_size});
ctx.drawImage(top_fin, {self.top_fin_pos[0]}, {self.top_fin_pos[1]}, {self.top_fin_x_size}, {self.top_fin_y_size});
ctx.drawImage(bottom_fin, {self.bottom_fin_pos[0]}, {self.bottom_fin_pos[1]}, {self.bottom_fin_x_size}, {self.bottom_fin_y_size});
ctx.drawImage(rear_fin, {self.rear_fin_pos[0]}, {self.rear_fin_pos[1]}, {self.rear_fin_x_size}, {self.rear_fin_y_size});
""")


@app.get('/')
def index():
    fish = Fish()
    return HTMLResponse(
        """
        
        <!doctype html>
        
        <html lang="en">
            <head>
              <meta charset="utf-8">
            
              <title>Make A Fish At Home</title>
            
            </head>
            
            
            <script>
                function loadOneImage(url) {
                    return new Promise(resolve => {
                        const img = new Image();
                        img.addEventListener('load', () => {resolve(img);});
                        img.src = url;
                    });
                }
                function loadAllImages(){
                    return Promise.all(""" + fish.get_image_load_string() + """);
                }
                window.onload = function() {
                    loadAllImages().then( (imgs) => {""" + fish.get_draw_code() + """});
                }
            </script>
            
            <style>
                canvas {
                    background-color:#5577AA;
                    outline: 2px solid white;
                    padding-left: 0;
                    padding-right: 0;
                    margin-left: auto;
                    margin-right: auto;
                    display: block;
                    width: 800px;
                    height: 600px;
                }
                p {
                    text-align: center;
                    color: white;
                }
            </style>
            
            
            
            <body style="background-color:#5577AA;">
                <div>
                    <canvas id='the-canvas'>
                    </canvas>
                </div>
                <p>Make A Fish At Home</p>
            </body>
        </html>
        
        """
    )
