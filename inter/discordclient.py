import httpx

import config

API_BASE = "https://discord.com/api/v8"
COMMANDS_PAYLOAD = [
    {
        "name": "roll",
        "description": "Roll some dice!",
        "options": [
            {
                "type": 3,  # string
                "name": "dice",
                "description": "The dice to roll",
                "required": True
            }
        ]
    },
    {
        "name": "eroll",
        "description": "Roll some dice, ephemerally!",
        "options": [
            {
                "type": 3,  # string
                "name": "dice",
                "description": "The dice to roll",
                "required": True
            }
        ]
    }
]


class DiscordClient:
    def __init__(self):
        self.http = httpx.AsyncClient(base_url=API_BASE)
        self.client_credentials_token = None

    async def close(self):
        await self.http.aclose()

    # ==== startup ====
    async def get_client_credentials_token(self):
        resp = await self.http.post(
            f"/oauth2/token",
            auth=(config.DISCORD_APPLICATION_ID, config.DISCORD_APPLICATION_SECRET),
            data={"grant_type": "client_credentials", "scope": "applications.commands.update"}
        )
        resp.raise_for_status()
        self.client_credentials_token = resp.json()['access_token']

    async def register_global_commands(self):
        resp = await self.http.put(
            f"/applications/{config.DISCORD_APPLICATION_ID}/commands",
            headers={"Authorization": f"Bearer {self.client_credentials_token}"},
            json=COMMANDS_PAYLOAD
        )
        resp.raise_for_status()

    async def register_guild_commands(self, guild_id: str):
        resp = await self.http.put(
            f"/applications/{config.DISCORD_APPLICATION_ID}/guilds/{guild_id}/commands",
            headers={"Authorization": f"Bearer {self.client_credentials_token}"},
            json=COMMANDS_PAYLOAD
        )
        resp.raise_for_status()
