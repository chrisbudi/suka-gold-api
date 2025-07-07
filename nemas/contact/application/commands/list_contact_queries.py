from contact.domain.repositories import ContactRequestRepository


class ListContactRequestsQuery:
    pass  # no filters for now


class ListContactRequestsHandler:
    def __init__(self, repository: ContactRequestRepository):
        self.repository = repository

    def handle(self, query: ListContactRequestsQuery):
        return self.repository.list_all()
