import httpx

async def coordenadas(address: str):

    print("direccion:", address)
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "co"
    }
    headers = {
        "User-Agent": "GymApp/1.0 nicolas.rioscon@gmail.com"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)

    print(response)

    data = response.json()

    print(data)

    if not data:
        return None

    return (data[0]["lat"], data[0]["lon"])