import asyncio
import os.path
import time
import aiohttp
from urllib.parse import urlparse

from info import info

URL = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'

async def delay(ms):
    await asyncio.sleep(ms / 1000)

async def download_image(session, image_url, file_path) -> None:
    print(f'Downloading {image_url}')
    try:
        async with session.get(image_url) as response:
            status = response.status

            if status != 200:
                raise Exception(f"Failed to get image: status {status}")

            content = await response.read()

            with open(file_path, 'wb') as f:
                f.write(content)

    except Exception as e:
        print(f"Error downloading image: {str(e)}")

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                status = response.status
                if status != 200:
                    raise Exception(f"Failed to fetch json file: status {status}")

                json_data = await response.json()
                data = json_data.get("data")

                if not data:
                    raise Exception("JSON data does not have \'data\' property as its root")

                download_dir = os.path.join(os.getcwd(), 'downloads')
                if not os.path.exists(download_dir):
                    os.mkdir(download_dir)
                    print(f"Created {download_dir}")

                file_items = 1
                for key, sub_property in data.items():
                    if sub_property and sub_property.get("dsd"):
                        # Only download 5 images (to save bandwidth)
                        if file_items >= 5: break

                        parsed_url = urlparse(sub_property["dsd"])
                        ext = os.path.splitext(parsed_url.path)[-1] or '.jpg'

                        file_name = f"{file_items}{ext}"
                        file_path = os.path.join(download_dir, file_name)

                        await download_image(session, parsed_url.geturl(), file_path)

                        file_items += 1
                        await delay(250)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # CLI version and description info
    info("0.0.0")

    # Sleep of {sec} second before executing main function.
    time.sleep(2)

    asyncio.run(main())
