from ..database import DEFAULT_SESSION_MAKER


class Uow:
    repos = ()

    def __init__(self):
        self.session_factory = DEFAULT_SESSION_MAKER

    async def __aenter__(self):
        self.session = self.session_factory()

        for repo in self.repos:
            name, class_ = repo
            setattr(self, name, class_(session=self.session))

        return self

    async def __aexit__(self, *args):
        if any(args):
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
