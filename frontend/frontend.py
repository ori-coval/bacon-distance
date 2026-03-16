from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home():
    """page for users to get bacon distance"""
    return """
    <!DOCTYPE html>
    <html>
    <body>

        <h2>get bacon distance</h2>

        <input id="textInput" type="text" placeholder="enter actor name"/>
        <button onclick="getName()">send</button>

        <h3>result</h3>
        <div id="result"></div>

        <script>
        async function getName() {
            const name = document.getElementById("textInput").value
            const resultBox = document.getElementById("result")
            resultBox.innerText = "Loading..."

            try {
                const response = await fetch("http://127.0.0.1:8000/bacon-distance/" + encodeURIComponent(name))

                const data = await response.json()
                resultBox.innerText = JSON.stringify(data, null, 2)
            } catch (error) {
                resultBox.innerText = "Error: " + error
            }
        }
        </script>

    </body>
    </html>
    """
