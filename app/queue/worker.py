import asyncio
from saq import Queue

from app.queue import REDIS_URL
from app.queue.jobs import generate_image_job

settings = {
    "queue": Queue.from_url(REDIS_URL),
    "functions": [generate_image_job],
    "concurrency": 1,  # GPU는 한 번에 하나씩
}


async def main():
    """워커 실행"""
    queue = Queue.from_url(REDIS_URL)
    await queue.connect()

    from saq import Worker

    worker = Worker(
        queue=queue,
        functions=[generate_image_job],
        concurrency=1,
    )
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
