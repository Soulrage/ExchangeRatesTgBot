from datetime import datetime
import xml.etree.ElementTree as ET
import aiohttp
import asyncio

async def fetch_xml_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cbr.ru/scripts/XML_daily.asp') as req:
            return await req.text()

async def parsing_current_rate():
    xml_data = await fetch_xml_data()
    root = ET.fromstring(xml_data)

    dict_current_rate = {'RUB': 1}
    for valute in root.findall('Valute'):
        name = valute.find('CharCode').text
        value = valute.find('VunitRate').text
        dict_current_rate[name] = value
    return dict_current_rate

