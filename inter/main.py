import logging

import d20
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from . import config
from . import discordclient
from . import models

app = FastAPI()
discord = discordclient.DiscordClient()
log = logging.getLogger('main')


# ==== fastapi ====
async def verify_signature(request: Request):
    """Verify the Discord signature for POST requests to /"""
    verify_key = VerifyKey(bytes.fromhex(config.DISCORD_APPLICATION_PUBLIC_KEY))

    try:
        signature = request.headers["X-Signature-Ed25519"]
        timestamp = request.headers["X-Signature-Timestamp"]
        body = (await request.body()).decode("utf-8")
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except (KeyError, BadSignatureError):
        raise HTTPException(401, 'invalid request signature')


@app.post("/", response_model=models.InteractionResponse, dependencies=[Depends(verify_signature)])
async def command_entrypoint(interaction: models.Interaction):
    log.debug(f"Got interaction data: {interaction.json(indent=2)}")
    if interaction.type == models.InteractionType.PING:
        return models.InteractionResponse(type=models.InteractionType.PING)
    elif interaction.type == models.InteractionType.APPLICATION_COMMAND:
        return await handle_command(interaction)


@app.get("/")
async def redirect_invite():
    """GET / - redirect to the Discord oauth page for now"""
    return RedirectResponse(f"https://discord.com/api/oauth2/authorize?client_id={config.DISCORD_APPLICATION_ID}&scope=applications.commands")


@app.on_event("startup")
async def on_startup():
    await discord.get_client_credentials_token()
    await discord.register_global_commands()
    if config.TEST_GUILD_ID:
        await discord.register_guild_commands(config.TEST_GUILD_ID)


@app.on_event("shutdown")
async def on_shutdown():
    await discord.close()


# ==== commands ====
async def handle_command(interaction: models.Interaction) -> models.InteractionResponse:
    handler = command_handlers.get(interaction.data.name, command_default)
    return await handler(interaction)


async def command_default(*_, **__) -> models.InteractionResponse:
    return models.InteractionResponse(
        type=models.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=models.InteractionCommandCallbackData(
            content="The specified command was not found.",
            flags=models.InteractionCommandCallbackDataFlags.EPHEMERAL
        )
    )


async def command_roll(interaction: models.Interaction) -> models.InteractionResponse:
    result = d20.roll(interaction.data.options[0].value)
    return models.InteractionResponse(
        type=models.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=models.InteractionCommandCallbackData(
            content=str(result)
        )
    )


async def command_eroll(interaction: models.Interaction) -> models.InteractionResponse:
    result = d20.roll(interaction.data.options[0].value)
    return models.InteractionResponse(
        type=models.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
        data=models.InteractionCommandCallbackData(
            content=str(result),
            flags=models.InteractionCommandCallbackDataFlags.EPHEMERAL
        )
    )


command_handlers = {
    "roll": command_roll,
    "eroll": command_eroll,
}
