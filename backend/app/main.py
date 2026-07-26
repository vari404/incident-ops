from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status

from backend.app.schemas import Ticket, TicketCreate, TicketStatus


app = FastAPI(
    title="IncidentOps API",
    description="Backend API for the IncidentOps support platform.",
    version="0.2.0",
)


tickets: list[Ticket] = []
next_ticket_id = 1


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
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ticket not found",
    )