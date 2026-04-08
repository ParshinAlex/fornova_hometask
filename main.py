import scrape_api_response, parse_api_response
import asyncio

async def main():
    await scrape_api_response.run_scrape()
    parse_api_response.get_rates_file()

if __name__ == "__main__":
    asyncio.run(main())