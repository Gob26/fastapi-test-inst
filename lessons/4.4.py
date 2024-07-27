import asyncio

async def q():
    print("q: Why can't programmers tell jokes?")
    await asyncio.sleep(3)
    print("q: 3 seconds have passed")
    await asyncio.sleep(2)
    print("q: 2 seconds have passed")
async def a():
    print("a: Timing!")
    await asyncio.sleep(1)
    print("a: 1 second has passed")

async def main():
    print("main: Starting tasks")
    await asyncio.gather(q(), a())
    print("main: Finished tasks")

print("Script started")
asyncio.run(main())
print("Script finished")
