from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status

from backend.app.schemas import (
    Ticket,
    TicketCreate,
    TicketStatus,
    TicketUpdate,
)


app = FastAPI(
    title="IncidentOps API",
    description="Backend API for the IncidentOps support platform.",
    version="0.3.0",
)


tickets: list[Ticket] = []
next_ticket_id = 1


def find_ticket_index(ticket_id: int) -> int:
    for index, ticket in enumerate(tickets):
        if ticket.id == ticket_id:
            return index

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ticket not found",
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "IncidentOps API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post(
    "/tickets",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(ticket_data: TicketCreate) -> Ticket:
    global next_ticket_id

    current_time = datetime.now(timezone.utc)

    ticket = Ticket(
        id=next_ticket_id,
        title=ticket_data.title,
        description=ticket_data.description,
        customer_email=ticket_data.customer_email,
        priority=ticket_data.priority,
        status=TicketStatus.OPEN,
        assigned_agent=None,
        created_at=current_time,
        updated_at=current_time,
    )

    tickets.append(ticket)
    next_ticket_id += 1

    return ticket


@app.get("/tickets", response_model=list[Ticket])
def get_tickets() -> list[Ticket]:
    return tickets


@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int) -> Ticket:
    ticket_index = find_ticket_index(ticket_id)
    return tickets[ticket_index]


@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
) -> Ticket:
    ticket_index = find_ticket_index(ticket_id)
    existing_ticket = tickets[ticket_index]

    update_data = ticket_data.model_dump(exclude_unset=True)

    if "status" in update_data and update_data["status"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Status cannot be null",
        )

    if "priority" in update_data and update_data["priority"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Priority cannot be null",
        )

    if not update_data:
        return existing_ticket

    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_ticket = existing_ticket.model_copy(update=update_data)
    tickets[ticket_index] = updated_ticket

    return updated_ticket