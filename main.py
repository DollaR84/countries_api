import asyncio

from prettytable import PrettyTable

from client import RestCountriesClient

from schemas import Country


def console_output(headers: list[str], data: list[Country]):
    table = PrettyTable()
    table.field_names = headers
    for country in data:
        table.add_row([country.name, country.capital, country.flags])

    print(table)


async def main():
    countries = RestCountriesClient()
    data = await countries.get_data()
    console_output(countries.headers, data)


if "__main__" == __name__:
    asyncio.run(main())
