from src.Config.db import customerCollection, productCollection

async def create_indexex():
    await productCollection.create_index(
        [
            ("productname","text"),
            ("detail","text"),
            ("category","text"),
            ("brand","text"),
        ]
    )