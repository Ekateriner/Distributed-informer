import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytest import mark
import asyncio
from telethon.tl.custom.message import Message


@mark.asyncio
async def test_help(client: TelegramClient):
    # Create a conversation
    async with client.conversation("@Incident_Informing_Bot", timeout=5) as conv:
        # Send a command
        await conv.send_message("/help")
        # Get response
        resp: Message = await conv.get_response()
        # Make assertions
        print(resp.raw_text)
        assert "/👎help" in resp.raw_text


@mark.asyncio
async def test_reg_del(client: TelegramClient):
    # Create a conversation
    async with client.conversation("@Incident_Informing_Bot", timeout=5) as conv:
        # Send a command
        await conv.send_message("/register")
        resp: Message = await conv.get_response()
        await conv.send_message('hfhfhfhf')
        assert "You have to" in resp.raw_text
        await conv.send_message("/register")
        resp: Message = await conv.get_response()
        await conv.send_message('a@mail.ru +78908908890')
        assert "Done" in resp.raw_text
        await conv.send_message("/delete")
        resp: Message = await conv.get_response()
        # Make assertions
        print(resp.raw_text)
        assert "You have been" in resp.raw_text


async def main():
    global api_id
    # set api_id
    # api_id = 12345
    global api_hash
    # set api_hash
    # api_hash = "abcdefg"
    async with TelegramClient(StringSession(), api_id, api_hash) as cl:
        global session_str
        session_str = cl.session.save()
        print("Your session string is:", cl.session.save())
        await test_help(cl)
        await test_reg_del(cl)

# uncomment following strings to test bot while it is working
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
