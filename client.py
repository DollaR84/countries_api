import logging

from aiohttp import ClientSession

from schemas import Country


class RestCountriesClient:

    def __init__(self):
        self.base_url: str = "https://restcountries.com/v3.1/all"
        self.headers: list[str] = list(Country.__fields__.keys())

    @property
    def api_url(self) -> str:
        return "?".join([
            self.base_url,
            "=".join([
            "fields",
            ",".join(self.headers)
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
