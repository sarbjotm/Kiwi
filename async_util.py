import asyncio

async def wait_for_response(self, ctx, seconds):
    try:
        msg = await self.client.wait_for(
            "message",
            timeout=seconds,
            check=lambda message: message.author == ctx.message.author and message.channel == ctx.channel
        )
        msg = msg.content.strip().lower()
        return msg
    except asyncio.TimeoutError:
        return None
        