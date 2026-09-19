import asyncio, httpx, time
async def main():
    async with httpx.AsyncClient() as c:
        start=time.perf_counter(); results=await asyncio.gather(*[c.post('http://localhost:8000/api/demo/ssh') for _ in range(20)]); elapsed=time.perf_counter()-start
        print({'events':len(results),'events_per_second':len(results)/elapsed,'average_ms':elapsed/len(results)*1000})
asyncio.run(main())
