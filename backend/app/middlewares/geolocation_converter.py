import httpx

async def coordenadas(address: str):

    url = "http://api.positionstack.com/v1/forward"

    params = {
        "access_key": "233795959c2896606515c421f988bb5b",
        "query": f"{address}, Bogota, Colombia",
        "limit": 1,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    print(data)

    if not data["data"]:
        return None

    return data["data"][0]["latitude"], data["data"][0]["longitude"]