import requests
from cryptography.fernet import Fernet

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse


def get_file_from(CID):
    res = requests.get(f"https://cloudflare-ipfs.com/ipfs/{CID}")
    return res.text

app = FastAPI()

def decrypting(data, key):
    Encrypt = Fernet(key)
    enc_data = Encrypt.decrypt(data)
    new_file = open("nft.png", 'wb')
    new_file.write(enc_data)
    new_file.close()


@app.post("/get_cid/")
async def get_cid_file(cid1: str = Form(...), cid2: str = Form(...), cid3: str = Form(...), cid4: str = Form(...), golden_key: str = Form(...)):
    all_cids = [cid1,cid2,cid3,cid4]
    all_bin = bytes()
    for c in all_cids:
        all_bin += get_file_from(c).encode("utf-8")
    decrypting(all_bin, golden_key)

    return FileResponse("nft.png", media_type='application/octet-stream',filename="nft.png")


@app.get("/")
async def main():
    content = """
<body>
<form action="/get_cid/" method="post">
<label>cid1: </label>
<input name="cid1" type="text" ><br /><br />
<label>cid2: </label>
<input name="cid2" type="text" ><br /><br />
<label>cid3: </label>
<input name="cid3" type="text" ><br /><br />
<label>cid4: </label>
<input name="cid4" type="text" ><br /><br />

<label>golden key: </label>
<input name="golden_key" type="text" ><br /><br />
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.get("/get")
async def geting():
    return FileResponse("temp.txt", media_type='application/octet-stream',filename="temp.txt")

