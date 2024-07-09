import asyncio
import logging

from aiohttp import ClientSession

from prettytable import PrettyTable

from schemas import Country


class RestCountries:

    def __init__(self):
        self.base_url: str = "https://restcountries.com/v3.1/all"
        self.fields: list[str] = list(Country.__fields__.keys())

    @property
    def api_url(self) -> str:
        return "?".join([
            self.base_url,
            "=".join([
            "fields",
            ",".join(self.fields)
            ])
        ])

    async def get_data(self) -> list[Country]:
        async with ClientSession() as session:
            try:
                return await self.get(session, self.api_url)

            except Exception as error:
                logging.error(error, exc_info=True)

    async def get(self, session: ClientSession, url: str) -> list[Country]:
        async with session.get(url) as response:
            data = await response.json()
            return self.parse(data)

    def parse(self, data: list[dict]) -> list[Country]:
        results = []
        for country in data:
            capital = country.get("capital")

            results.append(Country(
                name=country.get("name", {}).get("official"),
                capital=capital[0] if capital else "",
                flags=country.get("flags", {}).get("png"),
            ))

        return results


def console_output(data: list[Country]):
    table = PrettyTable()
    table.field_names = list(Country.__fields__.keys())
    for country in data:
        table.add_row([country.name, country.capital, country.flags])

    print(table)


async def main():
    countries = RestCountries()
    data = await countries.get_data()
    console_output(data)


if "__main__" == __name__:
    asyncio.run(main())
